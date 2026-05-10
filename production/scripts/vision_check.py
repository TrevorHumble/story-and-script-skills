"""Mid-render Haiku vision verification with structured-category verdict and
optional justification step.

This module extends the binary PASS/FAIL design from issue #1 to a two-step
pipeline:

Step 1 — Structured verdict
    Haiku examines the frame image and returns one of six category tokens:
        PASS
        FAIL_BLACK
        FAIL_NO_CHARACTERS
        FAIL_BROKEN_GEOMETRY
        FAIL_WRONG_SCALE
        FAIL_OTHER: <one-sentence reason>

    The prompt is scoped to render correctness ONLY.  Haiku must not comment
    on pose, framing, expression, lighting mood, or any creative judgment.

Step 2 — Justification (only for FAIL_BLACK and FAIL_NO_CHARACTERS)
    Categories FAIL_BROKEN_GEOMETRY, FAIL_WRONG_SCALE, and FAIL_OTHER skip
    justification — render artifacts cannot be narratively justified, and the
    filter saves API calls while preventing false-justified flags on genuine
    render bugs.

    When justification is eligible:
        - JUSTIFICATION_ENABLED env var (default "1") must be "1".
        - Haiku receives the failure category, script excerpt, director's
          notes, and recent frame history (capped at 5 entries).
        - Haiku answers JUSTIFIED: <reason> or CONFIRMED_FAIL: <reason>.
        - Timeout (10 s) → CONFIRMED_FAIL (conservative — we cannot dismiss
          a failure we couldn't justify; opposite of step-1's PASS-on-timeout).

Output parsing
--------------
Step 1: first line of response, stripped.  Matches one of the six tokens; if
    it starts with "FAIL_OTHER:" the remainder is the reason.  Anything else
    is a parse error → category = FAIL_OTHER, reason = raw text.

Step 2: first line of response, stripped.  Must begin with "JUSTIFIED:" or
    "CONFIRMED_FAIL:".  Text after the colon is the reason.  Parse error →
    CONFIRMED_FAIL (conservative).

Disposition logic (implemented in render_scene.py, documented here for clarity)
--------------------------------------------------------------------------------
    PASS category                          → PASS disposition
    FAIL category + JUSTIFIED              → PASS_WITH_NOTE disposition
    FAIL category + CONFIRMED_FAIL         → FAIL disposition
    FAIL category + justification disabled → FAIL disposition
    FAIL category not eligible for step-2  → FAIL disposition (no step-2 run)

Configuration env vars
----------------------
JUSTIFICATION_ENABLED   default 1   — set to 0 to skip step 2 entirely.
                                       Step 1 structured taxonomy still applies;
                                       any non-PASS category counts as FAIL.
JUSTIFICATION_MODEL     default same as VISION_MODEL — could be Sonnet for
                        harder reasoning if needed.
VISION_MODEL            default claude-haiku-4-5-20251001.
VISION_TIMEOUT_SECONDS  default 10.

Runtime requirements
--------------------
* ANTHROPIC_API_KEY environment variable must be set.
* The ``anthropic`` Python package must be importable.
  - In a Blender-hosted run: install into Blender's bundled Python:
    ``"C:\\Program Files\\Blender Foundation\\Blender 5.1\\5.1\\python\\bin\\python.exe" -m pip install anthropic``
* No API key is needed to *import* this module — only to call verify_frame()
  or justify_failure() at runtime.
"""

from __future__ import annotations

import base64
import concurrent.futures
import logging
import os
import textwrap
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Model / timeout configuration
# ---------------------------------------------------------------------------

DEFAULT_MODEL = "claude-haiku-4-5-20251001"

# Hard timeout per API call.  Step-1 timeout → PASS.  Step-2 timeout → CONFIRMED_FAIL.
_CALL_TIMEOUT_SECONDS = int(os.environ.get("VISION_TIMEOUT_SECONDS", "10"))


def _model() -> str:
    return os.environ.get("VISION_MODEL", DEFAULT_MODEL)


def _justification_model() -> str:
    return os.environ.get("JUSTIFICATION_MODEL", _model())


def _justification_enabled() -> bool:
    return os.environ.get("JUSTIFICATION_ENABLED", "1") != "0"


# ---------------------------------------------------------------------------
# Category and disposition constants
# ---------------------------------------------------------------------------

PASS = "PASS"
FAIL_BLACK = "FAIL_BLACK"
FAIL_NO_CHARACTERS = "FAIL_NO_CHARACTERS"
FAIL_BROKEN_GEOMETRY = "FAIL_BROKEN_GEOMETRY"
FAIL_WRONG_SCALE = "FAIL_WRONG_SCALE"
FAIL_OTHER = "FAIL_OTHER"

# All recognised non-PASS categories.
FAIL_CATEGORIES = frozenset(
    {FAIL_BLACK, FAIL_NO_CHARACTERS, FAIL_BROKEN_GEOMETRY, FAIL_WRONG_SCALE, FAIL_OTHER}
)

# Only these categories trigger the justification step.
# FAIL_BROKEN_GEOMETRY, FAIL_WRONG_SCALE, FAIL_OTHER are render artifacts:
# no script can justify broken geometry or wrong-scale characters.  Skipping
# justification for these saves API calls and prevents false-justified flags.
JUSTIFICATION_ELIGIBLE = frozenset({FAIL_BLACK, FAIL_NO_CHARACTERS})

# Final disposition values (used in _verification_log.md and SceneState).
DISPOSITION_PASS = "PASS"
DISPOSITION_PASS_WITH_NOTE = "PASS_WITH_NOTE"
DISPOSITION_FAIL = "FAIL"

# ---------------------------------------------------------------------------
# Prompt templates  (do not paraphrase — bounded to render correctness)
# ---------------------------------------------------------------------------

_STEP1_PROMPT = textwrap.dedent("""\
    You are a render-correctness supervisor. Examine this frame from scene \
"{scene_name}" (scene {scene_number}).
    Expected characters: {expected_characters}
    Scene description: {scene_description}

    Flag ONLY render-correctness problems. DO NOT comment on pose, framing, \
expression, lighting mood, or any creative judgment.

    Respond with exactly one of:
    PASS
    FAIL_BLACK
    FAIL_NO_CHARACTERS
    FAIL_BROKEN_GEOMETRY
    FAIL_WRONG_SCALE
    FAIL_OTHER: <one sentence reason>""")

_STEP2_PROMPT = textwrap.dedent("""\
    You are a render-correctness supervisor reviewing a flagged frame.

    Scene: "{scene_name}" (scene {scene_number})
    Script excerpt: {script_excerpt}
    Director's notes: {directors_notes_paragraph}
    Failure detected: {failure_category}
    Recent frame history: {frame_history_summary}

    Given the script, is this failure narratively justified? Answer exactly:
    JUSTIFIED: <one sentence reason>
    or
    CONFIRMED_FAIL: <one sentence reason>""")

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _encode_image(image_path: str) -> str:
    """Return base64-encoded bytes for an image file."""
    with open(image_path, "rb") as fh:
        return base64.standard_b64encode(fh.read()).decode("ascii")


def _media_type(image_path: str) -> str:
    ext = os.path.splitext(image_path)[1].lower()
    return "image/jpeg" if ext in {".jpg", ".jpeg"} else "image/png"


def _get_client(client: Any) -> Any:
    """Return the supplied Anthropic client or create a default one."""
    if client is not None:
        return client
    try:
        import anthropic  # type: ignore[import]
    except ImportError as exc:
        raise ImportError(
            "The 'anthropic' Python SDK is required for vision verification. "
            "Install it with: pip install anthropic\n"
            "For Blender's bundled Python on Windows:\n"
            "  \"C:\\Program Files\\Blender Foundation\\Blender 5.1\\5.1\\python\\bin\\python.exe\""
            " -m pip install anthropic"
        ) from exc
    return anthropic.Anthropic()


def _parse_step1(raw: str, image_path: str) -> Dict[str, str]:
    """Parse step-1 response into {category, reason}.

    Rules:
    - Inspect the first line only (stripped).
    - Exact match against category tokens.
    - FAIL_OTHER: the text after the colon is the reason.
    - Anything else → parse error, logged, treated as FAIL_OTHER.
    """
    first = raw.strip().splitlines()[0].strip() if raw.strip() else ""

    if first == PASS:
        return {"category": PASS, "reason": ""}

    for token in (FAIL_BLACK, FAIL_NO_CHARACTERS, FAIL_BROKEN_GEOMETRY, FAIL_WRONG_SCALE):
        if first == token:
            return {"category": token, "reason": ""}

    if first.startswith(FAIL_OTHER + ":"):
        reason = first[len(FAIL_OTHER) + 1:].strip()
        return {"category": FAIL_OTHER, "reason": reason}

    # Parse error.
    _log(
        f"step-1 parse error for {image_path!r} — unexpected response {first!r}; "
        "treating as FAIL_OTHER"
    )
    return {"category": FAIL_OTHER, "reason": f"parse error: {first!r}"}


def _parse_step2(raw: str) -> Dict[str, str]:
    """Parse step-2 response into {verdict, reason}.

    Rules:
    - Inspect the first line only (stripped).
    - Must begin with "JUSTIFIED:" or "CONFIRMED_FAIL:".
    - Text after the colon is the reason.
    - Parse error → CONFIRMED_FAIL (conservative).
    """
    first = raw.strip().splitlines()[0].strip() if raw.strip() else ""

    if first.startswith("JUSTIFIED:"):
        return {"verdict": "JUSTIFIED", "reason": first[len("JUSTIFIED:"):].strip()}

    if first.startswith("CONFIRMED_FAIL:"):
        return {"verdict": "CONFIRMED_FAIL", "reason": first[len("CONFIRMED_FAIL:"):].strip()}

    _log(
        f"step-2 parse error — unexpected response {first!r}; treating as CONFIRMED_FAIL (conservative)"
    )
    return {
        "verdict": "CONFIRMED_FAIL",
        "reason": f"parse error — malformed justification response: {first!r}",
    }


def _log(msg: str) -> None:
    """Print in the === format recognised by render_all.sh."""
    print(f"=== [vision_check] {msg}")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def verify_frame(
    image_path: str,
    scene_name: str,
    scene_number: int | str,
    expected_characters: str,
    scene_description: str,
    *,
    client: Any = None,
) -> Dict[str, str]:
    """Run step-1 structured-category verdict on a rendered frame.

    The structured taxonomy is always used (even when JUSTIFICATION_ENABLED=0)
    so callers always receive a rich category rather than a binary verdict.

    Network/timeout handling:
        Hard timeout (default 10 s, VISION_TIMEOUT_SECONDS).  On timeout,
        treat as PASS — a transient API failure should not punish the render.
        Timeout is logged.  Step-2 has the opposite convention (CONFIRMED_FAIL
        on timeout) because inability to justify a failure is not a pass.

    Args:
        image_path:          Absolute path to the PNG/JPEG frame to examine.
        scene_name:          Human-readable scene name, e.g. ``"Beach"``.
        scene_number:        Scene index, e.g. ``5`` or ``"Act.1-Scene.5"``.
        expected_characters: Comma-separated character names expected on screen.
        scene_description:   One-sentence description from directors_notes.md.
        client:              Optional pre-constructed ``anthropic.Anthropic``
                             instance (useful for testing / mocking).

    Returns:
        Dict with keys:

        ``category``
            One of: PASS, FAIL_BLACK, FAIL_NO_CHARACTERS, FAIL_BROKEN_GEOMETRY,
            FAIL_WRONG_SCALE, FAIL_OTHER.

        ``disposition``
            ``"PASS"`` when category is PASS; ``"FAIL"`` otherwise.
            (Step-2 justification is not run here — render_scene.py calls
            :func:`justify_failure` for eligible categories and derives the
            final PASS_WITH_NOTE disposition.)

        ``reason``
            Human-readable reason (empty string on PASS).
    """
    anthropic_client = _get_client(client)

    prompt = _STEP1_PROMPT.format(
        scene_name=scene_name,
        scene_number=scene_number,
        expected_characters=expected_characters,
        scene_description=scene_description,
    )

    encoded = _encode_image(image_path)
    media = _media_type(image_path)

    def _call() -> Dict[str, str]:
        response = anthropic_client.messages.create(
            model=_model(),
            max_tokens=64,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media,
                                "data": encoded,
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )
        raw = response.content[0].text if response.content else ""
        return _parse_step1(raw, image_path)

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        future = ex.submit(_call)
        try:
            parsed = future.result(timeout=_CALL_TIMEOUT_SECONDS)
        except concurrent.futures.TimeoutError:
            _log(
                f"step-1 vision check timed out after {_CALL_TIMEOUT_SECONDS}s "
                f"for {image_path!r}; treating as PASS"
            )
            return {
                "category": PASS,
                "disposition": DISPOSITION_PASS,
                "reason": "timeout — treated as PASS",
            }
        except Exception as exc:  # noqa: BLE001
            _log(f"step-1 exception ({type(exc).__name__}: {exc}) — treating as PASS")
            return {
                "category": PASS,
                "disposition": DISPOSITION_PASS,
                "reason": f"exception: {exc}",
            }

    category = parsed["category"]
    reason = parsed["reason"]

    if category == PASS:
        return {"category": PASS, "disposition": DISPOSITION_PASS, "reason": reason}

    return {"category": category, "disposition": DISPOSITION_FAIL, "reason": reason}


def justify_failure(
    category: str,
    scene_name: str,
    scene_number: int | str,
    script_excerpt: str,
    directors_notes_paragraph: str,
    frame_history: List[str],
    *,
    client: Any = None,
) -> Dict[str, str]:
    """Run step-2 justification against the scene script for an eligible failure.

    Eligibility filter: only FAIL_BLACK and FAIL_NO_CHARACTERS trigger this
    check.  FAIL_BROKEN_GEOMETRY, FAIL_WRONG_SCALE, and FAIL_OTHER are render
    artifacts; no script can justify them.  This filter saves API calls and
    prevents false-justified flags on genuine render bugs.

    Calling this function with an ineligible category is safe — it returns
    CONFIRMED_FAIL immediately with an explanatory reason and makes no API call.

    Timeout convention (opposite of step-1):
        On timeout → CONFIRMED_FAIL.  A failure we cannot justify is a failure
        we cannot dismiss.

    JUSTIFICATION_ENABLED=0:
        Returns CONFIRMED_FAIL immediately without an API call.  render_scene.py
        checks this flag before calling here, but the guard is duplicated for
        safety.

    Args:
        category:                  Step-1 category string.
        scene_name:                Human-readable scene name.
        scene_number:              Scene index.
        script_excerpt:            Relevant script paragraph(s) for this scene.
        directors_notes_paragraph: Director's notes paragraph for this scene.
        frame_history:             List of formatted strings from
                                   :meth:`SceneState.frame_history`, max 5 entries.
        client:                    Optional pre-constructed Anthropic client.

    Returns:
        Dict with keys:

        ``verdict``
            ``"JUSTIFIED"`` or ``"CONFIRMED_FAIL"``.

        ``reason``
            One-sentence explanation.
    """
    if not _justification_enabled():
        return {
            "verdict": "CONFIRMED_FAIL",
            "reason": "justification disabled (JUSTIFICATION_ENABLED=0)",
        }

    if category not in JUSTIFICATION_ELIGIBLE:
        return {
            "verdict": "CONFIRMED_FAIL",
            "reason": (
                f"{category} is a render artifact; no script can justify it — "
                "justification skipped to prevent false-justified flags on genuine render bugs"
            ),
        }

    anthropic_client = _get_client(client)

    frame_history_summary = "\n".join(frame_history) if frame_history else "(no prior frames)"

    prompt = _STEP2_PROMPT.format(
        scene_name=scene_name,
        scene_number=scene_number,
        script_excerpt=script_excerpt,
        directors_notes_paragraph=directors_notes_paragraph,
        failure_category=category,
        frame_history_summary=frame_history_summary,
    )

    def _call() -> Dict[str, str]:
        response = anthropic_client.messages.create(
            model=_justification_model(),
            max_tokens=64,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text if response.content else ""
        return _parse_step2(raw)

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        future = ex.submit(_call)
        try:
            return future.result(timeout=_CALL_TIMEOUT_SECONDS)
        except concurrent.futures.TimeoutError:
            _log(
                f"step-2 justification timed out after {_CALL_TIMEOUT_SECONDS}s "
                f"for category {category}; treating as CONFIRMED_FAIL (conservative)"
            )
            return {
                "verdict": "CONFIRMED_FAIL",
                "reason": "justification API timeout; failure stands (conservative)",
            }
        except Exception as exc:  # noqa: BLE001
            _log(f"step-2 exception ({type(exc).__name__}: {exc}) — treating as CONFIRMED_FAIL")
            return {
                "verdict": "CONFIRMED_FAIL",
                "reason": f"exception during justification: {exc}",
            }

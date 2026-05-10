"""Render the currently open scene to a PNG/EXR sequence with mid-render
vision verification (Production Skill 02 v2.3.0).

Usage (unchanged from v1 for backward compatibility with render_all.sh):

    blender --background scene.blend --python render_scene.py -- /path/to/output_root [options]

Options after the output root:
    --no-vision     Skip vision checks; use file-system verification only.
                    Useful when ANTHROPIC_API_KEY is unavailable or for cost control.
    --dry-run       Run verification logic against existing renders but do NOT
                    call bpy.ops.render.render().  Useful for testing the
                    supervisor against an already-rendered scene folder.

Output structure (unchanged):
    output_root/
      Act.1-Scene.5-Beach/
        Beach_0001.png
        Beach_0002.png
        ...
        _verification_log.md    <- per-frame vision audit trail
        .last_completed_frame   <- resume marker; deleted on COMPLETED
        scene_context.json      <- hand-authored before first run
    render_log.jsonl            <- append-mode structured log, one JSON object per scene

Per-scene vision verification uses the structured-category + optional
justification pipeline from vision_check.py (issue #3).  The binary PASS/FAIL
form from issue #1 is also supported via --no-vision fallback.

Disposition logic:
    PASS category                              -> PASS disposition
    FAIL_BLACK or FAIL_NO_CHARACTERS + JUSTIFIED   -> PASS_WITH_NOTE (no fail counter)
    FAIL_BLACK or FAIL_NO_CHARACTERS + CONFIRMED_FAIL -> FAIL (increment counter)
    FAIL_BROKEN_GEOMETRY, FAIL_WRONG_SCALE,
        FAIL_OTHER (ineligible for step-2)         -> FAIL (increment counter)
    3 consecutive FAIL dispositions                -> abort this scene

Scene context for verification is loaded from:
  1. <output_root>/<scene_label>/scene_context.json (preferred, per issue #1 spec)
  2. SCENE_CONTEXT_JSON env var (JSON file path)
  3. SCENE_CONTEXT_INLINE env var (raw JSON string)

Stdout format:
    Lines prefixed with "=== " are preserved for the render_all.sh grep filter.
    Structured log goes to render_log.jsonl; stdout stays human-readable.

Defaults are tuned for animatic speed: half-resolution (50% of scene's
resolution_x/y), EEVEE engine, PNG output.
"""

import bpy
import sys
import os
import json
import time
import datetime
from typing import Optional

# ==============================
# SETTINGS
# ==============================

RESOLUTION_PERCENTAGE = 50  # 50% of scene's resolution_x/y; lower = faster
FRAME_RATE = 24
ENGINE = "BLENDER_EEVEE_NEXT"  # Blender 5.x EEVEE; falls back to BLENDER_EEVEE for 4.x
FILE_FORMAT = "PNG"

# Vision verification settings.
SAMPLE_INTERVAL = int(os.environ.get("SAMPLE_INTERVAL", "24"))    # check every Nth frame
ABORT_THRESHOLD = int(os.environ.get("ABORT_THRESHOLD", "3"))      # consecutive FAILs before abort
LOG_PASS_WITH_NOTE_THRESHOLD = int(
    os.environ.get("LOG_PASS_WITH_NOTE_THRESHOLD", "1")
)  # min PASS_WITH_NOTE count to mention in artist summary

# Resume marker and structured log filenames.
_RESUME_MARKER = ".last_completed_frame"
_LOG_FILENAME = "render_log.jsonl"

# ==============================


def _log(msg: str) -> None:
    print(f"=== {msg}")


def parse_output_root():
    """Parse output root and optional flags from sys.argv.

    Returns:
        Tuple of (output_root: str, no_vision: bool, dry_run: bool).

    Raises:
        RuntimeError: If the output root is missing.
    """
    argv = sys.argv
    if "--" not in argv:
        raise RuntimeError("Pass output root after --, e.g.: -- /path/to/renders")
    args = argv[argv.index("--") + 1:]
    if not args:
        raise RuntimeError("Pass output root after --, e.g.: -- /path/to/renders")

    output_root = args[0]
    no_vision = "--no-vision" in args
    dry_run = "--dry-run" in args
    return output_root, no_vision, dry_run


def scene_label(blend_path: str) -> str:
    """Derive 'Act.1-Scene.5-Beach' from the blend filename."""
    base = os.path.splitext(os.path.basename(blend_path))[0]
    if base.endswith(" - complete"):
        base = base[: -len(" - complete")]
    return base


# Expose as _scene_label alias for smoke-test compatibility.
_scene_label = scene_label


# ---------------------------------------------------------------------------
# Resume support (issue #1)
# ---------------------------------------------------------------------------


def _read_resume_frame(out_dir: str) -> Optional[int]:
    """Return the last completed frame number from the resume marker, or None.

    Args:
        out_dir: Per-scene output directory.
    """
    marker = os.path.join(out_dir, _RESUME_MARKER)
    if not os.path.exists(marker):
        return None
    try:
        with open(marker, "r") as fh:
            return int(fh.read().strip())
    except (ValueError, OSError):
        return None


def _write_resume_frame(out_dir: str, frame: int) -> None:
    """Write *frame* to the resume marker file after each successful render.

    Args:
        out_dir: Per-scene output directory.
        frame:   Blender frame number just completed.
    """
    marker = os.path.join(out_dir, _RESUME_MARKER)
    try:
        with open(marker, "w") as fh:
            fh.write(str(frame))
    except OSError as exc:
        _log(f"WARNING: Could not write resume marker ({exc})")


def _delete_resume_marker(out_dir: str) -> None:
    """Delete the resume marker on successful scene completion.

    Args:
        out_dir: Per-scene output directory.
    """
    marker = os.path.join(out_dir, _RESUME_MARKER)
    try:
        os.remove(marker)
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Structured log (issue #1)
# ---------------------------------------------------------------------------


def _append_log_entry(output_root: str, entry: dict) -> None:
    """Append *entry* as a JSON line to render_log.jsonl (append mode).

    Args:
        output_root: Root output directory.
        entry:       Dict from :meth:`state_tracking.SceneState.to_log_entry`.
    """
    log_path = os.path.join(output_root, _LOG_FILENAME)
    try:
        with open(log_path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")
    except OSError as exc:
        _log(f"WARNING: Could not write {_LOG_FILENAME} ({exc})")


def load_scene_context(output_root: Optional[str] = None, label: Optional[str] = None) -> dict | None:
    """Load per-scene context dict.

    Resolution order:
    1. Sidecar JSON at <output_root>/<label>/scene_context.json (issue #1 spec).
    2. SCENE_CONTEXT_JSON env var (path to a JSON file).
    3. SCENE_CONTEXT_INLINE env var (raw JSON string).
    Returns None if no context can be loaded (vision verification is skipped).

    Expected dict shape:
        {
            "scene_label":          "Act.1-Scene.5-Beach",
            "expected_characters":  ["Florence", "Sebastian"],
            "description":          "Florence takes Sebastian's hand.",
            "script_excerpt":       "...",
            "directors_notes_paragraph": "..."
        }
    Note: scene_name and scene_number are derived automatically if absent.
    """
    # 1. Sidecar file (preferred path from issue #1).
    if output_root is not None and label is not None:
        sidecar = os.path.join(output_root, label, "scene_context.json")
        if os.path.exists(sidecar):
            try:
                with open(sidecar, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                # Derive scene_name / scene_number from label if absent.
                _enrich_context(data, label)
                return data
            except (json.JSONDecodeError, OSError) as exc:
                _log(f"WARNING: Could not parse {sidecar} ({exc}) — trying env vars")

    # 2. Env-var JSON path.
    inline = os.environ.get("SCENE_CONTEXT_INLINE")
    if inline:
        try:
            data = json.loads(inline)
            _enrich_context(data, label or "")
            return data
        except json.JSONDecodeError as exc:
            _log(f"WARNING: SCENE_CONTEXT_INLINE is not valid JSON ({exc}) — skipping verification")
            return None

    json_path = os.environ.get("SCENE_CONTEXT_JSON")
    if json_path:
        if not os.path.exists(json_path):
            _log(f"WARNING: SCENE_CONTEXT_JSON path {json_path!r} does not exist — skipping verification")
            return None
        try:
            with open(json_path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            _enrich_context(data, label or "")
            return data
        except (json.JSONDecodeError, OSError) as exc:
            _log(f"WARNING: Could not parse SCENE_CONTEXT_JSON ({exc}) — skipping verification")
            return None

    return None


def _enrich_context(data: dict, label: str) -> None:
    """Fill in scene_name and scene_number derived from *label* if absent.

    Mutates *data* in place.  E.g. 'Act.1-Scene.5-Beach' -> scene_number
    = 'Act.1-Scene.5', scene_name = 'Beach'.
    """
    if "scene_name" not in data or "scene_number" not in data:
        parts = label.rsplit("-", 1)
        if len(parts) == 2:
            data.setdefault("scene_number", parts[0])
            data.setdefault("scene_name", parts[1])
        else:
            data.setdefault("scene_number", label)
            data.setdefault("scene_name", label)

    # Normalise expected_characters to a comma-joined string for prompt formatting.
    chars = data.get("expected_characters", [])
    if isinstance(chars, list):
        data["expected_characters"] = ", ".join(chars) if chars else "(none specified)"


def write_verification_log(out_dir: str, checks: list) -> None:
    """Write the per-scene _verification_log.md audit file.

    Schema (one row per sample frame):

    | Frame | Raw verdict | Raw reason | Justification | Justification reason | Final disposition | consec_fails |
    |---|---|---|---|---|---|---|
    | 24 | FAIL_NO_CHARACTERS | | JUSTIFIED | Script: camera pan, Florence not due until frame 96 | PASS_WITH_NOTE | 0 |

    For scenes that complete cleanly, the log still exists with header + zero rows.

    Args:
        out_dir: Per-scene output directory (e.g. .../Act.1-Scene.5-Beach/).
        checks:  List of check dicts from SceneState._checks.
    """
    log_path = os.path.join(out_dir, "_verification_log.md")
    header = (
        "| Frame | Raw verdict | Raw reason | Justification | Justification reason "
        "| Final disposition | consec_fails |\n"
        "|---|---|---|---|---|---|---|\n"
    )
    rows = []
    running_consec = 0
    for entry in checks:
        disposition = entry.get("disposition", entry.get("verdict", ""))
        if disposition in ("PASS", "PASS_WITH_NOTE"):
            running_consec = 0
        else:
            running_consec += 1

        row = (
            f"| {entry['frame']} "
            f"| {entry.get('category', entry.get('verdict', ''))} "
            f"| {entry.get('reason', '')} "
            f"| {entry.get('justification', '—')} "
            f"| {entry.get('justification_reason', '')} "
            f"| {disposition} "
            f"| {running_consec} |\n"
        )
        rows.append(row)

    with open(log_path, "w", encoding="utf-8") as fh:
        fh.write("# Vision Verification Log\n\n")
        fh.write(header)
        fh.writelines(rows)

    _log(f"Wrote verification log: {log_path}")


def run_vision_check(
    frame_path: str,
    scene_ctx: dict,
    state,
    frame_number: int,
    verify_fn,
    justify_fn,
) -> str:
    """Run step-1 verify + optional step-2 justify, record in state, return disposition.

    Args:
        frame_path:   Absolute path to the rendered PNG for this frame.
        scene_ctx:    Scene context dict (from load_scene_context).
        state:        SceneState instance for this scene.
        frame_number: Blender frame number being checked.
        verify_fn:    vision_check.verify_frame callable (injectable for tests).
        justify_fn:   vision_check.justify_failure callable (injectable for tests).

    Returns:
        Final disposition string: "PASS", "PASS_WITH_NOTE", or "FAIL".
    """
    from vision_check import JUSTIFICATION_ELIGIBLE, DISPOSITION_PASS, DISPOSITION_PASS_WITH_NOTE, DISPOSITION_FAIL

    # Step 1 — structured verdict.
    result = verify_fn(
        frame_path,
        scene_ctx.get("scene_name", "unknown"),
        scene_ctx.get("scene_number", "?"),
        scene_ctx.get("expected_characters", "(none specified)"),
        scene_ctx.get("description", "(no description)"),
    )
    category = result["category"]
    reason = result.get("reason", "")
    initial_disposition = result["disposition"]

    _log(
        f"Frame {frame_number}: {category}"
        + (f" — {reason}" if reason else "")
    )

    if initial_disposition == DISPOSITION_PASS:
        state.record_check(
            frame_number,
            verdict="PASS",
            reason=reason,
            category=category,
            disposition=DISPOSITION_PASS,
            justification="—",
            justification_reason="",
        )
        return DISPOSITION_PASS

    # Non-PASS: determine eligibility for step-2 justification.
    from vision_check import _justification_enabled
    justification_enabled = _justification_enabled()

    if not justification_enabled or category not in JUSTIFICATION_ELIGIBLE:
        # Justification either disabled or ineligible (render artifact).
        just_label = "SKIPPED (disabled)" if not justification_enabled else "SKIPPED (not eligible)"
        just_reason = (
            "justification disabled (JUSTIFICATION_ENABLED=0)"
            if not justification_enabled
            else f"{category} is a render artifact; justification not applicable"
        )
        state.record_check(
            frame_number,
            verdict="FAIL",
            reason=reason,
            category=category,
            disposition=DISPOSITION_FAIL,
            justification=just_label,
            justification_reason=just_reason,
        )
        _log(f"Frame {frame_number}: disposition=FAIL ({just_label})")
        return DISPOSITION_FAIL

    # Step 2 — justification.
    history = state.frame_history(max=5)
    just_result = justify_fn(
        category,
        scene_ctx.get("scene_name", "unknown"),
        scene_ctx.get("scene_number", "?"),
        scene_ctx.get("script_excerpt", "(no script excerpt provided)"),
        scene_ctx.get("directors_notes_paragraph", "(no director's notes provided)"),
        history,
    )
    verdict = just_result["verdict"]
    just_reason = just_result.get("reason", "")

    if verdict == "JUSTIFIED":
        disposition = DISPOSITION_PASS_WITH_NOTE
        _log(
            f"Frame {frame_number}: disposition=PASS_WITH_NOTE "
            f"(JUSTIFIED — {just_reason})"
        )
    else:
        disposition = DISPOSITION_FAIL
        _log(
            f"Frame {frame_number}: disposition=FAIL "
            f"(CONFIRMED_FAIL — {just_reason})"
        )

    state.record_check(
        frame_number,
        verdict="FAIL",
        reason=reason,
        category=category,
        disposition=disposition,
        justification=verdict,
        justification_reason=just_reason,
    )
    return disposition


def main():
    output_root, no_vision, dry_run = parse_output_root()

    # Resolve helper module paths.
    _scripts_dir = os.path.dirname(os.path.abspath(__file__))
    if _scripts_dir not in sys.path:
        sys.path.insert(0, _scripts_dir)

    label = scene_label(bpy.data.filepath)
    out_dir = os.path.join(output_root, label)
    os.makedirs(out_dir, exist_ok=True)

    scene = bpy.context.scene

    # Apply render settings (skip in dry-run to avoid mutating the scene).
    if not dry_run:
        try:
            scene.render.engine = ENGINE
        except TypeError:
            scene.render.engine = "BLENDER_EEVEE"
        scene.render.image_settings.file_format = FILE_FORMAT
        scene.render.resolution_percentage = RESOLUTION_PERCENTAGE
        scene.render.fps = FRAME_RATE
        scene.render.filepath = os.path.join(out_dir, label + "_")

    # Resume support: start from the last completed frame if a marker exists.
    resume_from = _read_resume_frame(out_dir)
    if resume_from is not None:
        start_frame = resume_from + 1
        _log(f"Resuming {label} from frame {start_frame} (last completed: {resume_from})")
    else:
        start_frame = scene.frame_start

    _log(f"Rendering {label}")
    _log(
        f"Frames {start_frame}-{scene.frame_end} "
        f"({'dry-run' if dry_run else 'live'}, "
        f"{'no-vision' if no_vision else 'vision'}) -> {out_dir}"
    )

    # --- Vision verification setup ---
    scene_ctx = None if no_vision else load_scene_context(output_root, label)
    verify_available = scene_ctx is not None and not no_vision

    if not verify_available and not no_vision:
        _log(
            "WARNING: no scene context found (scene_context.json / "
            "SCENE_CONTEXT_JSON / SCENE_CONTEXT_INLINE) — "
            "vision verification disabled for this scene"
        )

    verify_fn = justify_fn = None
    if verify_available:
        try:
            from vision_check import verify_frame as _vf, justify_failure as _jf
            verify_fn, justify_fn = _vf, _jf
        except ImportError as exc:
            _log(f"WARNING: vision_check module not importable ({exc}) — vision verification disabled")
            verify_available = False

    # --- State ---
    from state_tracking import SceneState
    state = SceneState(label, out_dir)
    state.frames_expected = scene.frame_end - scene.frame_start + 1

    # --- Per-frame render loop (v2.3.0 architecture) ---
    aborted = False
    for frame in range(start_frame, scene.frame_end + 1):
        if not dry_run:
            scene.frame_set(frame)
            bpy.ops.render.render(write_still=True)

        state.record_frame(frame)
        _write_resume_frame(out_dir, frame)

        # Determine the path of the just-rendered frame.
        frame_filename = f"{label}_{frame:04d}.png"
        frame_path = os.path.join(out_dir, frame_filename)

        # Sample frame check (every SAMPLE_INTERVAL frames relative to scene start).
        relative = frame - scene.frame_start
        if verify_available and relative % SAMPLE_INTERVAL == 0:
            if not os.path.exists(frame_path):
                _log(f"Frame {frame}: rendered file not found at {frame_path!r} — skipping check")
            else:
                disposition = run_vision_check(
                    frame_path, scene_ctx, state, frame, verify_fn, justify_fn
                )
                if state.consecutive_fails() >= ABORT_THRESHOLD:
                    _log(
                        f"ABORT: {state.consecutive_fails()} consecutive FAIL dispositions "
                        f"(threshold {ABORT_THRESHOLD}) — aborting scene {label}"
                    )
                    aborted = True
                    break

    # --- Write per-scene verification log ---
    write_verification_log(out_dir, state.to_log_entry()["checks"])

    # --- Determine final status ---
    if aborted:
        state.finalise("ABORTED")
        _log(f"Scene {label}: ABORTED")
        _append_log_entry(output_root, state.to_log_entry())
        return

    _delete_resume_marker(out_dir)

    # File-system verification.
    if not os.path.isdir(out_dir):
        state.finalise("FAILED_FILESYSTEM")
        _append_log_entry(output_root, state.to_log_entry())
        raise RuntimeError(f"Output directory not found after render: {out_dir}")

    if not dry_run:
        frame_files = [
            f for f in os.listdir(out_dir)
            if f.endswith(".png") and not f.startswith("_")
        ]
        actual = len(frame_files)
        expected = state.frames_expected
        if actual != expected:
            state.finalise("FAILED_FILESYSTEM")
            _append_log_entry(output_root, state.to_log_entry())
            raise RuntimeError(
                f"Frame count mismatch for {label}: expected {expected}, found {actual}"
            )

        first_frame = os.path.join(out_dir, f"{label}_{scene.frame_start:04d}.png")
        last_frame = os.path.join(out_dir, f"{label}_{scene.frame_end:04d}.png")
        for f in (first_frame, last_frame):
            if not os.path.exists(f) or os.path.getsize(f) == 0:
                state.finalise("FAILED_FILESYSTEM")
                _append_log_entry(output_root, state.to_log_entry())
                raise RuntimeError(f"Frame file missing or empty: {f}")

    if state.vision_fails_total > 0:
        state.finalise("COMPLETED_WITH_FLAGS")
        _log(
            f"Scene {label}: COMPLETED_WITH_FLAGS "
            f"({state.vision_fails_total} FAIL(s), "
            f"{state.pass_with_note_total} PASS_WITH_NOTE(s))"
        )
    else:
        state.finalise("COMPLETED")
        _log(f"Scene {label}: COMPLETED")

    # --- Artist-facing PASS_WITH_NOTE summary ---
    if state.pass_with_note_total >= LOG_PASS_WITH_NOTE_THRESHOLD:
        _log(
            f"ARTIST NOTE: {state.pass_with_note_total} PASS_WITH_NOTE frame(s) in {label} "
            f"— spot-check {os.path.join(out_dir, '_verification_log.md')}"
        )

    entry = state.to_log_entry()
    _append_log_entry(output_root, entry)
    _log(
        f"Done {label}: "
        f"{entry['frames_rendered']}/{entry['frames_expected']} frames, "
        f"{entry['vision_checks_made']} checks, "
        f"{entry['vision_fails']} confirmed fail(s), "
        f"{entry.get('pass_with_note', 0)} pass-with-note(s), "
        f"{entry['elapsed_seconds']}s"
    )


main()

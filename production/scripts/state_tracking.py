"""Per-scene render state tracking for the mid-render vision verification pipeline.

Tracks frames rendered, vision checks made, consecutive failure count, and final
status. Serialises to a dict for appending to render_log.jsonl.

Status values (exact strings used in structured log):
    COMPLETED              — loop finished, file-system check passed, no vision FAILs
    COMPLETED_WITH_FLAGS   — loop finished, file-system check passed, had vision FAILs
                            but did not reach abort threshold
    ABORTED                — vision-check abort threshold reached mid-render
    FAILED_FILESYSTEM      — post-render file-system verification failed

Issue #3 additions
------------------
record_check() now accepts structured fields from the justification pipeline:
    category        — step-1 verdict category (PASS, FAIL_BLACK, etc.)
    disposition     — final PASS / PASS_WITH_NOTE / FAIL after step-2
    justification   — JUSTIFIED / CONFIRMED_FAIL / SKIPPED (disabled) / — (not run)
    justification_reason — one-sentence reason from step-2, or empty

frame_history(max=5) returns the last N check entries formatted for the step-2
prompt's {frame_history_summary} placeholder:
    frame {N}: {disposition} ({category})
"""

from __future__ import annotations

import time
from typing import List, Dict, Any, Optional


class SceneState:
    """Tracks the render and vision-check state for a single scene.

    All mutation is explicit; no hidden state outside this object.
    """

    # Valid terminal status strings (checked in render_scene.py assertions).
    STATUSES = frozenset(
        {"COMPLETED", "COMPLETED_WITH_FLAGS", "ABORTED", "FAILED_FILESYSTEM"}
    )

    def __init__(self, scene_label: str, output_dir: str) -> None:
        """Initialise state for *scene_label* writing output to *output_dir*.

        Args:
            scene_label: Human-readable label, e.g. ``Act.1-Scene.5-Beach``.
            output_dir:  Absolute path to the per-scene render output directory.
        """
        self.scene_label: str = scene_label
        self.output_dir: str = output_dir
        self.start_time: float = time.monotonic()

        self.frames_rendered: int = 0
        self.frames_expected: int = 0  # set by caller before loop starts

        # Per-check records: list of dicts with structured fields.
        # Keys: frame, category, disposition, reason, justification,
        #       justification_reason.
        self._checks: List[Dict[str, Any]] = []

        self._consecutive_fails: int = 0
        self.vision_fails_total: int = 0
        self.pass_with_note_total: int = 0

        # Terminal status — set exactly once, at the end of a scene.
        self.status: str | None = None

    # ------------------------------------------------------------------
    # Mutation helpers
    # ------------------------------------------------------------------

    def record_frame(self, frame_number: int) -> None:
        """Increment the rendered-frame counter.

        Call once per frame immediately after ``bpy.ops.render.render()``
        returns successfully.

        Args:
            frame_number: Blender frame number that was just rendered.
        """
        self.frames_rendered += 1

    def record_check(
        self,
        frame_number: int,
        verdict: str,
        reason: str,
        *,
        category: Optional[str] = None,
        disposition: Optional[str] = None,
        justification: Optional[str] = None,
        justification_reason: Optional[str] = None,
    ) -> None:
        """Record the outcome of a single vision check.

        Supports both the legacy binary API (verdict = "PASS" or "FAIL") and
        the structured issue-#3 API (category + disposition).  When both are
        supplied, the structured fields take precedence for history and log
        output.

        Consecutive-fail counter logic:
            - PASS or PASS_WITH_NOTE disposition → reset counter.
            - FAIL disposition → increment counter.
        If *disposition* is not supplied, falls back to *verdict* ("PASS" → reset,
        anything else → increment).

        Args:
            frame_number:        Blender frame number that was checked.
            verdict:             Legacy ``"PASS"`` or ``"FAIL"`` verdict (kept for
                                 backward compat; ignored when *disposition* is set).
            reason:              One-sentence raw reason from step-1 (empty on PASS).
            category:            Step-1 category token (e.g. ``"FAIL_BLACK"``).
            disposition:         Final disposition after step-2: ``"PASS"``,
                                 ``"PASS_WITH_NOTE"``, or ``"FAIL"``.
            justification:       ``"JUSTIFIED"``, ``"CONFIRMED_FAIL"``,
                                 ``"SKIPPED (disabled)"``, or ``"—"`` when step-2
                                 was not run.
            justification_reason: One-sentence reason from step-2, or empty.
        """
        effective_disposition = disposition if disposition is not None else verdict

        entry: Dict[str, Any] = {
            "frame": frame_number,
            # Structured fields (issue #3).
            "category": category if category is not None else verdict,
            "disposition": effective_disposition,
            "reason": reason,
            "justification": justification if justification is not None else "—",
            "justification_reason": justification_reason or "",
            # Legacy fields preserved for callers that only use old API.
            "verdict": verdict,
        }
        self._checks.append(entry)

        if effective_disposition in ("PASS", "PASS_WITH_NOTE"):
            self._consecutive_fails = 0
            if effective_disposition == "PASS_WITH_NOTE":
                self.pass_with_note_total += 1
        else:
            self._consecutive_fails += 1
            self.vision_fails_total += 1

    def consecutive_fails(self) -> int:
        """Return the current run of consecutive vision FAILs.

        Resets to 0 on the next PASS or PASS_WITH_NOTE recorded via
        :meth:`record_check`.

        Returns:
            Non-negative integer count.
        """
        return self._consecutive_fails

    def reset_consecutive_fails(self) -> None:
        """Manually reset the consecutive-fail counter to zero.

        Normally not needed — :meth:`record_check` resets it on PASS.  Exposed
        for callers that want to clear mid-scene after manual intervention.
        """
        self._consecutive_fails = 0

    def frame_history(self, max: int = 5) -> List[str]:
        """Return the last *max* sample-frame entries formatted for the
        step-2 justification prompt's ``{frame_history_summary}`` placeholder.

        Format per entry::

            frame {N}: {disposition} ({category})

        Examples::

            frame 1: PASS_WITH_NOTE (FAIL_BLACK)
            frame 24: PASS (PASS)
            frame 48: PASS_WITH_NOTE (FAIL_NO_CHARACTERS)

        Args:
            max: Maximum number of entries to return.  Caps at 5 by default to
                 bound prompt length.  Pass a different value only in tests.

        Returns:
            List of formatted strings, chronological order (oldest first),
            length <= *max*.
        """
        tail = self._checks[-max:] if len(self._checks) > max else list(self._checks)
        return [
            f"frame {entry['frame']}: {entry['disposition']} ({entry['category']})"
            for entry in tail
        ]

    def finalise(self, status: str) -> None:
        """Set the terminal status for this scene.

        Args:
            status: One of the strings in :attr:`STATUSES`.

        Raises:
            ValueError: If *status* is not a recognised value.
        """
        if status not in self.STATUSES:
            raise ValueError(
                f"Unknown status {status!r}. Must be one of {sorted(self.STATUSES)}."
            )
        self.status = status

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_log_entry(self) -> Dict[str, Any]:
        """Return a JSON-serialisable dict for appending to render_log.jsonl.

        Includes all fields needed for the aggregate report, including the
        issue-#3 pass_with_note count for the artist-facing summary.

        Returns:
            Dict with keys:
            ``scene_label``, ``frames_rendered``, ``frames_expected``,
            ``vision_checks_made``, ``vision_fails``, ``pass_with_note``,
            ``status``, ``elapsed_seconds``, ``checks`` (full per-check list).
        """
        return {
            "scene_label": self.scene_label,
            "frames_rendered": self.frames_rendered,
            "frames_expected": self.frames_expected,
            "vision_checks_made": len(self._checks),
            "vision_fails": self.vision_fails_total,
            "pass_with_note": self.pass_with_note_total,
            "status": self.status,
            "elapsed_seconds": round(time.monotonic() - self.start_time, 2),
            "checks": list(self._checks),
        }

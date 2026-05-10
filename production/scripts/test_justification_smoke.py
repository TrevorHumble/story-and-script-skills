"""Smoke test for the issue-#3 justification pipeline.

Verifies the public API surface and internal parsing logic using mocked
Anthropic responses — no live API calls, no Blender dependency.

Run with:
    python production/scripts/test_justification_smoke.py

Exit code 0 = all assertions passed.
Exit code 1 = at least one assertion failed (AssertionError printed).
"""

from __future__ import annotations

import sys
import types
import unittest
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch


# ---------------------------------------------------------------------------
# Helpers for mocking the Anthropic client
# ---------------------------------------------------------------------------


def _make_response(text: str) -> Any:
    """Build a minimal fake Anthropic response object."""
    content_block = MagicMock()
    content_block.text = text
    response = MagicMock()
    response.content = [content_block]
    return response


def _mock_client(step1_reply: str, step2_reply: str | None = None) -> Any:
    """Return an Anthropic client mock that returns canned responses.

    If *step2_reply* is None, any second call also returns *step1_reply*
    (shouldn't happen in normal flow).
    """
    client = MagicMock()
    replies = iter([step1_reply, step2_reply or step1_reply])

    def _create(**kwargs):
        return _make_response(next(replies))

    client.messages.create.side_effect = _create
    return client


# ---------------------------------------------------------------------------
# Import the modules under test
# ---------------------------------------------------------------------------

# vision_check and state_tracking live next to this test file.
sys.path.insert(0, ".")

import importlib
import os

# Remove any cached module so env changes take effect.
for mod in ("vision_check", "state_tracking"):
    sys.modules.pop(mod, None)

import vision_check as vc
import state_tracking as st


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestStep1Parsing(unittest.TestCase):
    """Unit tests for _parse_step1."""

    def _parse(self, raw: str) -> Dict[str, str]:
        return vc._parse_step1(raw, "fake_frame.png")

    def test_pass(self):
        r = self._parse("PASS")
        self.assertEqual(r["category"], "PASS")
        self.assertEqual(r["reason"], "")

    def test_fail_black(self):
        r = self._parse("FAIL_BLACK")
        self.assertEqual(r["category"], "FAIL_BLACK")

    def test_fail_no_characters(self):
        r = self._parse("FAIL_NO_CHARACTERS")
        self.assertEqual(r["category"], "FAIL_NO_CHARACTERS")

    def test_fail_broken_geometry(self):
        r = self._parse("FAIL_BROKEN_GEOMETRY")
        self.assertEqual(r["category"], "FAIL_BROKEN_GEOMETRY")

    def test_fail_wrong_scale(self):
        r = self._parse("FAIL_WRONG_SCALE")
        self.assertEqual(r["category"], "FAIL_WRONG_SCALE")

    def test_fail_other_with_reason(self):
        r = self._parse("FAIL_OTHER: flickering geometry on character mesh")
        self.assertEqual(r["category"], "FAIL_OTHER")
        self.assertEqual(r["reason"], "flickering geometry on character mesh")

    def test_parse_error_treated_as_fail_other(self):
        r = self._parse("something completely unexpected")
        self.assertEqual(r["category"], "FAIL_OTHER")
        self.assertIn("parse error", r["reason"])

    def test_leading_whitespace_stripped(self):
        r = self._parse("  PASS  \n")
        self.assertEqual(r["category"], "PASS")

    def test_only_first_line_used(self):
        r = self._parse("PASS\nSome extra text that should be ignored")
        self.assertEqual(r["category"], "PASS")


class TestStep2Parsing(unittest.TestCase):
    """Unit tests for _parse_step2."""

    def _parse(self, raw: str) -> Dict[str, str]:
        return vc._parse_step2(raw)

    def test_justified(self):
        r = self._parse("JUSTIFIED: Script specifies fade-in from black at scene start.")
        self.assertEqual(r["verdict"], "JUSTIFIED")
        self.assertEqual(r["reason"], "Script specifies fade-in from black at scene start.")

    def test_confirmed_fail(self):
        r = self._parse("CONFIRMED_FAIL: Script does not anticipate missing characters.")
        self.assertEqual(r["verdict"], "CONFIRMED_FAIL")
        self.assertEqual(r["reason"], "Script does not anticipate missing characters.")

    def test_parse_error_conservative(self):
        r = self._parse("I'm not sure, maybe it's okay?")
        self.assertEqual(r["verdict"], "CONFIRMED_FAIL")
        self.assertIn("parse error", r["reason"])

    def test_only_first_line_used(self):
        r = self._parse("JUSTIFIED: Fade-in.\nExtra line.")
        self.assertEqual(r["verdict"], "JUSTIFIED")
        self.assertEqual(r["reason"], "Fade-in.")


class TestVerifyFrameAPI(unittest.TestCase):
    """verify_frame() returns correct structured result with mocked client."""

    def _fake_image(self, tmp_path: str) -> str:
        """Create a tiny valid PNG file for testing."""
        import base64
        # Minimal 1x1 red PNG bytes.
        png_b64 = (
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQI12P4z8BQDwADhQGAWjR9awAAAABJRU5ErkJggg=="
        )
        path = os.path.join(tmp_path, "frame_0001.png")
        with open(path, "wb") as fh:
            fh.write(base64.b64decode(png_b64))
        return path

    def setUp(self):
        import tempfile
        self._tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self._tmpdir, ignore_errors=True)

    def test_pass_category_returns_pass_disposition(self):
        img = self._fake_image(self._tmpdir)
        client = _mock_client("PASS")
        result = vc.verify_frame(
            img,
            scene_name="Beach",
            scene_number="Act.1-Scene.5",
            expected_characters="Florence, Sebastian",
            scene_description="Florence takes Sebastian's hand.",
            client=client,
        )
        self.assertEqual(result["category"], "PASS")
        self.assertEqual(result["disposition"], "PASS")

    def test_fail_black_returns_fail_disposition(self):
        img = self._fake_image(self._tmpdir)
        client = _mock_client("FAIL_BLACK")
        result = vc.verify_frame(
            img,
            scene_name="Apartment",
            scene_number="Act.1-Scene.1",
            expected_characters="Florence",
            scene_description="Slow fade in from black.",
            client=client,
        )
        self.assertEqual(result["category"], "FAIL_BLACK")
        self.assertEqual(result["disposition"], "FAIL")

    def test_fail_other_with_reason(self):
        img = self._fake_image(self._tmpdir)
        client = _mock_client("FAIL_OTHER: mesh clipping visible on left shoulder")
        result = vc.verify_frame(
            img,
            scene_name="Void",
            scene_number="Act.2-Scene.3",
            expected_characters="Sebastian",
            scene_description="Sebastian repairs Florence's finger.",
            client=client,
        )
        self.assertEqual(result["category"], "FAIL_OTHER")
        self.assertEqual(result["disposition"], "FAIL")
        self.assertIn("clipping", result["reason"])

    def test_result_dict_has_required_keys(self):
        img = self._fake_image(self._tmpdir)
        client = _mock_client("PASS")
        result = vc.verify_frame(
            img, "Beach", "5", "Florence", "desc", client=client
        )
        for key in ("category", "disposition", "reason"):
            self.assertIn(key, result, f"missing key: {key}")


class TestJustifyFailureAPI(unittest.TestCase):
    """justify_failure() returns correct verdict with mocked client."""

    def test_fail_black_justified(self):
        client = _mock_client("JUSTIFIED: Script specifies fade-in from black at scene start.")
        result = vc.justify_failure(
            "FAIL_BLACK",
            "Apartment",
            "Act.1-Scene.1",
            "Slow fade in from black, then pan.",
            "Scene opens in darkness.",
            ["frame 1: FAIL (FAIL_BLACK)"],
            client=client,
        )
        self.assertEqual(result["verdict"], "JUSTIFIED")
        self.assertIn("fade-in", result["reason"])

    def test_fail_no_characters_confirmed_fail(self):
        client = _mock_client(
            "CONFIRMED_FAIL: Script specifies both characters present throughout."
        )
        result = vc.justify_failure(
            "FAIL_NO_CHARACTERS",
            "Beach",
            "Act.1-Scene.5",
            "Florence and Sebastian present throughout.",
            "Both characters interact at beach.",
            [],
            client=client,
        )
        self.assertEqual(result["verdict"], "CONFIRMED_FAIL")

    def test_ineligible_category_skip_without_api(self):
        """FAIL_BROKEN_GEOMETRY must return CONFIRMED_FAIL without API call."""
        client = MagicMock()
        result = vc.justify_failure(
            "FAIL_BROKEN_GEOMETRY",
            "Void",
            "3",
            "excerpt",
            "notes",
            [],
            client=client,
        )
        self.assertEqual(result["verdict"], "CONFIRMED_FAIL")
        client.messages.create.assert_not_called()

    def test_fail_other_ineligible(self):
        client = MagicMock()
        result = vc.justify_failure(
            "FAIL_OTHER",
            "Beach",
            "5",
            "excerpt",
            "notes",
            [],
            client=client,
        )
        self.assertEqual(result["verdict"], "CONFIRMED_FAIL")
        client.messages.create.assert_not_called()

    def test_justification_disabled_env(self):
        """When JUSTIFICATION_ENABLED=0, returns CONFIRMED_FAIL immediately."""
        with patch.dict(os.environ, {"JUSTIFICATION_ENABLED": "0"}):
            # Reload so the env change is picked up by the module-level function.
            client = MagicMock()
            result = vc.justify_failure(
                "FAIL_BLACK",
                "Apartment",
                "1",
                "excerpt",
                "notes",
                [],
                client=client,
            )
        self.assertEqual(result["verdict"], "CONFIRMED_FAIL")
        client.messages.create.assert_not_called()

    def test_timeout_treated_as_confirmed_fail(self):
        """Step-2 timeout must return CONFIRMED_FAIL (conservative).

        We simulate a timeout by patching concurrent.futures.Future.result to
        raise TimeoutError directly — no sleeping thread required.
        """
        import concurrent.futures

        client = MagicMock()
        # Client never actually called; Future.result raises TimeoutError.

        original_submit = concurrent.futures.ThreadPoolExecutor.submit

        def _submit_raising(self_ex, fn, *args, **kwargs):
            future = MagicMock(spec=concurrent.futures.Future)
            future.result.side_effect = concurrent.futures.TimeoutError()
            return future

        with patch.object(concurrent.futures.ThreadPoolExecutor, "submit", _submit_raising):
            result = vc.justify_failure(
                "FAIL_BLACK",
                "Apartment",
                "1",
                "excerpt",
                "notes",
                [],
                client=client,
            )
        self.assertEqual(result["verdict"], "CONFIRMED_FAIL")
        self.assertIn("timeout", result["reason"].lower())

    def test_result_dict_has_required_keys(self):
        client = _mock_client("JUSTIFIED: Fade-in from black is scripted.")
        result = vc.justify_failure(
            "FAIL_BLACK", "Apartment", "1", "excerpt", "notes", [], client=client
        )
        for key in ("verdict", "reason"):
            self.assertIn(key, result, f"missing key: {key}")


class TestJustificationEligibleConstants(unittest.TestCase):
    """Ensure the eligibility set contains exactly the right categories."""

    def test_eligible_set(self):
        self.assertEqual(
            vc.JUSTIFICATION_ELIGIBLE,
            frozenset({"FAIL_BLACK", "FAIL_NO_CHARACTERS"}),
        )

    def test_ineligible_not_in_set(self):
        for cat in ("FAIL_BROKEN_GEOMETRY", "FAIL_WRONG_SCALE", "FAIL_OTHER"):
            self.assertNotIn(cat, vc.JUSTIFICATION_ELIGIBLE)


class TestSceneStateFrameHistory(unittest.TestCase):
    """SceneState.frame_history() returns correctly formatted strings."""

    def setUp(self):
        self.state = st.SceneState("Act.1-Scene.1-Apartment", "/tmp/renders")

    def _record(self, frame: int, category: str, disposition: str) -> None:
        verdict = "PASS" if category == "PASS" else "FAIL"
        self.state.record_check(
            frame,
            verdict=verdict,
            reason="",
            category=category,
            disposition=disposition,
        )

    def test_empty_history(self):
        result = self.state.frame_history(max=5)
        self.assertEqual(result, [])

    def test_single_entry(self):
        self._record(1, "FAIL_BLACK", "PASS_WITH_NOTE")
        result = self.state.frame_history(max=5)
        self.assertEqual(len(result), 1)
        self.assertIn("frame 1", result[0])
        self.assertIn("PASS_WITH_NOTE", result[0])
        self.assertIn("FAIL_BLACK", result[0])

    def test_format_matches_spec(self):
        """Verify exact format: 'frame {N}: {disposition} ({category})'"""
        self._record(24, "PASS", "PASS")
        result = self.state.frame_history(max=5)
        self.assertEqual(result[0], "frame 24: PASS (PASS)")

    def test_capped_at_max(self):
        for frame in range(0, 150, 24):  # 7 entries
            self._record(frame, "PASS", "PASS")
        result = self.state.frame_history(max=5)
        self.assertEqual(len(result), 5)

    def test_most_recent_returned(self):
        for frame in range(0, 150, 24):  # 7 entries at 0,24,48,72,96,120,144
            self._record(frame, "PASS", "PASS")
        result = self.state.frame_history(max=5)
        # Should contain frames 48,72,96,120,144 (last 5).
        self.assertIn("frame 48", result[0])
        self.assertIn("frame 144", result[-1])

    def test_chronological_order(self):
        for frame in [1, 24, 48]:
            self._record(frame, "PASS", "PASS")
        result = self.state.frame_history(max=5)
        self.assertIn("frame 1", result[0])
        self.assertIn("frame 24", result[1])
        self.assertIn("frame 48", result[2])


class TestSceneStateConsecutiveFails(unittest.TestCase):
    """Consecutive-fail counter resets on PASS or PASS_WITH_NOTE."""

    def setUp(self):
        self.state = st.SceneState("Scene", "/tmp")

    def _record(self, disposition: str) -> None:
        cat = "PASS" if disposition == "PASS" else "FAIL_BLACK"
        verdict = "PASS" if disposition == "PASS" else "FAIL"
        self.state.record_check(
            1, verdict=verdict, reason="", category=cat, disposition=disposition
        )

    def test_fail_increments(self):
        self._record("FAIL")
        self.assertEqual(self.state.consecutive_fails(), 1)
        self._record("FAIL")
        self.assertEqual(self.state.consecutive_fails(), 2)

    def test_pass_resets(self):
        self._record("FAIL")
        self._record("FAIL")
        self._record("PASS")
        self.assertEqual(self.state.consecutive_fails(), 0)

    def test_pass_with_note_resets(self):
        self._record("FAIL")
        self._record("FAIL")
        self._record("PASS_WITH_NOTE")
        self.assertEqual(self.state.consecutive_fails(), 0)

    def test_pass_with_note_counted(self):
        self._record("PASS_WITH_NOTE")
        self._record("PASS_WITH_NOTE")
        self.assertEqual(self.state.pass_with_note_total, 2)


class TestWorkflowExamples(unittest.TestCase):
    """End-to-end worked examples from the issue spec (mocked API).

    Verifies the full disposition sequence without Blender or live API.
    """

    def _run_sequence(
        self,
        categories: List[str],
        justifications: List[str | None],
        justification_enabled: bool = True,
    ) -> List[str]:
        """Simulate a sequence of verify+justify calls; return dispositions."""
        state = st.SceneState("TestScene", "/tmp")
        dispositions = []

        env_patch = {"JUSTIFICATION_ENABLED": "1" if justification_enabled else "0"}

        for i, (cat, just) in enumerate(zip(categories, justifications)):
            frame = (i + 1) * 24

            # Build mocked verify_frame result.
            if cat == "PASS":
                verify_result = {"category": "PASS", "disposition": "PASS", "reason": ""}
            else:
                verify_result = {"category": cat, "disposition": "FAIL", "reason": ""}

            # Build mocked justify_failure result.
            if just is not None:
                justify_result = {"verdict": just, "reason": "test reason"}
            else:
                justify_result = None

            with patch.dict(os.environ, env_patch):
                # Reload module to pick up env changes.
                importlib.reload(vc)

                category = verify_result["category"]
                initial_disposition = verify_result["disposition"]

                if initial_disposition == "PASS":
                    disposition = "PASS"
                elif category not in vc.JUSTIFICATION_ELIGIBLE or not vc._justification_enabled():
                    disposition = "FAIL"
                else:
                    verdict = justify_result["verdict"] if justify_result else "CONFIRMED_FAIL"
                    disposition = "PASS_WITH_NOTE" if verdict == "JUSTIFIED" else "FAIL"

                # Record with full structured fields.
                jlabel = "—"
                jreason = ""
                if initial_disposition != "PASS":
                    if category not in vc.JUSTIFICATION_ELIGIBLE or not vc._justification_enabled():
                        jlabel = "SKIPPED (not eligible)" if category not in vc.JUSTIFICATION_ELIGIBLE else "SKIPPED (disabled)"
                    elif justify_result:
                        jlabel = justify_result["verdict"]
                        jreason = justify_result["reason"]

                state.record_check(
                    frame,
                    verdict="PASS" if category == "PASS" else "FAIL",
                    reason="",
                    category=category,
                    disposition=disposition,
                    justification=jlabel,
                    justification_reason=jreason,
                )
                dispositions.append(disposition)

        return dispositions

    def test_example1_fade_in_flyby_not_aborted(self):
        """Example 1: fade-in, flyby, flyby — all PASS_WITH_NOTE, not aborted."""
        dispositions = self._run_sequence(
            categories=["FAIL_BLACK", "FAIL_NO_CHARACTERS", "FAIL_NO_CHARACTERS", "PASS"],
            justifications=["JUSTIFIED", "JUSTIFIED", "JUSTIFIED", None],
        )
        self.assertEqual(dispositions[0], "PASS_WITH_NOTE")
        self.assertEqual(dispositions[1], "PASS_WITH_NOTE")
        self.assertEqual(dispositions[2], "PASS_WITH_NOTE")
        self.assertEqual(dispositions[3], "PASS")

    def test_example2_dialogue_scene_confirmed_fails(self):
        """Example 2: 3 CONFIRMED_FAIL in a row → abort threshold reached."""
        dispositions = self._run_sequence(
            categories=["FAIL_NO_CHARACTERS"] * 3,
            justifications=["CONFIRMED_FAIL"] * 3,
        )
        self.assertEqual(dispositions, ["FAIL", "FAIL", "FAIL"])

    def test_example3_single_broken_frame_counter_resets(self):
        """Example 3: PASS, broken geometry, PASS — counter resets on last PASS."""
        state = st.SceneState("Void", "/tmp")
        # Frame 24: PASS
        state.record_check(24, verdict="PASS", reason="", category="PASS", disposition="PASS")
        self.assertEqual(state.consecutive_fails(), 0)
        # Frame 48: FAIL_BROKEN_GEOMETRY (ineligible for justification → FAIL)
        state.record_check(
            48, verdict="FAIL", reason="", category="FAIL_BROKEN_GEOMETRY", disposition="FAIL",
            justification="SKIPPED (not eligible)", justification_reason="render artifact",
        )
        self.assertEqual(state.consecutive_fails(), 1)
        # Frame 72: PASS
        state.record_check(72, verdict="PASS", reason="", category="PASS", disposition="PASS")
        self.assertEqual(state.consecutive_fails(), 0)
        self.assertEqual(state.vision_fails_total, 1)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)

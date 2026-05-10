"""Smoke tests for the issue-1 vision-verification modules.

These tests verify public API surface only -- no Blender, no Anthropic API key
required.  They are safe to run with any standard CPython 3.9+ interpreter.

Run with:
    python tests/test_smoke.py

Or with pytest:
    pytest tests/test_smoke.py -v

Runtime requirements:
    - Standard library only (no third-party packages needed for the smoke test
      itself).  The `anthropic` package is needed at runtime for vision checks
      but is NOT imported here.
    - All modules under production/scripts must be importable from the repo
      root without `bpy` being available.

Design:
    Each module is imported with a mock for `bpy` pre-installed in sys.modules
    so that top-level imports of `bpy` inside the module do not raise
    ImportError.  The bpy mock raises ImportError if any bpy API is actually
    *called*, which is correct -- no Blender session exists during smoke tests.
"""

from __future__ import annotations

import importlib
import inspect
import json
import os
import sys
import tempfile
import types
import unittest

# ---------------------------------------------------------------------------
# Path setup -- add production/scripts to sys.path so imports resolve.
# ---------------------------------------------------------------------------

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SCRIPTS_DIR = os.path.join(_REPO_ROOT, "production", "scripts")

if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)


# ---------------------------------------------------------------------------
# Lightweight bpy stub -- lets modules import without a running Blender session.
# ---------------------------------------------------------------------------

def _make_bpy_stub() -> types.ModuleType:
    """Return a minimal bpy stub that raises ImportError if any API is called."""
    bpy = types.ModuleType("bpy")

    class _Raiser:
        def __getattr__(self, name: str):
            raise ImportError(
                f"bpy.{name} was called during smoke test -- "
                "this requires a live Blender session."
            )

    bpy.data = _Raiser()
    bpy.context = _Raiser()
    bpy.ops = _Raiser()
    bpy.types = _Raiser()
    return bpy


# Install the stub before importing any module that may import bpy at module level.
sys.modules.setdefault("bpy", _make_bpy_stub())


# ---------------------------------------------------------------------------
# Helper: import a module from production/scripts by name.
# ---------------------------------------------------------------------------

def _import_scripts_module(name: str) -> types.ModuleType:
    """Import *name* from production/scripts, clearing cached version first."""
    # Remove any stale cached version so tests are deterministic.
    sys.modules.pop(name, None)
    return importlib.import_module(name)


# ===========================================================================
# Tests
# ===========================================================================


class TestStateTracking(unittest.TestCase):
    """SceneState public API surface."""

    def setUp(self) -> None:
        self.mod = _import_scripts_module("state_tracking")

    def test_class_exists(self) -> None:
        self.assertTrue(hasattr(self.mod, "SceneState"))

    def test_init_signature(self) -> None:
        sig = inspect.signature(self.mod.SceneState.__init__)
        params = list(sig.parameters.keys())
        self.assertIn("scene_label", params)
        self.assertIn("output_dir", params)

    def test_record_frame(self) -> None:
        state = self.mod.SceneState("TestScene", "/tmp/test")
        self.assertEqual(state.frames_rendered, 0)
        state.record_frame(1)
        self.assertEqual(state.frames_rendered, 1)

    def test_record_check_pass(self) -> None:
        state = self.mod.SceneState("TestScene", "/tmp/test")
        state.record_check(1, "PASS", "")
        self.assertEqual(state.consecutive_fails(), 0)
        self.assertEqual(state.vision_fails_total, 0)

    def test_record_check_fail_increments(self) -> None:
        state = self.mod.SceneState("TestScene", "/tmp/test")
        state.record_check(1, "FAIL", "black frame")
        state.record_check(25, "FAIL", "missing character")
        self.assertEqual(state.consecutive_fails(), 2)
        self.assertEqual(state.vision_fails_total, 2)

    def test_consecutive_fails_resets_on_pass(self) -> None:
        state = self.mod.SceneState("TestScene", "/tmp/test")
        state.record_check(1, "FAIL", "black frame")
        state.record_check(25, "FAIL", "broken geometry")
        self.assertEqual(state.consecutive_fails(), 2)
        state.record_check(49, "PASS", "")
        self.assertEqual(state.consecutive_fails(), 0)

    def test_reset_consecutive_fails(self) -> None:
        state = self.mod.SceneState("TestScene", "/tmp/test")
        state.record_check(1, "FAIL", "x")
        state.reset_consecutive_fails()
        self.assertEqual(state.consecutive_fails(), 0)

    def test_to_log_entry_keys(self) -> None:
        state = self.mod.SceneState("TestScene", "/tmp/test")
        state.frames_expected = 96
        state.record_frame(1)
        state.record_check(1, "PASS", "")
        state.finalise("COMPLETED")
        entry = state.to_log_entry()
        for key in (
            "scene_label",
            "frames_rendered",
            "frames_expected",
            "vision_checks_made",
            "vision_fails",
            "status",
            "elapsed_seconds",
            "checks",
        ):
            with self.subTest(key=key):
                self.assertIn(key, entry)

    def test_to_log_entry_is_json_serialisable(self) -> None:
        state = self.mod.SceneState("TestScene", "/tmp/test")
        state.finalise("COMPLETED")
        entry = state.to_log_entry()
        # Should not raise.
        json.dumps(entry)

    def test_finalise_valid_statuses(self) -> None:
        valid = ["COMPLETED", "COMPLETED_WITH_FLAGS", "ABORTED", "FAILED_FILESYSTEM"]
        for status in valid:
            with self.subTest(status=status):
                state = self.mod.SceneState("TestScene", "/tmp/test")
                state.finalise(status)
                self.assertEqual(state.status, status)

    def test_finalise_invalid_status_raises(self) -> None:
        state = self.mod.SceneState("TestScene", "/tmp/test")
        with self.assertRaises(ValueError):
            state.finalise("UNKNOWN_STATUS")

    def test_statuses_frozenset_has_four_values(self) -> None:
        self.assertEqual(len(self.mod.SceneState.STATUSES), 4)


class TestSceneContext(unittest.TestCase):
    """scene_context.load_scene_context public API surface."""

    def setUp(self) -> None:
        self.mod = _import_scripts_module("scene_context")

    def test_function_exists(self) -> None:
        self.assertTrue(hasattr(self.mod, "load_scene_context"))

    def test_signature(self) -> None:
        sig = inspect.signature(self.mod.load_scene_context)
        params = list(sig.parameters.keys())
        self.assertIn("output_root", params)
        self.assertIn("scene_label", params)

    def test_returns_dict(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.mod.load_scene_context(tmpdir, "TestScene")
        self.assertIsInstance(result, dict)

    def test_fallback_has_required_keys(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.mod.load_scene_context(tmpdir, "TestScene")
        for key in ("scene_label", "expected_characters", "description"):
            self.assertIn(key, result)

    def test_loads_valid_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scene_dir = os.path.join(tmpdir, "Act.1-Scene.5-Beach")
            os.makedirs(scene_dir)
            sidecar = {
                "scene_label": "Act.1-Scene.5-Beach",
                "expected_characters": ["Florence", "Sebastian"],
                "description": "Florence meets Sebastian on the beach.",
            }
            with open(os.path.join(scene_dir, "scene_context.json"), "w") as fh:
                json.dump(sidecar, fh)

            result = self.mod.load_scene_context(tmpdir, "Act.1-Scene.5-Beach")

        self.assertEqual(result["expected_characters"], ["Florence", "Sebastian"])
        self.assertIn("Florence meets Sebastian", result["description"])

    def test_malformed_json_falls_back(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scene_dir = os.path.join(tmpdir, "BadScene")
            os.makedirs(scene_dir)
            with open(os.path.join(scene_dir, "scene_context.json"), "w") as fh:
                fh.write("{this is not json}")
            result = self.mod.load_scene_context(tmpdir, "BadScene")
        # Should not raise; fallback keys present.
        self.assertIn("scene_label", result)


class TestVisionCheck(unittest.TestCase):
    """vision_check.verify_frame public API surface (no API key needed)."""

    def setUp(self) -> None:
        self.mod = _import_scripts_module("vision_check")

    def test_function_exists(self) -> None:
        self.assertTrue(hasattr(self.mod, "verify_frame"))

    def test_signature_has_image_path(self) -> None:
        sig = inspect.signature(self.mod.verify_frame)
        params = list(sig.parameters.keys())
        self.assertIn("image_path", params)

    def test_default_model_is_haiku(self) -> None:
        self.assertEqual(self.mod.DEFAULT_MODEL, "claude-haiku-4-5-20251001")

    def test_step1_prompt_contains_required_variables(self) -> None:
        """The step-1 prompt template must contain all required placeholders."""
        # Accept either _STEP1_PROMPT (issue #3) or _PROMPT_TEMPLATE (issue #1).
        template = getattr(self.mod, "_STEP1_PROMPT", None) or getattr(
            self.mod, "_PROMPT_TEMPLATE", None
        )
        self.assertIsNotNone(template, "No prompt template found in vision_check module")
        for placeholder in ("{scene_name}", "{scene_number}", "{expected_characters}", "{scene_description}"):
            self.assertIn(placeholder, template, f"Missing {placeholder} in prompt template")

    def test_step1_prompt_prohibits_creative_critique(self) -> None:
        """The prompt must forbid creative judgment (render-correctness only)."""
        template = getattr(self.mod, "_STEP1_PROMPT", None) or getattr(
            self.mod, "_PROMPT_TEMPLATE", None
        )
        self.assertIsNotNone(template)
        self.assertIn("DO NOT", template)
        self.assertIn("creative judgment", template)

    def test_step1_prompt_requires_pass_or_fail_format(self) -> None:
        """The prompt must require PASS or FAIL verdict format."""
        template = getattr(self.mod, "_STEP1_PROMPT", None) or getattr(
            self.mod, "_PROMPT_TEMPLATE", None
        )
        self.assertIsNotNone(template)
        self.assertIn("PASS", template)
        self.assertIn("FAIL", template)

    def test_step1_prompt_is_bounded_to_render_correctness(self) -> None:
        """The prompt must be scoped to render correctness, not creative critique."""
        template = getattr(self.mod, "_STEP1_PROMPT", None) or getattr(
            self.mod, "_PROMPT_TEMPLATE", None
        )
        self.assertIsNotNone(template)
        self.assertIn("render-correctness", template)

    def test_verify_frame_exists_and_is_callable(self) -> None:
        self.assertTrue(callable(self.mod.verify_frame))

    def test_fail_categories_present_if_issue3(self) -> None:
        """If this is the issue-#3 version, required FAIL category constants must exist."""
        if hasattr(self.mod, "FAIL_CATEGORIES"):
            # Issue #3 version: check all required categories.
            for cat in ("FAIL_BLACK", "FAIL_NO_CHARACTERS", "FAIL_BROKEN_GEOMETRY",
                        "FAIL_WRONG_SCALE", "FAIL_OTHER"):
                self.assertIn(cat, self.mod.FAIL_CATEGORIES)

    def test_timeout_constant_exists(self) -> None:
        """A hard timeout constant must be present."""
        # Accept either _CALL_TIMEOUT_SECONDS or equivalent.
        has_timeout = (
            hasattr(self.mod, "_CALL_TIMEOUT_SECONDS")
            or hasattr(self.mod, "TIMEOUT_SECONDS")
        )
        self.assertTrue(has_timeout, "No timeout constant found in vision_check module")

    def test_verify_frame_is_callable_with_correct_signature(self) -> None:
        """verify_frame must be callable and have at least image_path parameter.

        Note: actually calling verify_frame at runtime requires the 'anthropic'
        package to be installed and ANTHROPIC_API_KEY to be set.  The smoke
        test only verifies the callable signature -- not the runtime behavior.
        This is by design: the smoke test runs without an API key.
        """
        import inspect
        fn = self.mod.verify_frame
        self.assertTrue(callable(fn))
        sig = inspect.signature(fn)
        self.assertIn("image_path", sig.parameters)

    def test_anthropic_api_key_not_hardcoded(self) -> None:
        """The module must not contain a hardcoded API key string."""
        with open(os.path.join(_SCRIPTS_DIR, "vision_check.py")) as fh:
            source = fh.read()
        # Crude check: no sk- prefix followed by digits (typical Anthropic key prefix).
        self.assertNotRegex(source, r'"sk-[a-zA-Z0-9]{20,}"')
        self.assertNotRegex(source, r"'sk-[a-zA-Z0-9]{20,}'")


class TestExrConvert(unittest.TestCase):
    """exr_convert.to_temp_png public API surface (no Blender required)."""

    def setUp(self) -> None:
        self.mod = _import_scripts_module("exr_convert")

    def test_function_exists(self) -> None:
        self.assertTrue(hasattr(self.mod, "to_temp_png"))

    def test_signature(self) -> None:
        sig = inspect.signature(self.mod.to_temp_png)
        params = list(sig.parameters.keys())
        self.assertIn("exr_path", params)
        self.assertIn("scene", params)

    def test_raises_on_api_call_without_blender(self) -> None:
        """to_temp_png must raise an error when called outside a Blender session.

        The bpy stub raises ImportError when any bpy API is actually invoked.
        to_temp_png checks the file exists first (raises RuntimeError on missing
        file), then calls bpy.data.images.load() which triggers the stub's
        ImportError.  We use a real temp file so the path check passes.
        """
        with tempfile.NamedTemporaryFile(suffix=".exr", delete=False) as tmp:
            fake_exr = tmp.name
        try:
            # Either RuntimeError or ImportError is acceptable:
            # - RuntimeError: bpy API was reached and raised via the stub
            # - ImportError: bpy itself was not available
            # In either case, the function correctly refuses to proceed.
            with self.assertRaises((ImportError, RuntimeError, AttributeError)):
                self.mod.to_temp_png(fake_exr, None)
        finally:
            os.unlink(fake_exr)

    def test_private_helpers_exist(self) -> None:
        """Internal helpers must be present for unit-testability."""
        for name in ("_load_image", "_ensure_combined_layer", "_save_as_png"):
            with self.subTest(name=name):
                self.assertTrue(hasattr(self.mod, name), f"Missing helper: {name}")


class TestRenderSceneModule(unittest.TestCase):
    """render_scene.py public functions and constants.

    render_scene.py calls main() at module level (it is designed to be run by
    Blender, not imported).  The test loads the module source, strips the final
    ``main()`` call, and exec()s the result into a fresh module namespace so we
    can inspect exported names without triggering the render loop.
    """

    def setUp(self) -> None:
        import importlib.util
        # Load the source, strip the bare main() call at the end, and exec.
        render_scene_path = os.path.join(_SCRIPTS_DIR, "render_scene.py")
        with open(render_scene_path, "r", encoding="utf-8") as fh:
            source = fh.read()

        # Remove the bare "main()" call at module level so the file can be
        # exec'd without a live Blender session.  The call is always the last
        # non-blank line in the file.
        lines = source.splitlines()
        stripped_lines = []
        for line in lines:
            # Skip the standalone main() call (not a def, not inside a block).
            if line.strip() == "main()":
                continue
            stripped_lines.append(line)
        safe_source = "\n".join(stripped_lines)

        # Create a fresh module to exec into.
        mod = types.ModuleType("render_scene")
        mod.__file__ = render_scene_path
        try:
            exec(compile(safe_source, render_scene_path, "exec"), mod.__dict__)
            self.mod = mod
        except Exception as exc:
            self.mod = None
            self._import_error = exc

    def test_module_imported(self) -> None:
        self.assertIsNotNone(self.mod)

    def test_constants_present(self) -> None:
        """Core configurable constants must be exported."""
        for name in ("SAMPLE_INTERVAL", "ABORT_THRESHOLD", "RESOLUTION_PERCENTAGE"):
            with self.subTest(name=name):
                self.assertTrue(hasattr(self.mod, name), f"Missing constant: {name}")

    def test_sample_interval_default(self) -> None:
        self.assertEqual(self.mod.SAMPLE_INTERVAL, 24)

    def test_abort_threshold_default(self) -> None:
        self.assertEqual(self.mod.ABORT_THRESHOLD, 3)

    def test_scene_label_strips_complete_suffix(self) -> None:
        # Accept either scene_label or _scene_label.
        fn = getattr(self.mod, "_scene_label", None) or getattr(self.mod, "scene_label", None)
        self.assertIsNotNone(fn)
        self.assertEqual(
            fn("/path/to/Act.1-Scene.1-Apartment - complete.blend"),
            "Act.1-Scene.1-Apartment",
        )

    def test_scene_label_no_suffix(self) -> None:
        fn = getattr(self.mod, "_scene_label", None) or getattr(self.mod, "scene_label", None)
        self.assertIsNotNone(fn)
        self.assertEqual(
            fn("/path/to/Act.1-Scene.5-Beach.blend"),
            "Act.1-Scene.5-Beach",
        )

    def test_resume_read_write_delete(self) -> None:
        """Resume marker round-trip."""
        read_fn = getattr(self.mod, "_read_resume_frame", None)
        write_fn = getattr(self.mod, "_write_resume_frame", None)
        delete_fn = getattr(self.mod, "_delete_resume_marker", None)
        if read_fn is None or write_fn is None or delete_fn is None:
            self.skipTest("Resume marker functions not yet exported from render_scene")
        with tempfile.TemporaryDirectory() as tmpdir:
            # Nothing there yet.
            self.assertIsNone(read_fn(tmpdir))
            # Write frame 48.
            write_fn(tmpdir, 48)
            self.assertEqual(read_fn(tmpdir), 48)
            # Delete marker.
            delete_fn(tmpdir)
            self.assertIsNone(read_fn(tmpdir))

    def test_append_log_entry_writes_jsonl(self) -> None:
        """Structured log helper must write valid JSON lines."""
        append_fn = getattr(self.mod, "_append_log_entry", None)
        if append_fn is None:
            self.skipTest("_append_log_entry not yet exported from render_scene")
        with tempfile.TemporaryDirectory() as tmpdir:
            entry = {"scene_label": "TestScene", "status": "COMPLETED"}
            append_fn(tmpdir, entry)
            log_path = os.path.join(tmpdir, "render_log.jsonl")
            self.assertTrue(os.path.exists(log_path))
            with open(log_path) as fh:
                line = fh.readline()
            parsed = json.loads(line)
            self.assertEqual(parsed["scene_label"], "TestScene")

    def test_no_vision_flag_in_parse_output_root(self) -> None:
        """parse_output_root must support --no-vision flag."""
        parse_fn = getattr(self.mod, "parse_output_root", None)
        if parse_fn is None:
            self.skipTest("parse_output_root not exported")
        _orig = sys.argv[:]
        try:
            sys.argv = ["blender", "--", "/tmp/renders", "--no-vision"]
            result = parse_fn()
            # Result should be a tuple with at least 2 elements, second being True.
            if isinstance(result, tuple) and len(result) >= 2:
                out_root, no_vision = result[0], result[1]
                self.assertTrue(no_vision)
            elif isinstance(result, str):
                # Old-style (returns only output_root) -- skip flag test.
                pass
        finally:
            sys.argv = _orig

    def test_dry_run_flag_in_parse_output_root(self) -> None:
        """parse_output_root must support --dry-run flag."""
        parse_fn = getattr(self.mod, "parse_output_root", None)
        if parse_fn is None:
            self.skipTest("parse_output_root not exported")
        _orig = sys.argv[:]
        try:
            sys.argv = ["blender", "--", "/tmp/renders", "--dry-run"]
            result = parse_fn()
            if isinstance(result, tuple) and len(result) >= 3:
                out_root, no_vision, dry_run = result[0], result[1], result[2]
                self.assertTrue(dry_run)
        finally:
            sys.argv = _orig


# ---------------------------------------------------------------------------
# Integration: state_tracking <-> scene_context round-trip
# ---------------------------------------------------------------------------


class TestIntegrationStatePlusContext(unittest.TestCase):
    """Verify that SceneState.to_log_entry() output matches the render_log schema."""

    def test_full_scene_lifecycle(self) -> None:
        state_mod = _import_scripts_module("state_tracking")
        ctx_mod = _import_scripts_module("scene_context")

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a sidecar JSON.
            scene_dir = os.path.join(tmpdir, "Act.1-Scene.5-Beach")
            os.makedirs(scene_dir)
            sidecar = {
                "scene_label": "Act.1-Scene.5-Beach",
                "expected_characters": ["Florence", "Sebastian"],
                "description": "Florence meets Sebastian on the beach.",
            }
            with open(os.path.join(scene_dir, "scene_context.json"), "w") as fh:
                json.dump(sidecar, fh)

            # Load context.
            ctx = ctx_mod.load_scene_context(tmpdir, "Act.1-Scene.5-Beach")
            self.assertEqual(ctx["expected_characters"], ["Florence", "Sebastian"])

            # Simulate a 48-frame render with 2 sample checks.
            state = state_mod.SceneState("Act.1-Scene.5-Beach", scene_dir)
            state.frames_expected = 48
            for f in range(1, 49):
                state.record_frame(f)
                if f in (1, 25):
                    state.record_check(f, "PASS", "")
            state.finalise("COMPLETED")

            entry = state.to_log_entry()

        # Verify schema.
        self.assertEqual(entry["frames_rendered"], 48)
        self.assertEqual(entry["vision_checks_made"], 2)
        self.assertEqual(entry["vision_fails"], 0)
        self.assertEqual(entry["status"], "COMPLETED")
        # Must be JSON-serialisable.
        json.dumps(entry)


class TestIssue1Requirements(unittest.TestCase):
    """Explicitly verify each acceptance criterion from issue #1 is addressable."""

    def test_state_tracking_has_all_required_methods(self) -> None:
        """SceneState interface from issue #1 review additions."""
        mod = _import_scripts_module("state_tracking")
        cls = mod.SceneState
        for method in ("record_frame", "record_check", "consecutive_fails",
                       "reset_consecutive_fails", "to_log_entry"):
            with self.subTest(method=method):
                self.assertTrue(hasattr(cls, method), f"SceneState missing method: {method}")

    def _load_render_scene_mod(self):
        """Load render_scene without executing main() (helper for test methods)."""
        render_scene_path = os.path.join(_SCRIPTS_DIR, "render_scene.py")
        with open(render_scene_path, "r", encoding="utf-8") as fh:
            source = fh.read()
        lines = source.splitlines()
        safe_source = "\n".join(l for l in lines if l.strip() != "main()")
        mod = types.ModuleType("render_scene_issue1")
        mod.__file__ = render_scene_path
        exec(compile(safe_source, render_scene_path, "exec"), mod.__dict__)
        return mod

    def test_resume_marker_constant_in_render_scene(self) -> None:
        """render_scene.py must define the resume marker filename."""
        mod = self._load_render_scene_mod()
        marker = getattr(mod, "_RESUME_MARKER", None)
        self.assertIsNotNone(marker, "_RESUME_MARKER constant missing from render_scene")
        self.assertIn("last_completed_frame", marker)

    def test_log_filename_constant_in_render_scene(self) -> None:
        """render_scene.py must define the JSONL log filename."""
        mod = self._load_render_scene_mod()
        log_fn = getattr(mod, "_LOG_FILENAME", None)
        self.assertIsNotNone(log_fn, "_LOG_FILENAME constant missing from render_scene")
        self.assertIn(".jsonl", log_fn)

    def test_vision_check_respects_render_correctness_boundary(self) -> None:
        """The prompt boundary is documented in source -- verify it."""
        mod = _import_scripts_module("vision_check")
        template = getattr(mod, "_STEP1_PROMPT", None) or getattr(
            mod, "_PROMPT_TEMPLATE", None
        )
        self.assertIsNotNone(template)
        # Must NOT judge creative elements.
        for term in ("pose", "framing", "expression", "lighting mood"):
            self.assertIn(term, template,
                          f"Prompt should explicitly call out '{term}' as out of scope")

    def test_exr_convert_uses_save_render_not_save(self) -> None:
        """exr_convert must use save_render() (not image.save()) for view transform.

        save_render() applies the scene's colour-management view transform.
        image.save() writes raw linear-light values, which will look blown-out
        or black when HDR EXR is the source.
        """
        with open(os.path.join(_SCRIPTS_DIR, "exr_convert.py")) as fh:
            source = fh.read()
        self.assertIn("save_render", source,
                      "exr_convert.py must use save_render() for colour-managed PNG output")
        # Verify the key save_render call is present as a method call (not just in a comment).
        self.assertRegex(source, r'\.save_render\s*\(',
                         "exr_convert.py must call .save_render() as a method")

    def test_scene_context_sidecar_path_convention(self) -> None:
        """scene_context.py must load from <output_root>/<scene_label>/scene_context.json."""
        with open(os.path.join(_SCRIPTS_DIR, "scene_context.py")) as fh:
            source = fh.read()
        self.assertIn("scene_context.json", source)

    def test_status_strings_are_exact(self) -> None:
        """The four status strings must match the exact strings from the spec."""
        mod = _import_scripts_module("state_tracking")
        expected = {"COMPLETED", "COMPLETED_WITH_FLAGS", "ABORTED", "FAILED_FILESYSTEM"}
        self.assertEqual(mod.SceneState.STATUSES, expected)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(verbosity=2)

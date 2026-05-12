# Changelog

All notable changes to this pipeline are tracked here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows [SemVer](https://semver.org/).

## [Unreleased]

## [4.0.0] — 2026-05-12

### Changed
- **Analysis reorganized into 5 phases** (was 4). Skills regrouped by craft dimension:
  - **Phase 1 — Foundation** (01–05): unchanged
  - **Phase 2 — Narrative Arc** (06–08): plot architecture, split from old "Character & Conflict"
  - **Phase 3 — Character** (09–13): character analysis, split from old "Character & Conflict"
  - **Phase 4 — Scene Craft** (14–23): merged old "Structure & Pacing" + dialogue skills from "Dialogue & Surface"
  - **Phase 5 — Synthesis** (24 + FigJam): postmortem and beat board, split from old "Dialogue & Surface"
- **Orchestrators co-located with skills.** Each phase is now a numbered folder (`01_foundation/`, `02_narrative_arc/`, etc.) containing its `orchestrator.md` alongside its skill files. Replaces the flat `analysis/skills/` directory.
- **Parent orchestrator added** (`analysis/pipeline.md`): ties together all five phases, documents phase dependencies, cross-phase re-run instructions, and single-phase entry.
- **FigJam build instructions** moved from dialogue orchestrator to `analysis/05_synthesis/orchestrator.md` where they belong — the beat board is a pipeline-wide deliverable, not a dialogue artifact.

### Removed
- `analysis/foundation.md`, `analysis/character.md`, `analysis/structure_pacing.md`, `analysis/dialogue.md` — replaced by phase-folder orchestrators.
- `analysis/skills/` flat directory — skills now live in their phase folders.

## [3.0.0] — 2026-05-11

### Changed
- **Pipeline restructured into independent phases.** The monolithic `00_orchestrator.md` is replaced by phase-specific orchestrators, each focused on one dimension of craft. The writer works through one phase at a time, making decisions at each stop, and comes back later for the next.
- **Analysis skills** moved from root into `analysis/skills/`. Four orchestrators in `analysis/`: `foundation.md` (skills 01–05), `character.md` (skills 06–13), `structure_pacing.md` (skills 14–17), `dialogue.md` (skills 18–24 + FigJam build).
- **Scene scaffolding** moved from `production/` into its own `scaffolding/` folder with a dedicated orchestrator.
- **Render & Assembly** (Production Skill 02) moved to [TrevorHumble/Blender-Skills](https://github.com/TrevorHumble/Blender-Skills). It's a Blender rendering operation, not a story analysis step. Scripts (`render_scene.py`, `render_all.sh`, `assemble_vse.py`) moved with it. Issues #1–4, #6 transferred.
- **Shared infrastructure** extracted into `common.md` — agent spawning rules, OUTPUT STYLE block, show-don't-tell, director's notes lifecycle, decisions log protocol, re-run dependency map. Every orchestrator reads it first.
- **Repo renamed** from `story-and-script-skills` to `story-pipeline`.

### Added
- `analysis/README.md` — analysis phase overview with pipeline philosophy.
- `scaffolding/README.md` — scaffolding phase overview.
- Cross-phase re-run instructions in `common.md`.
- Each orchestrator has a "Where you left off" prerequisite check and a "Handoff" section naming what comes next.
- Each phase is independently runnable — bring your own script for analysis, bring your own FigJam board for scaffolding.

### Removed
- `00_orchestrator.md` — content split across `common.md` and the phase orchestrators.
- `production/` folder — contents relocated to `scaffolding/` and Blender-Skills.

### Notes
- This is a breaking restructure. All file paths changed. Git history preserved via `git mv`.
- v2.x orchestrator and skill content is preserved in git history (commits prior to v3.0.0).

## [2.4.0] — 2026-05-10

### Changed
- **Render output folder structure** is now pass-isolated: `<project>/renders/<pass_type>/<pass_instance>/<scene_label>/`. Pass types: `animatic`, `lookdev`, `final`, `dailies`. Pass instance format: `<YYYY-MM-DD>_<version>_<engine>_<resolution>[_<note>]`. Multiple render passes (animatic v1, v2, lookdev, final) can coexist without overwriting each other.
- **`render_scene.py` no longer overrides the saved engine.** Previous version had `ENGINE = "BLENDER_EEVEE_NEXT"` hardcoded that force-set the engine before every render. v2.4.0: default behavior respects the engine saved in the .blend file. Optional `--engine <NAME>` CLI arg overrides explicitly with logged confirmation.

### Added
- `_meta.json` schema written to each pass instance with engine, resolution, scene list, render times, vision-check summary.
- Production Skill 02 v2.4.0 doc section on the new folder structure and engine policy with the lesson encoded: *scripts that silently override saved settings cause hard-to-diagnose bugs.*

### Fixed
- **Engine-override bug discovered during 2026-05-09 first render.** Artist requested Workbench animatic; script silently rendered EEVEE. Bug confirmed by render time (3 sec/frame is EEVEE territory at 540p, not Workbench) and visual identification by the artist. Python checks via `bpy.context.scene.render.engine` returned BLENDER_WORKBENCH because the script didn't save after the override, so post-render inspection showed the saved value, not the in-memory render-time value.

### Notes
- Issue #4 tracks the actual `render_scene.py` and `render_all.sh` code changes. Issues #1/#2/#3 (vision verification, SMS notifications, justification chain) build on the v2.4.0 foundation and are tracked as separate implementation work.
- This is a breaking change to the render output path. The 2026-05-09 first-run renders were migrated into the new structure as `renders/animatic/2026-05-10_v1_eevee_540p/` (note: `eevee` reflects the actual engine used due to the bug, not the intended Workbench).

## [2.3.0] — 2026-05-09

### Added
- **Mid-render Haiku 4.5 vision verification** added to Production Skill 02. Every 24th frame (configurable) is sampled to a vision LLM that flags render-correctness problems (black frames, missing characters, broken geometry). 3 consecutive vision failures abort the scene, save remaining render time for other scenes.
- **EXR auto-conversion to temp PNG** for sample frames only. Full EXR sequences are preserved untouched for downstream compositing. Conversion uses Blender's native `bpy.data.images.save_render()` with the scene's color management view transform applied (handles HDR tonemap into 8-bit PNG).
- **New CI-3.5 check-in** — artist reviews vision-flagged or aborted scenes before continuing.
- **Two-tier failure handling**:
  - Structural failure (file-system) = STOP whole run
  - Vision failure = MARK SCENE FAILED, CONTINUE to next (could be false positive)
  - Vision abort (3 in a row) = ABORT this scene's render, MARK ABORTED, CONTINUE
- **Architectural change**: rendering primitive is now a Python frame-by-frame loop instead of `bpy.ops.render.render(animation=True)`. Enables mid-render verification, clean cancellation, and resume-from-frame-N.
- **Failure modes table expanded** with vision-check-specific failures (prompt drifted into creative critique, EXR conversion lost data, multilayer EXR wrong active layer, repeated API timeouts).

### Notes
- v2.3.0 of Production Skill 02 describes the *design*. The deterministic Python implementation is tracked as a separate GitHub issue.
- Vision supervisor is bounded to render correctness only. The boundary against creative critique is paper-worthy and explicitly defended in the skill's Standards and Teaching Moment.

## [2.2.0] — 2026-05-09

### Added
- **`production/02_render_and_assembly.md`** — sequential per-scene headless rendering with verification, then Blender VSE assembly into the final video deliverable. Five formal user check-ins (pre-flight, settings-lock, mid-render, pre-assembly, watch-v1). Compositing is explicitly deferred — animatic uses Workbench engine which needs no comp; final film compositing belongs in a future Production Skill 03.
- Skill written first-time-run thorough: detailed failure-mode table, rationale for sequential-not-parallel rendering, explicit boundary defenses against in-skill compositing or audio work.

### Notes
- This skill is theoretical until run end-to-end on Catalysis (target: Thursday/Friday this week). It will be revised with real-world findings after first execution.

## [2.1.0] — 2026-05-09

### Added
- **`production/`** — first production-side skill set. Skills that come *after* the McKee analysis pipeline ends, taking canonical artifacts (director's notes, postmortem, FigJam beat board) and turning them into the files an artist actually opens to start animating.
- **`production/01_scene_scaffolding.md`** — reading the FigJam beat board and the director's notes, then creating one Blender scene file per beat with characters appended at default offset positions.
- **`production/scripts/`** — reference implementations:
  - `inspect_character.py` — recon a character `.blend` for collection/object names
  - `append_characters.py` — parameterized character collection append
  - `offset_characters.py` — translate appended collections to avoid overlap
  - `render_scene.py` — per-scene headless render
  - `render_all.sh` — batch wrapper for full-film headless render
  - `assemble_vse.py` — stitch rendered sequences into a Blender VSE timeline

### Notes
- The production skill set is growing alongside an in-progress short film case study. Future skills (pose blocking aids, render queue management, sound design integration) will land as production stages are validated against real work.
- Same design principles as the analysis skills apply — show-don't-tell, test before batching, mechanical operations only.

## [2.0.0] — 2026-05-09

Major rewrite of the orchestrator and skills based on lessons from the first full pipeline run (Catalysis short film).

### Added
- **`templates/intake_template.md`** — one-page brief filled before kickoff (genre, format, logline, working title, authorial intent, constraints).
- **`templates/directors_notes_template.md`** — initialized at intake; the canonical staging document agents read as authorial truth.
- **`templates/decisions_log_template.md`** — structured chronological log of decisions made at pit stops and check-ins.
- **`templates/lessons_template.md`** — cross-project craft principles distilled from analysis runs.
- **Show-don't-tell rule** in the orchestrator: director's notes describe what the staging *is*, not what it's *meant to achieve*; agents infer intent from the work itself.
- **Pin `model: "opus"`** required on every Agent call (pins Opus 4.6 regardless of parent conversation).
- **Output style block** inserted into every agent prompt: concise prose, define McKee jargon in plain English on first use, 4-part teaching moment structure, scene-specific problems and suggestions.
- **Re-run protocol**: dependency map specifying which downstream skills must rerun when a director's notes change affects an upstream skill.
- **Final artifact: FigJam beat board** built by the orchestrator after Skill 24 — three columns (suggestions / beats / removed), color-coded cards, derived from the postmortem and director's notes.
- **Cross-skill contradictions** as a required section in Skill 24 (was implicit in v1).
- **Surface problems, don't auto-propose solutions** rule for orchestrator reporting back to the user.

### Changed
- **All 24 skills slimmed** to a standardized template (Purpose, Inputs, Instructions, Output, plus a single reference to the orchestrator's output-style requirements).
- **`00_orchestrator.md`** rewritten as the master skill, including intake step, lifecycle for director's notes, stop protocols, decisions-log integration, re-run protocol, and FigJam build step.
- Per-skill teaching moments now follow the 4-part structure (plain English / why it matters / how it operates here / takeaway).

### Notes
- v1 skills are preserved in git history (commit prior to v2.0.0).

## [1.0.0] — initial release

Original 24-skill McKee story analysis pipeline plus orchestrator. Per-script analysis kept local via `.gitignore`.

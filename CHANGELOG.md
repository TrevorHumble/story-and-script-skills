# Changelog

All notable changes to this pipeline are tracked here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows [SemVer](https://semver.org/).

## [Unreleased]

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

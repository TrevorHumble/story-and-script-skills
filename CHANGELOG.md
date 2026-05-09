# Changelog

All notable changes to this pipeline are tracked here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows [SemVer](https://semver.org/).

## [Unreleased]

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

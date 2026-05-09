# Story and Script Skills

A 24-skill Robert McKee story analysis pipeline for screenplays. Agents run sequentially through structure, character, dialogue, and rhythm, then synthesize a postmortem and (in v2) a FigJam beat board.

## How it works

`00_orchestrator.md` is the master skill — it spawns one agent per skill, in order, against your screenplay. Each agent reads its inputs from a staging folder, follows its skill's instructions, and writes an output file. Stop protocols (pit stops, one-pager summaries, check-ins) bring the user into the loop at meaningful checkpoints.

The 24 skills cover, in order:

1. Genre Contract — what the audience is promised
2. Controlling Idea — the one-sentence argument the climax makes
3. Story Spine — the scene-by-scene throughline
4. Image System — recurring visuals carrying argument
5. Act Structure — proportions, turning points
6. Inciting Incident — what disturbs the protagonist's life
7. Complications — escalating obstacles
8. Crisis — the dilemma
9. Conflict Levels — inner / personal / extra-personal
10. True Character — what's revealed under pressure
11. Character Dimension — contradictions
12. Antagonism — opposing forces
13. Negation of the Negation — thematic depth
14. Subplot — secondary lines
15. Scene Values — turn-by-turn polarity
16. Rhythm — pacing and contrast
17. Gap — expectation vs. result
18. Text and Subtext — surface vs. underneath
19. Beat Analysis — gerunds in dialogue
20. On-the-Nose — direct dialogue diagnosis
21. Exposition — information as ammunition
22. Said / Unsaid / Unsayable — inner life
23. Trialogue — third-element technique
24. Postmortem — synthesis and rewrite roadmap

## Required inputs

- `script.txt` — the screenplay
- `beat_sheet.txt` — beat-level summary

These files are gitignored by default (per-script content stays local).

## Status

**v2.0.0 — current.** Standardized output style across all skills, intake step, formal director's notes lifecycle, structured decisions log, re-run protocol with dependency map, FigJam board built automatically after the postmortem. See `CHANGELOG.md` for details. v1 is preserved in git history.

## Quick start

1. Drop `script.txt` and `beat_sheet.txt` in the project root.
2. Copy `templates/intake_template.md` to `intake.md` and fill it in.
3. Copy `templates/directors_notes_template.md` to `directors_notes.md` (carry over the Authorial Intent line from intake).
4. Copy `templates/decisions_log_template.md` to `decisions_log.md`.
5. Open `00_orchestrator.md` — it tells you everything else.

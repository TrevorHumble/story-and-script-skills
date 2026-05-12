# Analysis Phase 1 — Foundation (Skills 01–05)

> Phase 1 of 5 in the [Analysis Pipeline](../pipeline.md). You can run this phase independently if you have the prerequisites below, or as the first phase of a full pipeline run.

This phase establishes what the story is *about*: the genre contract with the audience, the controlling idea, the protagonist's through-line, the visual motifs, and the act structure. Every downstream phase builds on decisions made here.

---

## Read first

Read [`common.md`](../../common.md) before proceeding. It contains agent spawning rules, the OUTPUT STYLE block, show-don't-tell staging rules, and the director's notes / decisions log lifecycle.

---

## Required setup before kickoff

Project root must contain:

1. `script.txt` — the screenplay
2. `beat_sheet.txt` — beat-level summary of the script
3. `intake.md` — filled from `templates/intake_template.md`
4. `directors_notes.md` — initialized from `templates/directors_notes_template.md` (Authorial Intent section copied from intake)
5. `decisions_log.md` — initialized from `templates/decisions_log_template.md`
6. `outputs/` directory — where all skill outputs land

If any of these are missing, halt and ask the user. Do not begin Skill 01 with partial setup.

---

## Skills

| # | Skill | Inputs | Stop |
|---|---|---|---|
| 01 | [Genre Contract](01_genre_contract.md) | script, beat_sheet, intake | |
| 02 | [Controlling Idea](02_controlling_idea.md) | script, 01 | **Pit stop** |
| 03 | [Story Spine](03_story_spine.md) | script, 02 | |
| 04 | [Image System](04_image_system.md) | script, 02, 03 | **One-pager** |
| 05 | [Act Structure](05_act_structure.md) | script, beat_sheet, 02, 03 | **Pit stop** |

---

## Stop protocols

### After Skill 02 — Pit stop: Controlling Idea

The controlling idea is the one-sentence argument the climax makes. Everything downstream depends on it. Confirm the sentence before continuing.

### After Skill 04 — One-pager

Brief summary of skills 01–04 findings. Surface what's working, what's contradictory, what's unresolved. Save as `outputs/summary_after_04.md`.

### After Skill 05 — Pit stop: Act Structure

Confirm act proportions and turning points. These are the structural pillars the narrative arc and character analysis will build on.

---

## Handoff

After this phase completes, the following artifacts exist:

- `outputs/01_genre_contract.md` through `outputs/05_act_structure.md`
- `outputs/summary_after_04.md`
- `directors_notes.md` — updated with decisions from this phase's stops
- `decisions_log.md` — updated

**Next phase:** [Narrative Arc](../02_narrative_arc/orchestrator.md) — how the story's events escalate.

# Analysis Phase 4 — Scene Craft (Skills 14–23)

> Phase 4 of 5 in the [Analysis Pipeline](../pipeline.md). You can run this phase independently if you have the prerequisites below, or after the [Character](../03_character/orchestrator.md) phase.

This phase examines how individual scenes work — first the architecture (subplot design, polarity turns, rhythm, gaps between expectation and result), then the dialogue mechanics (subtext, beats, over-direct lines, exposition delivery, the inner life characters can't express, the third-element technique).

---

## Read first

Read [`common.md`](../../common.md) before proceeding.

---

## Where you left off

The following must exist before starting this phase:

| Prerequisite | Produced by |
|---|---|
| `script.txt`, `beat_sheet.txt` | User setup |
| `outputs/02_controlling_idea.md` | [Foundation](../01_foundation/orchestrator.md) — Skill 02 |
| `outputs/05_act_structure.md` | [Foundation](../01_foundation/orchestrator.md) — Skill 05 |
| `outputs/11_character_dimension.md` | [Character](../03_character/orchestrator.md) — Skill 11 |
| `outputs/13_negation.md` | [Character](../03_character/orchestrator.md) — Skill 13 |
| `directors_notes.md` | Updated through Character phase |
| `decisions_log.md` | Updated through Character phase |

If any are missing, halt and tell the user which prerequisite is absent.

---

## Scene Architecture (Skills 14–17)

| # | Skill | Inputs | Stop |
|---|---|---|---|
| 14 | [Subplot](14_subplot.md) | script, 02, 05, 13 | |
| 15 | [Scene Values](15_scene_values.md) | script, beat_sheet, 02 | **Pit stop** |
| 16 | [Rhythm](16_rhythm.md) | script, beat_sheet, 05, 15 | |
| 17 | [Gap](17_gap.md) | script, 15 | **Check-in** |

---

## Dialogue Mechanics (Skills 18–23)

| # | Skill | Inputs | Stop |
|---|---|---|---|
| 18 | [Text and Subtext](18_text_subtext.md) | script, 15, 17 | |
| 19 | [Beat Analysis](19_beat_analysis.md) | script, 15 | |
| 20 | [On-the-Nose](20_on_the_nose.md) | script, 19 | **One-pager** |
| 21 | [Exposition](21_exposition.md) | script, 19, 20 | |
| 22 | [Said / Unsaid / Unsayable](22_said_unsaid.md) | script, 11, 19 | |
| 23 | [Trialogue](23_trialogue.md) | script, 20, 22 | |

---

## Stop protocols

### After Skill 15 — Pit stop: Scene Values

*Scene value* is the polarity charge of a scene — the state that shifts from positive to negative (or vice versa) within a single scene. Confirm the scene-by-scene polarity map before rhythm and gap analysis, which both depend on it.

### After Skill 17 — Check-in

Lighter touch than a pit stop. Surface the biggest open problems from the scene architecture analysis. The writer decides which to act on before moving to dialogue mechanics.

### After Skill 20 — One-pager

Brief summary of skills 14–20 findings. Save as `outputs/summary_after_20.md`.

---

## Handoff

After this phase completes:

- `outputs/14_subplot.md` through `outputs/23_trialogue.md`
- `outputs/summary_after_20.md`
- `directors_notes.md` — updated
- `decisions_log.md` — updated

**Next phase:** [Synthesis](../05_synthesis/orchestrator.md) — postmortem and FigJam beat board.

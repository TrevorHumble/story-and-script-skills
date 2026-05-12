# Analysis Phase 4 — Dialogue & Surface (Skills 18–24)

> Part of the [Story Pipeline](../README.md). You can run this phase independently if you have the prerequisites below, or after the [Structure & Pacing](structure_pacing.md) phase.

This phase examines how dialogue carries (or fails to carry) everything established in the first three phases: the subtext beneath the surface, the action-layer of each beat, where dialogue is too direct, how exposition is delivered, the inner life characters can't express, and the third-element technique. The phase ends with a full synthesis postmortem and a FigJam beat board.

---

## Read first

Read [`common.md`](../common.md) before proceeding.

---

## Where you left off

The following must exist before starting this phase:

| Prerequisite | Produced by |
|---|---|
| `script.txt`, `beat_sheet.txt` | User setup |
| `outputs/11_character_dimension.md` | [Character & Conflict](character.md) — Skill 11 |
| `outputs/15_scene_values.md` | [Structure & Pacing](structure_pacing.md) — Skill 15 |
| `outputs/17_gap.md` | [Structure & Pacing](structure_pacing.md) — Skill 17 |
| `directors_notes.md` | Updated through Structure & Pacing phase |
| `decisions_log.md` | Updated through Structure & Pacing phase |

If any are missing, halt and tell the user which prerequisite is absent.

---

## Skills

| # | Skill | Inputs | Stop |
|---|---|---|---|
| 18 | [Text and Subtext](skills/18_text_subtext.md) | script, 15, 17 | |
| 19 | [Beat Analysis](skills/19_beat_analysis.md) | script, 15 | |
| 20 | [On-the-Nose](skills/20_on_the_nose.md) | script, 19 | **One-pager** |
| 21 | [Exposition](skills/21_exposition.md) | script, 19, 20 | |
| 22 | [Said / Unsaid / Unsayable](skills/22_said_unsaid.md) | script, 11, 19 | |
| 23 | [Trialogue](skills/23_trialogue.md) | script, 20, 22 | |
| 24 | [Postmortem](skills/24_postmortem.md) | all 23 outputs + summaries + script + beat_sheet + directors_notes | **Final + FigJam build** |

---

## Stop protocols

### After Skill 20 — One-pager

Brief summary of skills 14–20 findings. Save as `outputs/summary_after_20.md`.

### After Skill 24 — Final: Postmortem + FigJam Beat Board

The postmortem synthesizes all 24 analyses into a prioritized action plan (Tier 1 foundational, Tier 2 scene-level, Tier 3 dialogue). After the postmortem, build the FigJam beat board automatically — it is the single most useful artifact for the rewrite phase.

---

## FigJam beat board

### What it is

A three-column FigJam board:

- **LEFT — Suggestions Not Yet Taken**: every open problem from `postmortem.md`, color-coded by tier (Tier 1 = orange, Tiers 2–3 = yellow). Each card carries the problem name, scene reference, and one-paragraph mechanical description.
- **MIDDLE — Beat Sheet (Restructured)**: every scene in the canonical restructured order from `directors_notes.md`, color-coded by status:
  - KEPT (green) — unchanged from page
  - CHANGED (blue) — revised; card describes what changed mechanically
  - NEW (pink) — added scene; card describes what's staged
  - Act dividers (`ACT ONE`, `ACT TWO`, `ACT THREE`) as headers between groups
- **RIGHT — Removed**: every scene/beat cut from the original draft, with the mechanical reason for the cut. Red cards.

Cards are draggable. Sections are draggable. Saves to Figma cloud (cross-device automatic).

### Build steps

1. Confirm `postmortem.md` and `directors_notes.md` exist in `outputs/`.
2. Call Figma `whoami` to get the user's planKey. If multiple plans exist and the user hasn't specified, ask which team.
3. Call Figma `create_new_file` with `editorType: "figjam"`, `fileName: "[Working Title] — Beat Board"`, and the planKey.
4. Call Figma `use_figma` with the file key and the population script. The script:
   - Loads Inter Regular / Medium / Bold fonts
   - Creates three sections (Suggestions Not Yet Taken / Beat Sheet — Restructured / Removed)
   - For each card: `figma.createShapeWithText()`, `shapeType = 'ROUNDED_RECTANGLE'`, fill color per status, text = `${status}\n\n${title}\n\n${body}`, resize ~340x240
   - Stacks cards vertically inside each section with consistent spacing (gap ~40, header gap ~100)
   - Appends each card into its section via `section.appendChild(card)`
   - Calls `figma.viewport.scrollAndZoomIntoView(allNodes)` at the end
5. Return the FigJam URL to the user.

### Color palette (RGB 0–1)

| Status | Color | RGB |
|---|---|---|
| KEPT | light green | `{r: 0.74, g: 0.91, b: 0.74}` |
| CHANGED | light blue | `{r: 0.70, g: 0.85, b: 0.97}` |
| NEW | light pink | `{r: 1.00, g: 0.78, b: 0.91}` |
| REMOVED | red | `{r: 0.97, g: 0.65, b: 0.65}` |
| SUGGESTION-OPEN (T2/T3) | yellow | `{r: 1.00, g: 0.95, b: 0.55}` |
| TIER-1 urgent | orange | `{r: 1.00, g: 0.78, b: 0.40}` |

### Card content rules

- **Card title**: scene name + number (e.g., "8 — Ballroom") OR problem name for suggestions
- **Card body**: 1–3 sentences, mechanical description only (no value words, per the show-don't-tell rule)
- **Status tag** at the top of each card: `[KEPT]`, `[CHANGED]`, `[NEW]`, `[REMOVED]`, `[TIER 1 · OPEN]`, etc.

---

## Handoff

After this phase completes, the full analysis is done:

- `outputs/18_text_subtext.md` through `outputs/24_postmortem.md`
- `outputs/summary_after_20.md`
- `postmortem.md` — prioritized action plan
- FigJam beat board — the visual artifact for the rewrite
- `directors_notes.md` — final canonical staging
- `decisions_log.md` — complete decision history

**Next step:** [Scene Scaffolding](../scaffolding/orchestrator.md) — translating the beat board and director's notes into Blender scene files.

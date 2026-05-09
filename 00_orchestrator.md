# 00 — Orchestrator (v2)

The master skill. Spawns one agent per analysis skill, in order, against the screenplay. Manages staging, the director's notes lifecycle, stop protocols, the decisions log, and the final FigJam beat board.

This file is read by Claude (or any agent runner) at the start of a pipeline run. Follow it like a runbook.

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

## Agent spawning — the four non-negotiables

Every Agent call MUST:

1. **Use `subagent_type: "general-purpose"`**
2. **Pin `model: "opus"`** — pins Opus 4.6 regardless of the parent conversation's model. Without this, the agent inherits the parent's model and quality varies between runs.
3. **Include the OUTPUT STYLE block (below) verbatim** in the prompt
4. **Pass canonical staging from `directors_notes.md` as STAGING ONLY** — no intent or effect framing (see Show-Don't-Tell rule below)

Stage inputs into `outputs/staging/skill_NN/` before each call. Pass file paths in the prompt.

---

## OUTPUT STYLE block — paste verbatim into every agent prompt

```
## OUTPUT STYLE — required, non-negotiable

1. **Be concise.** Tight prose. Short sentences. Lead with the finding. No throat-clearing, no multi-clause hedging, no restating the question before answering.

2. **Define McKee jargon in plain English on first use.** When you first use a term like *controlling idea, true character, dimension, gap, beat, gerund, on-the-nose, the unsayable, scene value, negation of the negation, trialogue* — give a one-sentence plain-English definition first, then apply it. Don't assume the reader knows McKee.

3. **Teaching moment must follow this 4-part structure:**
   - **What this means in plain English** — define the principle without jargon
   - **Why it matters in any story** — the general craft reason
   - **How it operates in THIS script** — point at specific scenes/beats
   - **Takeaway for the writer** — one or two actionable sentences

4. **Problems and Suggestions: scene-specific and direct.** Each item starts with the scene name (and beat reference if relevant), names the issue in one sentence, then briefly explains the impact. Suggestions name a concrete intervention, not a vague direction.

5. **Internal reasoning can be loose. The OUTPUT DOCUMENT must be clean.** The user reads the output, not the chain of thought.
```

---

## Show-don't-tell — the rule that protects analysis integrity

When passing director's notes content into an agent prompt, **describe WHAT THE STAGING IS, not WHAT IT'S MEANT TO ACHIEVE.**

- ❌ "Sebastian's slow finger gesture is intended to feel intimate and to make Florence's permission visible as a chosen act."
- ✅ "Sebastian raises his thumb to Florence's lips. Holds. Eye contact. Florence's breathing visibly deepens. He slides his index finger in. He works the gum free."

**Why this matters.** Pre-loading intent corrupts analysis. An agent told "this is meant to feel intimate" will report back that it does — confirming the writer's hope rather than checking the page. An agent given only the staging will report what is actually legible.

**No value words** in agent-facing staging: avoid *powerful, intimate, rich, sophisticated, devastating, beautiful*, etc. Mechanical description only.

**No effect framing**: avoid *meant to, intended to, designed to, in order to, so that the audience...* The staging IS the intent; if it isn't legible, the staging needs to change.

The user-facing director's notes follow the same rule (see `templates/directors_notes_template.md`). The orchestrator passes excerpts straight through.

---

## Director's notes lifecycle

`directors_notes.md` is the canonical staging document. Treat it as authorial truth — it supersedes `script.txt` where they conflict.

**When to read it:** before staging inputs for any skill. The agent's understanding of "what's on the page" must include the directors_notes revisions.

**When to update it:** at every pit stop / one-pager / check-in where the user makes a staging decision. Append a new revision section using the template format (mechanical description + source citation). Do not delete superseded sections — mark them as superseded so history is visible.

**What goes in:** decided staging changes only. Open problems live in the "Open Problems" section at the bottom — surface them but don't propose solutions until the user decides.

**Source citation required.** Every revision section ends with `**Source:** [skill file or pit stop reference]`. This is how future-you traces why a decision was made.

---

## Stop protocols

Stops are where the user is brought into the loop. Do not skip them.

| After skill | Type | What happens |
|---|---|---|
| 02 — Controlling Idea | Pit stop | Confirm controlling idea sentence; this anchors everything downstream |
| 04 — Image System | One-pager | Brief summary of skills 01–04 findings |
| 05 — Act Structure | Pit stop | Confirm act proportions and turning points |
| 11 — Character Dimension | Pit stop | Confirm character dimensions before downstream dialogue analysis |
| 13 — Negation of the Negation | One-pager | Brief summary of skills 05–13 findings |
| 15 — Scene Values | Pit stop | Confirm scene-by-scene polarity before rhythm/gap analysis |
| 17 — Gap | Check-in | Lighter touch — surface biggest open problems |
| 20 — On-the-Nose | One-pager | Brief summary of skills 14–20 findings |
| 24 — Postmortem | Final | Synthesis + FigJam board build |

**At each stop:**
1. Surface findings from the recent skills (problems, contradictions, what's working)
2. Capture user decisions in `decisions_log.md`
3. Update `directors_notes.md` with any new staging changes
4. Confirm before continuing

---

## Decisions log

After each pit stop / check-in, append to `decisions_log.md`:

- **Quick table row** for every decision (date, skill/stop, decision, mechanical change, source)
- **Detailed entry** only when the table row can't carry the decision

The orchestrator does this; the user does not have to ask.

---

## Re-run protocol — dependency map

When a directors_notes change overturns an upstream finding, downstream skills may need to rerun. Use this map.

| If you change... | You must rerun... |
|---|---|
| Genre or controlling idea (01–02) | Everything from 03 onward |
| Story spine or act structure (03, 05) | 06–09, 14, 15, 16 |
| Inciting incident or crisis (06, 08) | 07, 15, 17 |
| Conflict levels or character dimension (09, 10, 11) | 12, 18, 19, 22 |
| Antagonism (12) | 14, 22, 23 |
| Subplot (14) | 15, 16, 17 |
| Scene values (15) | 16, 17, 18 |
| Any dialogue scene staging | 18, 19, 20, 21, 22, 23 |
| Final pass: any change | 24 (postmortem must rerun if anything earlier changed) |

Re-run individual skills with the same staging-folder pattern as the first run. Mark the re-run output with a `## Re-run notice` block citing what triggered it.

---

## Surface problems, don't auto-propose solutions

When reporting back to the user from agent outputs:

- **Surface the problems** the agent flagged — name the scene, the issue, the impact
- **Do NOT auto-propose the agent's suggested solution** unless the user asks
- The user is a thinking partner, not a passive consumer; let them see the problem before being handed a fix

The agent's output document still contains its suggestions — the user can read them. The orchestrator's user-facing report leads with problems.

---

## Final artifact: FigJam beat board

After Skill 24 completes, build the FigJam beat board automatically. Do not skip this — it is the single most useful artifact for the rewrite phase.

### What it is

A three-column FigJam board:

- **LEFT — Suggestions Not Yet Taken**: every open problem from `postmortem.md`, color-coded by tier (Tier 1 = orange, Tiers 2–3 = yellow). Each card carries the problem name, scene reference, and one-paragraph mechanical description.
- **MIDDLE — Beat Sheet (Restructured)**: every scene in the canonical restructured order from `directors_notes.md`, color-coded by status:
  - 🟢 KEPT (green) — unchanged from page
  - 🔵 CHANGED (blue) — revised; card describes what changed mechanically
  - 🩷 NEW (pink) — added scene; card describes what's staged
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
   - For each card: `figma.createShapeWithText()`, `shapeType = 'ROUNDED_RECTANGLE'`, fill color per status, text = `${status}\n\n${title}\n\n${body}`, resize ~340×240
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

## Skill list

| # | Skill | Inputs | Stops |
|---|---|---|---|
| 01 | Genre Contract | script, beat_sheet, intake | |
| 02 | Controlling Idea | script, 01 | **Pit stop** |
| 03 | Story Spine | script, beat_sheet, 02 | |
| 04 | Image System | script, 02, 03 | One-pager |
| 05 | Act Structure | script, beat_sheet, 03 | **Pit stop** |
| 06 | Inciting Incident | script, 03, 05 | |
| 07 | Complications | script, 05, 06 | |
| 08 | Crisis | script, 02, 05, 07 | |
| 09 | Conflict Levels | script, 02, 03 | |
| 10 | True Character | script, 02, 08, 09 | |
| 11 | Character Dimension | script, 09, 10 | **Pit stop** |
| 12 | Antagonism | script, 02, 09, 10, 11 | |
| 13 | Negation of the Negation | script, 02, 12 | One-pager |
| 14 | Subplot | script, 02, 03 | |
| 15 | Scene Values | script, beat_sheet, 03, 05 | **Pit stop** |
| 16 | Rhythm | script, beat_sheet, 05, 15 | |
| 17 | Gap | script, 15 | Check-in |
| 18 | Text and Subtext | script, 15, 17 | |
| 19 | Beat Analysis | script, 15 | |
| 20 | On-the-Nose | script, 19 | One-pager |
| 21 | Exposition | script, 19, 20 | |
| 22 | Said / Unsaid / Unsayable | script, 11, 19 | |
| 23 | Trialogue | script, 20, 22 | |
| 24 | Postmortem | all 23 outputs + summaries + script + beat_sheet + directors_notes | **Final + FigJam build** |

---

## Notes for the orchestrating agent

- **Confirm before destructive actions.** Re-runs that overwrite outputs need a one-line check with the user.
- **Don't summarize what the user can read.** When pointing the user at a finding, link the file and lead with the headline. The full detail is in the file.
- **Trust the staging folder pattern.** Every skill reads its inputs from `outputs/staging/skill_NN/`. Do not pass long quoted excerpts in the prompt when a file path will do.
- **Memory is your friend.** If you encounter feedback that should apply to future runs (output style, scope, tone), save it as a feedback memory.

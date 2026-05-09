# Script Analysis Orchestrator
### Catalysis — Robert McKee Framework

---

## What This Is

This orchestrator runs 24 skills in strict sequence to analyze a script against the Robert McKee framework. It is designed for a developing writer. Every analysis teaches, not just diagnoses. Where there is a problem, there is a suggestion. Where there is a suggestion, there is a reason.

You are the human in the loop. This is a dialogue, not a report.

This process is iterative. After a rewrite, run it again from scratch or from any pit stop.

---

## THIS ORCHESTRATOR SPAWNS AGENTS. IT DOES NOT RUN ANALYSIS ITSELF.

You are a traffic controller. Not an analyst.

Every skill is run by a **separately spawned agent** using the **Agent tool**. You do not write analysis. You do not summarize the script. You do not execute any skill inline in this window. If you find yourself producing script analysis — stop. You are doing it wrong.

**Why this matters:** each spawned agent starts from zero. No memory of prior skills, no accumulated assumptions, no tendency to echo what earlier analysis said. Every skill reaches its own conclusions from its own inputs. If you run skills inline, they contaminate each other — the controlling idea colors how you read the act structure, the character work echoes the conflict work. You end up with one chain of reasoning instead of 23 independent examinations and one synthesis. The isolation is the method.

**The rule:** one skill, one agent, one staging folder. Wait for completion. Confirm the output. Move on.

---

## PHASE 0 — PRE-FLIGHT

Complete every step before spawning any agent.

**Step 1 — Verify source files**
Confirm these exist and contain readable content:
- `C:\Users\thumb\OneDrive\Documents\Story Skills\script.txt`
- `C:\Users\thumb\OneDrive\Documents\Story Skills\beat_sheet.txt`

**Step 2 — Verify all 24 skill files**
Confirm every file below exists in `C:\Users\thumb\OneDrive\Documents\Story Skills\`:
```
01_genre_contract.md        13_negation.md
02_controlling_idea.md      14_subplot.md
03_story_spine.md           15_scene_values.md
04_image_system.md          16_rhythm.md
05_act_structure.md         17_gap.md
06_inciting_incident.md     18_text_subtext.md
07_complications.md         19_beat_analysis.md
08_crisis.md                20_on_the_nose.md
09_conflict_levels.md       21_exposition.md
10_true_character.md        22_said_unsaid.md
11_character_dimension.md   23_trialogue.md
12_antagonism.md            24_postmortem.md
```

**Step 3 — Create directories**
```
C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\
C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\staging\
```

**Step 4 — State your plan**
Tell the user:
- Pre-flight passed (all files present, directories created)
- "I will spawn agents using the Agent tool, one per skill, in sequence. I will not run any analysis inline."
- The stop structure: 4 pit stops, 3 one-pager summaries
- Which skill you will begin with

Ask: "Ready to start?" Do not begin until the user says go.

---

## PHASE 1 — RUNNING EACH SKILL

This procedure applies to every skill, every time. No exceptions.

### Step 1 — Stage the inputs

Create a staging folder: `C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\staging\skill_[NN]\`

Copy only the files listed for this skill (see Input Mapping below) into that folder. Nothing else goes in. The agent is instructed to read only from this folder.

All files copy as-is — source files are already named `script.txt` and `beat_sheet.txt`.

### Step 2 — Read the skill file

Read `C:\Users\thumb\OneDrive\Documents\Story Skills\[skill_file].md` into your context.

### Step 3 — Spawn the agent

Call the Agent tool with this structure:

```
Agent(
  description: "Skill [N]: [Skill Name]",
  subagent_type: "general-purpose",
  prompt: """
[PASTE FULL CONTENTS OF THE SKILL FILE HERE]

---

Your input files are in this staging folder:
C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\staging\skill_[NN]\

Read every file in that folder. Those are your only inputs.
Do not read any files outside that folder.

Save your output to:
C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\[output_filename].md

Standards:
- Analyze THIS script specifically — name actual scenes, characters, and lines
- Every problem states WHAT it is, WHERE it occurs, and WHY it is a problem
- Every suggestion is concrete and scene-specific — not "add more conflict" but a specific instruction tied to a specific scene
- Include a teaching moment explaining the underlying McKee principle for a developing writer
- Be honest. Be critical. Be useful. This is a student learning the craft.
- Never say "this is good" without saying what specifically makes it work and why.
- Never say "this needs work" without saying exactly what work and how.
- If you are uncertain about any finding, mark it [LOW CONFIDENCE] and briefly explain why.

When done, report: "Skill [N] complete. Output saved to [full path]."
"""
)
```

### Step 4 — Wait

Do not proceed. Do not spawn the next agent. Wait for the agent to report completion.

### Step 5 — Verify the output

Check that the output file exists at exactly this path:
`C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\[output filename from mapping table]`

Read it. Using the skill file's Output Format section as your spec, confirm the output contains every section defined there. If the file is missing, empty, incorrectly located, or missing required sections, re-spawn the agent with an explicit note identifying what is wrong and where to save the file.

**Retry budget: maximum 3 attempts.** If the output is still invalid after 3 tries, halt. Tell the user which skill failed, what was wrong with the output, and wait for instruction before proceeding.

If the output contains any [LOW CONFIDENCE] flags, surface them to the user before proceeding to the next skill. Ask whether to continue or revisit.

### Step 6 — Check for a stop

See the Stop Protocols section. If this skill has a stop marker, execute it before moving on.

### Step 7 — Clear staging

Delete `outputs\staging\skill_[NN]\` before creating the next staging folder.

---

## INPUT MAPPING

Each skill receives only the files listed here. Stage exactly these — nothing more.

| Skill | Inputs | Output |
|-------|--------|--------|
| 01 Genre Contract | script.txt, beat_sheet.txt | 01_genre_contract.md |
| 02 Controlling Idea | script.txt, 01_genre_contract.md | 02_controlling_idea.md |
| 03 Story Spine | script.txt, 02_controlling_idea.md | 03_story_spine.md |
| 04 Image System | script.txt, 02_controlling_idea.md, 03_story_spine.md | 04_image_system.md |
| 05 Act Structure | script.txt, beat_sheet.txt, 02_controlling_idea.md, 03_story_spine.md | 05_act_structure.md |
| 06 Inciting Incident | script.txt, beat_sheet.txt, 02_controlling_idea.md, 05_act_structure.md | 06_inciting_incident.md |
| 07 Complications | script.txt, beat_sheet.txt, 02_controlling_idea.md, 05_act_structure.md | 07_complications.md |
| 08 Crisis | script.txt, 02_controlling_idea.md, 05_act_structure.md, 07_complications.md | 08_crisis.md |
| 09 Conflict Levels | script.txt, 02_controlling_idea.md, 03_story_spine.md | 09_conflict_levels.md |
| 10 True Character | script.txt, 02_controlling_idea.md, 03_story_spine.md, 09_conflict_levels.md | 10_true_character.md |
| 11 Character Dimension | script.txt, 10_true_character.md | 11_character_dimension.md |
| 12 Antagonism | script.txt, 09_conflict_levels.md, 10_true_character.md, 11_character_dimension.md | 12_antagonism.md |
| 13 Negation | script.txt, 02_controlling_idea.md, 05_act_structure.md | 13_negation.md |
| 14 Subplot | script.txt, 02_controlling_idea.md, 05_act_structure.md, 13_negation.md | 14_subplot.md |
| 15 Scene Values | script.txt, 02_controlling_idea.md | 15_scene_values.md |
| 16 Rhythm | script.txt, beat_sheet.txt, 05_act_structure.md, 15_scene_values.md | 16_rhythm.md |
| 17 Gap | script.txt, 15_scene_values.md | 17_gap.md |
| 18 Text/Subtext | script.txt, 15_scene_values.md, 17_gap.md | 18_text_subtext.md |
| 19 Beat Analysis | script.txt, 15_scene_values.md | 19_beat_analysis.md |
| 20 On-the-Nose | script.txt, 19_beat_analysis.md | 20_on_the_nose.md |
| 21 Exposition | script.txt, 19_beat_analysis.md, 20_on_the_nose.md | 21_exposition.md |
| 22 Said/Unsaid | script.txt, 11_character_dimension.md, 19_beat_analysis.md | 22_said_unsaid.md |
| 23 Trialogue | script.txt, 20_on_the_nose.md, 22_said_unsaid.md | 23_trialogue.md |
| 24 Postmortem | see Postmortem section below | postmortem.md |

---

## POSTMORTEM — SPECIAL HANDLING

Skill 24 cannot use the standard staging procedure. It needs all 23 prior outputs plus the source files — too much content to paste into one prompt. Instead, spawn the postmortem agent with file paths only. The agent reads all files directly using its file tools.

```
Agent(
  description: "Skill 24: Postmortem",
  subagent_type: "general-purpose",
  prompt: """
[PASTE FULL CONTENTS OF 24_postmortem.md HERE]

---

Read each of the following files before beginning your analysis:

SOURCE FILES:
- C:\Users\thumb\OneDrive\Documents\Story Skills\script.txt
- C:\Users\thumb\OneDrive\Documents\Story Skills\beat_sheet.txt

SKILL OUTPUTS:
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\01_genre_contract.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\02_controlling_idea.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\03_story_spine.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\04_image_system.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\05_act_structure.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\06_inciting_incident.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\07_complications.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\08_crisis.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\09_conflict_levels.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\10_true_character.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\11_character_dimension.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\12_antagonism.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\13_negation.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\14_subplot.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\15_scene_values.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\16_rhythm.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\17_gap.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\18_text_subtext.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\19_beat_analysis.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\20_on_the_nose.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\21_exposition.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\22_said_unsaid.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\23_trialogue.md

SUMMARIES (if present):
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\summary_after_04.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\summary_after_13.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\summary_after_20.md

Read all files above. Then complete every step in the skill file.

Save your output to:
C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\postmortem.md

When done, report: "Skill 24 complete. Postmortem saved."
"""
)
```

---

## STOP PROTOCOLS

### 🔴 PIT STOP — After skills 02, 05, 11, 15

After confirming the output file is saved:
1. Stop. Do nothing further until the user responds.
2. Read the output file
3. Present key findings to the user in plain language — what was found, why it matters for the story
4. Ask the user to confirm, push back, or revise
5. If the user revises: edit the output file directly to reflect the agreed version. Note: editing an output file based on user instruction is the one permitted inline action at a pit stop. Generating new analysis is not.
6. Do not spawn the next agent until the user explicitly says to continue

### ⚡ CHECK-IN — After skill 17

After confirming the 17_gap.md output is saved:
1. Stop. Do not spawn the next agent.
2. Read 16_rhythm.md and 17_gap.md
3. Give the user a two-sentence summary of each: what was found in rhythm, what was found in gap analysis
4. Ask: "Anything here you want to revisit before we continue into text/subtext and beat work?"
5. If the user wants to discuss or revise: handle it — same rule as a pit stop: edit output files based on user instruction only, do not generate new analysis inline
6. Once the user says continue, proceed to Skill 18

This is a lighter stop than a full pit stop — the goal is to surface what was found in the uncheckpointed rhythm/gap stretch before the dialogue-level analysis begins, not to require deep revision.

---

### 📋 ONE-PAGER SUMMARY — After skills 04, 13, 20

After confirming the output file is saved, spawn a summary agent:

**After skill 04** — spawn with these paths:
```
Agent(
  description: "One-Pager Summary after Skill 04",
  subagent_type: "general-purpose",
  prompt: """
Read each of the following files:
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\01_genre_contract.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\02_controlling_idea.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\03_story_spine.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\04_image_system.md

Write a one-page summary. Bullets only. Include:
- Key decisions established (genre, controlling idea, spine, image system)
- Assumptions the analysis is operating on
- Open questions or flags not yet resolved

Save to: C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\summary_after_04.md
Report: "Summary complete."
"""
)
```

**After skill 13** — spawn with these paths:
```
Agent(
  description: "One-Pager Summary after Skill 13",
  subagent_type: "general-purpose",
  prompt: """
Read each of the following files:
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\01_genre_contract.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\02_controlling_idea.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\03_story_spine.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\04_image_system.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\05_act_structure.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\06_inciting_incident.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\07_complications.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\08_crisis.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\09_conflict_levels.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\10_true_character.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\11_character_dimension.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\12_antagonism.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\13_negation.md

Write a one-page summary. Bullets only. Include:
- Key decisions established (structure, character, thematic depth)
- Assumptions the analysis is operating on
- Open questions or flags not yet resolved

Save to: C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\summary_after_13.md
Report: "Summary complete."
"""
)
```

**After skill 20** — spawn with these paths:
```
Agent(
  description: "One-Pager Summary after Skill 20",
  subagent_type: "general-purpose",
  prompt: """
Read each of the following files:
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\01_genre_contract.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\02_controlling_idea.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\03_story_spine.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\04_image_system.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\05_act_structure.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\06_inciting_incident.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\07_complications.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\08_crisis.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\09_conflict_levels.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\10_true_character.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\11_character_dimension.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\12_antagonism.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\13_negation.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\14_subplot.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\15_scene_values.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\16_rhythm.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\17_gap.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\18_text_subtext.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\19_beat_analysis.md
- C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\20_on_the_nose.md

Write a one-page summary. Bullets only. Include:
- Key decisions established (scene-level craft, dialogue, beat work)
- Assumptions the analysis is operating on
- Open questions or flags not yet resolved

Save to: C:\Users\thumb\OneDrive\Documents\Story Skills\outputs\summary_after_20.md
Report: "Summary complete."
"""
)
```

Verify the summary: confirm the file exists at the expected path and contains all three required sections (decisions, assumptions, open flags). If missing or incomplete, re-spawn the summary agent once. Maximum 2 attempts — if it still fails, tell the user and wait for instruction.

Present the summary to the user. Wait for go-ahead before proceeding to the next skill.

---

## SEQUENCE AND STOP MAP

| # | Skill | Stop |
|---|-------|------|
| 01 | Genre Contract | — |
| 02 | Controlling Idea | 🔴 |
| 03 | Story Spine | — |
| 04 | Image System | 📋 |
| 05 | Act Structure | 🔴 |
| 06 | Inciting Incident | — |
| 07 | Complications | — |
| 08 | Crisis | — |
| 09 | Conflict Levels | — |
| 10 | True Character | — |
| 11 | Character Dimension | 🔴 |
| 12 | Antagonism | — |
| 13 | Negation | 📋 |
| 14 | Subplot | — |
| 15 | Scene Values | 🔴 |
| 16 | Rhythm | — |
| 17 | Gap | ⚡ |
| 18 | Text/Subtext | — |
| 19 | Beat Analysis | — |
| 20 | On-the-Nose | 📋 |
| 21 | Exposition | — |
| 22 | Said/Unsaid | — |
| 23 | Trialogue | — |
| 24 | Postmortem | — |

---

## TONE AND STANDARDS — PASS TO EVERY AGENT

Include this block in every agent prompt:

- Analyze THIS script specifically — name actual scenes, characters, and lines
- Every problem states WHAT it is, WHERE it occurs, and WHY it is a problem
- Every suggestion is concrete and scene-specific — not "add more conflict" but a specific instruction tied to a specific scene
- Include a teaching moment explaining the underlying McKee principle for a developing writer
- Be honest. Be critical. Be useful. This is a student learning the craft.
- Never say "this is good" without saying what specifically makes it work and why.
- Never say "this needs work" without saying exactly what work and how.
- If you are uncertain about any finding, mark it [LOW CONFIDENCE] and briefly explain why.

---

## RESUMING A BROKEN RUN

**Scenario: session ended mid-run, same draft, same script.**
Before spawning any agent, check whether its expected output file already exists and is non-empty. If it does, skip that skill and move to the next. Report to the user which skills were skipped and which are being run fresh. All outputs in the folder are from the same draft — resuming mid-sequence is safe.

---

## AFTER A REWRITE

**Scenario: the script has been rewritten. This is a new draft.**
Always start from Skill 01. Do not resume mid-sequence with a new script. Prior outputs were generated from a different draft — feeding them to new agents will contaminate the analysis. The only safe starting point for a new draft is the beginning.

1. Replace `script.txt` with the new draft
2. Move `outputs\` to `outputs\draft_[N]\` to preserve prior analysis
3. Create fresh `outputs\` and `outputs\staging\` directories
4. Restart from Skill 01, or ask the user if they want to resume from a pit stop

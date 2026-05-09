# Skill 24 — Postmortem

## Purpose
The postmortem takes every output from the 23 exercises and synthesizes them
into one digestible document. It is not a summary — it is a prioritized action
plan with teaching embedded. It separates what is working from what isn't,
orders the problems by urgency, and gives the writer a clear picture of what
the next draft needs to accomplish.

This is the document you bring to your rewrite.

## Inputs
All 23 exercise output files, all 3 summary one-pagers, and the original:
- script.txt
- beat_sheet.txt

## Instructions

If a required input file is missing or does not contain the expected content, halt immediately and report the missing input to the orchestrator — do not proceed with partial context.

### Step 1 — Triage All Problems
Read every output file. List every problem identified across all 23 exercises.
Then sort them into three tiers:

**TIER 1 — FOUNDATIONAL** (fix these first; they affect everything else)
These are structural and thematic problems: weak controlling idea, broken spine,
missing structural beats, flat antagonism, one-dimensional conflict. If these
aren't fixed, scene-level improvements won't hold.

**TIER 2 — SCENE-LEVEL** (fix after foundation is solid)
Scenes that don't turn, rhythm problems, gap failures, text/subtext misalignment.
These are the craft problems that a solid foundation can now support.

**TIER 3 — DIALOGUE AND SURFACE** (refine last)
On-the-nose lines, exposition delivery, beat flatness, trialogue opportunities.
These are important but are the last pass — fixing them before Tier 1 and 2
is polishing before the structure is sound.

After sorting all problems into tiers, look for contradictions across skill outputs — places where two skills reached different conclusions about the same element. Name both conclusions, explain the disagreement, and state which to trust and why. Do not silently pick one.

### Step 2 — Identify What Is Working
For each exercise, note what the script is doing WELL — specifically, with
scene/line references. What should be protected in the rewrite? What is
already achieving the controlling idea?

Do not be vague. "The image system is strong" is not sufficient.
"The gum's color saturation as a value indicator in Scenes 1, 3, and 5
is a functioning image system that connects directly to the controlling
idea — protect this and extend it" is.

### Step 3 — Write the Priority Action List
For each Tier 1 problem: write a specific rewrite instruction.
Not "strengthen the crisis" — "The crisis in Scene 5 is currently Florence
choosing to give Sebastian all her gum. This is not a genuine dilemma because
the audience does not yet feel what the gum costs her. Before the crisis,
establish one moment in which the gum is the only thing that saves her —
so that giving it away is a real sacrifice."

### Step 4 — Write the Teaching Section
For each major finding — positive or negative — write a brief teaching moment
explaining the principle behind it. This section is written for the writer
as a student: what is the underlying craft principle, and why does it matter?

This is not criticism — it is education. The goal is for the writer to
understand not just WHAT to fix but WHY it matters, so they carry the
principle forward into the next project.

### Step 5 — Rewrite Roadmap
Write a brief rewrite roadmap: in what order should the writer address
the problems? Starting with Tier 1, ending with Tier 3. For a short film,
this should be a one-page plan.

## Output Format

If the script does not provide enough material to complete this analysis confidently, mark the output [INCONCLUSIVE] at the top of the file, describe what is missing or ambiguous, and flag it for human review before the pipeline continues.

Save as `postmortem.md`:

```
# SCRIPT ANALYSIS POSTMORTEM
Script: [title if present, or filename]
Analysis completed: [date]

---

## WHAT IS WORKING
[Numbered list — specific, with scene references]
1. [What + why it works + protect this in the rewrite]
...

---

## TIER 1 — FOUNDATIONAL PROBLEMS
[These must be addressed first]

[Problem number]. [PROBLEM NAME]
- What it is: [specific description with scene reference]
- Why it matters: [the principle at stake — one sentence]
- What to do: [specific rewrite instruction]

...

---

## TIER 2 — SCENE-LEVEL PROBLEMS
[Address after Tier 1 is resolved]

[Same format]

---

## TIER 3 — DIALOGUE AND SURFACE
[Refine last]

[Same format]

---

## TEACHING MOMENTS
[The principles behind the major findings — written for a developing writer]

[Topic]: [2-3 sentence explanation of the craft principle and why it matters,
grounded in what this specific script revealed]

...

---

## REWRITE ROADMAP
Draft [X+1] priorities, in order:
1. [First thing to tackle + why]
2. [Second]
...

Estimated scope: [how significant are the changes needed?
Small adjustments / Scene-level rewrites / Structural rebuild]

---

## A NOTE ON THIS SCRIPT
[One honest paragraph — not a grade, not a verdict — about what this script
is attempting and how close it is to achieving it. What is its strongest
impulse? Where is it most itself? What does it need to become what it's
trying to be?]
```

## Standards for the Postmortem
- Every problem must have a specific rewrite instruction — not general advice
- Every strength must be named specifically with scene references
- The teaching moments must explain the WHY, not just the WHAT
- The final note must be honest and generous — this is a developing writer
- The tone is a knowledgeable collaborator, not a judge


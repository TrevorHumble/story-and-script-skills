# Skill 10 — True Character vs. Characterization Test

## Purpose
Characterization is the surface: how a character dresses, speaks, what job they
hold, how they act when nothing is at stake. True character is who they actually
are — revealed only when they must make a meaningful choice under genuine pressure,
when one option costs them something real.

McKee: "True character is revealed in the choices a human being makes under
pressure — the greater the pressure, the deeper the revelation."

A character can be richly characterized for fifty pages. If they are never truly
tested, the audience does not yet know them.

## Inputs
- script.txt
- 02_controlling_idea.md
- 03_story_spine.md
- 09_conflict_levels.md

## Instructions

If a required input file is missing or does not contain the expected content, halt immediately and report the missing input to the orchestrator — do not proceed with partial context.

### Step 1 — List Characterization
For each major character: list their surface traits. How they appear. How they
speak. What the world knows about them. What we observe in low-stakes moments.

### Step 2 — Identify Moments of Choice Under Pressure
For each major character: find every moment in the script where they make a
consequential choice with real cost. Write each down. What the protagonist reveals under pressure should connect to what the controlling idea argues — true character and the story's central claim are ultimately the same thing.

### Step 3 — Test the Pressure
For each choice: is there a REAL cost to one of the options? Is the character
risking something they genuinely value — a relationship, safety, identity,
moral self-image?

If the choice has no real cost, the pressure is insufficient. The true character
is not being revealed — only the characterization.

### Step 4 — Check for Contradiction Between Surface and Depth
Does the character's behavior under pressure SURPRISE us in a way that is more
true than their surface? Or do they behave exactly as their surface traits predict?
The most revealing moments are those where who they turn out to be is different
from — but more true than — who they appeared to be.

### Step 5 — Identify the Deepest Revelation
For each major character: which moment of choice reveals them most deeply?
Is it near the climax? It should be — the climax should produce the deepest
revelation of all.

### Step 6 — Check for Arc
Does the character's true nature change — or become more fully expressed —
over the course of the story? Or do they make one choice under pressure and
then return to exactly who they were?

## Output Format

If the script does not provide enough material to complete this analysis confidently, mark the output [INCONCLUSIVE] at the top of the file, describe what is missing or ambiguous, and flag it for human review before the pipeline continues.

Save as `10_true_character.md`:

```
CHARACTER: [name]
CHARACTERIZATION: [surface traits]
MOMENTS OF CHOICE UNDER PRESSURE:
  - [Scene]: [choice] — Cost: [real / insufficient] — Reveals: [what]
DEEPEST REVELATION: [scene + what it shows]
SURFACE VS DEPTH: [does pressure reveal something truer than the surface?]
ARC: [does true nature change or deepen? or does character reset?]

[Repeat for each major character]

PROBLEMS: [which characters are never genuinely tested, or whose choices have no cost]
SUGGESTIONS: [specific scenes where pressure could be increased, or where a
choice currently has no cost and could be given one]
TEACHING MOMENT: [the difference between characterization and true character —
why a richly described character with no pressure is still a stranger to the audience]
```


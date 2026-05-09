# Skill 01 — Genre Contract Audit

## Purpose
Every story makes a promise to its audience before a single scene plays out. That
promise is the genre contract: a set of conventions the audience expects to see honored,
and a set of obligatory scenes they need delivered. This skill audits whether the script
is keeping that promise — and whether it's doing so freshly or falling back on cliché.

This runs first because everything downstream depends on knowing what kind of story
this is and what it must deliver. A thriller that doesn't generate dread, a romance
that doesn't earn connection — these aren't just missed opportunities, they're broken
contracts.

## Inputs
- script.txt
- beat_sheet.txt

## Instructions

### Step 1 — Name the Genre
Read the script. Identify the genre or genre blend. Be specific.
Not "drama" — "surrealist coming-of-age with dark comedy elements."
Not "romance" — "reluctant-connection character study with magical realist framing."

If multiple genres are at play, name the dominant one and the secondary one.
Note: a short film often bends genre more aggressively than a feature. That's fine —
but the contract still exists and must be named.

### Step 2 — Define the Emotional Promise
What core emotional experience does this genre promise the audience?
Write it as a sentence: "This story promises the audience [X feeling] through [Y experience]."
Example: "This story promises the audience a sense of liberation and melancholy through
watching a person discover they've been giving themselves away."

### Step 3 — List the Obligatory Scenes
Based on the genre, list the scenes the audience absolutely needs to see.
These are the scenes whose absence would feel like a cheat.

For each obligatory scene:
- Name it
- Check whether it is present in the script
- If present: is it executed freshly or predictably?
- If missing: flag it

### Step 4 — List the Conventions
List the genre's recurring elements — character types, settings, tonal registers,
structural patterns — that signal to the audience what kind of story this is.
For each: is it present? Is it used as a foundation for something specific, or
as a shorthand that produces cliché?

### Step 5 — Check for Genre Confusion
Does the script promise one genre contract in the opening and deliver a different
one by the end? If so: is the shift earned and intentional, or does it leave the
audience stranded?

### Step 6 — Subversion Assessment
McKee's standard: a masterful genre writer honors every convention but executes
none of them predictably. Where is this script subverting convention? Is the
subversion earning something, or is it avoiding the hard work of executing the
convention well?

## Output Format

If the script does not provide enough material to complete this analysis confidently, mark the output [INCONCLUSIVE] at the top of the file, describe what is missing or ambiguous, and flag it for human review before the pipeline continues.

Save as `01_genre_contract.md` with these sections:

```
GENRE: [specific genre name]
EMOTIONAL PROMISE: [one sentence]

OBLIGATORY SCENES:
- [Scene name]: PRESENT / MISSING — [fresh or clichéd, and why]

CONVENTIONS:
- [Convention]: PRESENT / MISSING — [working or clichéd, and why]

GENRE CONFUSION: [yes/no, and explanation if yes]

SUBVERSION: [what is being subverted, whether it earns it]

PROBLEMS:
[Numbered list of specific issues with scene/line references]

SUGGESTIONS:
[For each problem: a concrete suggestion with explanation of why it would work]

TEACHING MOMENT:
[One paragraph explaining the principle at stake — written for a student]
```

## Standards
- Every problem must name the specific scene or moment in the script
- Every suggestion must be actionable, not abstract
- If the genre is being done well, say so and say why — specifics only


# Skill 11 — Character Dimension Contradiction Mapping
# 🔴 PIT STOP AFTER THIS EXERCISE

## Purpose
McKee defines dimension as CONSISTENT CONTRADICTION — either within a character's
deep nature (a ruthless person who is tender with strangers) or between their
surface and their depth (a charming person who is destructive at their core).

The key word is consistent. A contradiction that appears once is a surprise.
A contradiction that appears repeatedly, under different pressures, in different
situations — that is a dimension. It means this person has an inner life the
audience can never fully predict.

A flat character has no contradictions. An inconsistent character has contradictions
that feel random rather than psychologically true. A dimensional character has
contradictions that are both surprising and inevitable.

## Inputs
- script.txt
- 10_true_character.md

## Instructions

If a required input file is missing or does not contain the expected content, halt immediately and report the missing input to the orchestrator — do not proceed with partial context.

### Step 1 — List All Traits and Behaviors
For each major character: list every trait and behavioral pattern visible in
the script. Include both surface (characterization) and pressure-revealed
(true character) behaviors from Exercise 10.

### Step 2 — Find the Contradictions
Look for places where two traits or behaviors seem to oppose each other.
Don't look for inconsistency — look for contradiction that is psychologically real.
List each one: "[Character] is [X] but also [Y]."

### Step 3 — Test for Consistency
For each contradiction: does it appear more than once across the script?
Does it show up in different situations under different pressures?
One appearance = surprise. Multiple appearances = dimension.

### Step 4 — Test for Credibility
For each contradiction: can you construct a psychological or biographical reason
why these two opposing traits coexist in this person?
If you cannot explain it, it may be inconsistency rather than dimension.

### Step 5 — Test Under Pressure
When things are hardest for the character, which side of the contradiction wins?
A contradiction that is never tested under maximum pressure is not load-bearing.
It is decoration.

### Step 6 — Check the Antagonist
A purely negative antagonist with no contradictions is a function, not a character.
Does the antagonist have at least one dimension — one place where they surprise us
in a psychologically credible way?

## Output Format

If the script does not provide enough material to complete this analysis confidently, mark the output [INCONCLUSIVE] at the top of the file, describe what is missing or ambiguous, and flag it for human review before the pipeline continues.

Save as `11_character_dimension.md`:

```
CHARACTER: [name]
TRAITS INVENTORY: [full list]
CONTRADICTIONS:
  - [Contradiction]: Consistent (appears X times) / Single appearance
    Credible: YES/NO — [psychological explanation]
    Tested under pressure: YES/NO
DIMENSIONALITY ASSESSMENT: Dimensional / Flat / Inconsistent

[Repeat for each major character]

ANTAGONIST DIMENSION: [specific contradiction + whether it is working]

PROBLEMS: [characters who are flat, or whose contradictions feel random]
SUGGESTIONS: [concrete — "Sebastian's willingness to manipulate while also
genuinely comforting Florence is a strong contradiction. It appears in Scene 5
and Scene 7. It needs one more appearance under different pressure to become
a true dimension — consider Scene 3's initial meeting."]
TEACHING MOMENT: [the difference between inconsistency and dimension —
why contradiction must be consistent to create inner life]
```

## Note: Pit Stop
This exercise is followed by a pit stop. The orchestrator handles the pause and user review — your job is to complete the analysis, save the output, and report done.


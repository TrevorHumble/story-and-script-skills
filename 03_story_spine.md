# Skill 03 — Story Spine Extraction

## Purpose
The story spine is the through-line of desire that holds the whole story together:
the protagonist's conscious want and unconscious need, established by the inciting
incident and resolved only at the climax. If the spine is unclear or shifts without
dramatic cause, the story feels directionless even when individual scenes work.

A want is what the protagonist is consciously chasing. A need is what they actually
require — often in direct contradiction to the want. The most resonant stories make
the protagonist choose between them.

## Inputs
- script.txt
- 02_controlling_idea.md

## Instructions

If a required input file is missing or does not contain the expected content, halt immediately and report the missing input to the orchestrator — do not proceed with partial context.

### Step 1 — State the Want
What is the protagonist consciously pursuing? Write it as a specific infinitive:
"Florence wants to escape the weight of real life."
Avoid abstractions like "wants to be happy." That is not a want — it is a mood.
The want must be specific enough that you can write a scene that advances or blocks it.

### Step 2 — State the Need
What does the protagonist actually need — the thing that would genuinely change
their life, which they are often resisting or unaware of?
Write it the same way: specific infinitive.
"Florence needs to stop giving herself away to things that can't give back."

### Step 3 — Check the Spine
Ask: is the protagonist's want established by or shortly after the inciting incident?
Ask: does the climax resolve the want — by achieving it, failing to achieve it,
or by the protagonist consciously abandoning it for something more important?
If the inciting incident and the climax are not answering the same question,
the spine is broken. Name where it breaks.

### Step 4 — Trace the Spine Through the Story
Go act by act (or scene by scene for a short). Is the want still the engine
driving events in the middle? Or does a different desire take over without
dramatic cause? Mark any moment where the spine seems to drop.

### Step 5 — Check the Want/Need Tension
Does the story create situations where pursuing the want makes satisfying the
need harder? The best stories make the protagonist's surface goal the very
thing standing between them and what they actually need.

### Step 6 — Connect to the Controlling Idea
The spine and the controlling idea should be in conversation. The protagonist's
want should be what leads them toward (or away from) the value in the controlling
idea. Check: does the spine connect to the controlling idea, or are they
pulling in different directions?

## Output Format

If the script does not provide enough material to complete this analysis confidently, mark the output [INCONCLUSIVE] at the top of the file, describe what is missing or ambiguous, and flag it for human review before the pipeline continues.

Save as `03_story_spine.md`:

```
PROTAGONIST: [name]
WANT: [specific infinitive]
NEED: [specific infinitive]
WANT/NEED TENSION: [how they conflict]

SPINE INTEGRITY:
- Inciting incident establishes the want: PASS/FAIL — [where/why]
- Want drives the middle: PASS/FAIL — [where it drops, if anywhere]
- Climax resolves the want: PASS/FAIL — [how]
- Need is addressed by the climax: PASS/FAIL — [how]

CONNECTION TO CONTROLLING IDEA: [how the spine feeds the story's argument]

PROBLEMS:
[Specific moments where the spine breaks or the want shifts without cause]

SUGGESTIONS:
[Concrete fixes — not "make the want clearer" but "in Scene X, Florence's
action is serving a different desire. Tie it back to Y by doing Z."]

TEACHING MOMENT:
[Explain want vs. need and why their tension is the engine of character arc.
Why "wants to be happy" isn't a spine. What makes a spine specific enough to work.]
```


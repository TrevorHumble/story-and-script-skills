# Skill 17 — The Gap Analysis

## Purpose
The gap is the rift between what a character expects to happen when they take
action and what actually happens. It is the engine of dramatic tension. When a
character takes action and gets exactly what they expected — when there is no
gap between intention and result — there is no tension. The world is cooperating,
which means nothing is at stake.

McKee: "The substance of a story is the gap that splits open between what a
human being expects to happen when they take action and what really does happen."

## Inputs
- script.txt
- 15_scene_values.md

## Instructions

If a required input file is missing or does not contain the expected content, halt immediately and report the missing input to the orchestrator — do not proceed with partial context.

### Step 1 — Identify Action and Expectation
For key scenes (prioritize those that failed the scene value test, and those
around major structural beats): what action does the protagonist take? What
do they expect to happen as a result?

### Step 2 — Identify the Result
What actually happens? Does reality deliver what was expected — or something
different?

### Step 3 — Measure the Gap
Is there a gap between expectation and result?
If no gap: flag the moment. The protagonist got what they wanted. No tension.
If yes: how significant is the gap? Does it force the protagonist to change
their approach, or are they able to continue with the same strategy?

### Step 4 — Trace Gap Escalation
Across the story: is each gap larger than the last? Does each gap force the
protagonist to risk more than the previous beat?
McKee's pattern: action → gap → escalated action → larger gap → crisis.
Map this pattern and identify where it breaks down.

### Step 5 — Find the Largest Gap
Where is the moment in the script where the distance between expectation and
result is most extreme? This should be near or at the crisis.
If the largest gap is early in the story, the story may be peaking too soon.

### Step 6 — Check Gap-less Passages
Identify any extended passage where the protagonist is moving through the world
without resistance — where reality keeps cooperating. These passages have no
gap and therefore no dramatic tension, even if they are beautifully written.

## Output Format

If the script does not provide enough material to complete this analysis confidently, mark the output [INCONCLUSIVE] at the top of the file, describe what is missing or ambiguous, and flag it for human review before the pipeline continues.

Save as `17_gap.md`:

```
GAP ANALYSIS BY SCENE:
| Scene | Action | Expectation | Result | Gap? | Gap Size |
|-------|--------|-------------|--------|------|----------|
| [scene] | [what protagonist does] | [what they expect] | [what happens] | YES/NO | small/medium/large |
...

ESCALATION PATTERN: [is each gap larger? where does it break down?]
LARGEST GAP: [scene + why it's the peak]
GAP-LESS PASSAGES: [scenes where world cooperates — list and explain impact]

PROBLEMS: [numbered, specific — moments with no gap, gaps that don't escalate]
SUGGESTIONS: [concrete — "In Scene 3, Florence expects the gum to transport her
to safety but instead lands her somewhere more threatening. That gap is working.
In Scene 2, she expects to be left alone and is — no gap, no tension. Consider
having the environment resist her in a small but specific way."]
TEACHING MOMENT: [why the gap is not just a plot complication but the moment
of discovery — the place where the protagonist learns something about the world
and must adapt. Why a world that cooperates is a world without drama.]
```


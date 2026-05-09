# Skill 15 — Scene Value Shift Analysis

## Purpose
Every scene must turn the value-charged condition of a character's life from one
polarity to another. If the value at the scene's opening is identical to the value
at its close, nothing meaningful happened — the scene is a non-event. McKee:
"Why is this scene in your script?"

This is the most actionable and non-negotiable exercise in the set. It applies
to every single scene. There are no exceptions.

Run this exercise scene by scene across the full script. Produce a chart.

## Inputs
- script.txt
- 02_controlling_idea.md

## Instructions

If a required input file is missing or does not contain the expected content, halt immediately and report the missing input to the orchestrator — do not proceed with partial context.

For EACH scene in the script, complete the following five steps.

### Step 1 — Define the Conflict
Who is driving the scene (scene protagonist)?
Who or what is opposing them (scene antagonist)?
State each desire as an infinitive:
"[Character] wants to [X]." "[Character/force] wants to [Y]."
The conflict must be DIRECT — not tangential.

### Step 2 — Note the Opening Value
The controlling idea names the core value this story is tracking — use it as your compass for which value polarity matters most in each scene. What value-charged condition is operative at the scene's start?
State it as one word and its polarity: hope (positive), isolation (negative),
safety (positive), shame (negative).

### Step 3 — Break into Beats
A beat is one exchange of action/reaction in character behavior.
For each beat, assign a gerund pair: asking/ignoring, insisting/deflecting.
These label what characters are actually DOING — not what they are saying.

### Step 4 — Note the Closing Value and Compare
What is the value at the scene's end? Same word? Same polarity?
If opening value = closing value: the scene is a non-event. Flag it.
If opening polarity = closing polarity (both negative, or both positive)
but the value has shifted: note the degree of change — is it meaningful?

### Step 5 — Locate the Turning Point
Survey the beats. Find the moment when the value shifts — the gap between
expectation and result that causes the reversal. Is it specific? Does it
arrive as a surprise that feels, in retrospect, inevitable?

## Output Format

If the script does not provide enough material to complete this analysis confidently, mark the output [INCONCLUSIVE] at the top of the file, describe what is missing or ambiguous, and flag it for human review before the pipeline continues.

Save as `15_scene_values.md`:

First, a scene-by-scene chart:
```
SCENE VALUE CHART:
| Scene | Opening Value | Closing Value | Turns? | Turning Point |
|-------|--------------|---------------|--------|---------------|
| 1     | [value/charge] | [value/charge] | YES/NO | [beat] |
| 2     | ...
...
```

Then, for each scene that FAILS (does not turn):
```
SCENE [X] — NON-EVENT ANALYSIS:
Conflict: [protagonist want / antagonist want]
Opening value: [word + charge]
Closing value: [word + charge — same as opening]
Why it fails: [specific explanation]
How to fix it: [concrete suggestion — what would have to change in the scene's
action for the value to shift by the end]
```

Then overall:
```
SCENES THAT TURN: [count] / [total]
SCENES THAT DON'T: [list]
STRONGEST TURNING POINT: [scene + why it works]
WEAKEST SCENE: [scene + most urgent fix needed]

TEACHING MOMENT:
[Explain the non-event rule — why a scene where nothing changes is not just
weak but actively harmful. Why the turning point must feel both surprising
and inevitable. Why this is the test every scene must pass before anything else.]
```

## Note: Pit Stop
This exercise is followed by a pit stop. The orchestrator handles the pause and user review — your job is to complete the analysis, save the output, and report done.


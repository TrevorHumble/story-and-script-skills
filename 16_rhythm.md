# Skill 16 — Rhythm and Pacing Audit

## Purpose
Rhythm is the pattern of variation in scene length across a story. Tempo is the
level of activity within each scene. A story that holds the same register — same
length, same intensity, same emotional pitch — for too long becomes numbing even
when individual scenes are strong. The audience needs contrast and recovery to
feel each impact fully.

McKee: "Repetitiveness is the enemy of rhythm. When emotional experience repeats,
the power of the second event is cut in half."

## Inputs
- script.txt
- beat_sheet.txt
- 05_act_structure.md
- 15_scene_values.md

## Instructions

If a required input file is missing or does not contain the expected content, halt immediately and report the missing input to the orchestrator — do not proceed with partial context.

### Step 1 — Map Scene Length and Register
For each scene, note:
- Approximate length (short / medium / long relative to the other scenes)
- Dominant emotional register: high tension, moderate tension, low tension,
  release/comedy, reflection, transition

### Step 2 — Read the Pattern
Look at the length and register sequence as a whole. Measure rhythm against act structure — does pacing build toward act turns or obscure them? Find:
- Runs of 3+ consecutive scenes at the same register: flag as flat passages
- Scenes of equal length running consecutively: flag as rhythmically monotonous

### Step 3 — Test the Impact Scenes
For each high-tension scene or major reversal: what immediately precedes it?
Is there a scene of lower tension or shorter length that gives the audience
room to breathe before the impact arrives?
A climax preceded by equal-intensity scenes will not land at full force.

### Step 4 — Check Tempo Variation
Are all scenes running at the same activity level — all dialogue, all action,
all visual? Vary the method of storytelling alongside the rhythm of length.

### Step 5 — Test the Longest Scene
Identify the longest scene. Does it earn its length? Does it carry proportionally
more weight than shorter scenes? A long scene that doesn't carry more weight is
simply slow.

### Step 6 — Check Scene Value Rhythm
Using the scene value chart from Exercise 15: are consecutive scenes charging
the same value polarity? Two consecutive positive-to-negative turns without
relief between them may be rhythmically numbing even if both scenes work individually.

## Output Format

If the script does not provide enough material to complete this analysis confidently, mark the output [INCONCLUSIVE] at the top of the file, describe what is missing or ambiguous, and flag it for human review before the pipeline continues.

Save as `16_rhythm.md`:

```
RHYTHM MAP:
| Scene | Length | Register | Value Direction |
|-------|--------|----------|-----------------|
| 1     | [short/med/long] | [register] | [+ to - / - to + / etc] |
...

FLAT PASSAGES: [consecutive scenes at same register — list them]
IMPACT SCENE BREATHING ROOM: [does each major reversal have recovery before it?]
TEMPO VARIATION: PASS/FAIL — [explanation]
LONGEST SCENE JUSTIFIED: PASS/FAIL — [which scene, why or why not]
VALUE RHYTHM: [are value directions varying enough?]

PROBLEMS: [numbered, specific]
SUGGESTIONS: [concrete — "Scene 4 and 5 are both high-tension medium-length
scenes with negative value turns. A brief scene of release between them —
even 30 seconds — would let the audience reset before Scene 5 hits."]
TEACHING MOMENT: [why contrast is not a luxury but a requirement — the audience's
emotional system needs rest to function. Why rest is not weakness.]
```


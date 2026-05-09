# Skill 22 — The Said, Unsaid, and Unsayable

## Purpose
McKee describes every character as having three concentric layers:
- **The Said**: what they express to others
- **The Unsaid**: what they think to themselves but don't express — their inner
  voice, running continuously beneath the surface
- **The Unsayable**: subconscious urges and drives the character cannot articulate
  even to themselves — mute desires below awareness

In any scene, each character is responding not to what was literally said but to
what they INTERPRETED it to mean — filtered through their history, fears, and desires.
Behavior that looks irrational on the surface is almost always logical when seen from
inside the character's head.

This exercise makes that invisible layer visible.

## Inputs
- script.txt
- 11_character_dimension.md
- 19_beat_analysis.md

## Instructions

If a required input file is missing or does not contain the expected content, halt immediately and report the missing input to the orchestrator — do not proceed with partial context.

### Step 1 — Select Scenes
Choose scenes where character behavior feels unexpected, unmotivated, or where
the scene's emotional intensity seems disproportionate to its surface content.
These are the scenes most likely to have a rich unsaid layer that isn't visible.

### Step 2 — Write the Inner Monologue
For each character in the scene, go beat by beat.
At each beat where the character speaks or acts, write in parentheses what they
are ACTUALLY THINKING — in first person, present tense, their own voice.

This is the unsaid layer. Not what they would say if they were honest — what
they are thinking RIGHT NOW, including the misreadings and assumptions.

Example:
Character says: "Have you eaten?"
Inner monologue: *(She looks pale. Something is wrong. If I ask directly she'll
shut down. Try something that looks like care but gives me information.)*

### Step 3 — Map the Misreadings
Look at the gap between each character's inner interpretation and what the other
character actually said or meant. Mark every misreading, false assumption,
or projection.

Ask: is this misreading intentional? Is it serving the scene's turning point?
Or is it an accidental inconsistency?

### Step 4 — Find the Unsayable
Go deeper: is there anything either character wants that they cannot even admit
to themselves? A desire or fear so threatening that even their inner voice
avoids naming it directly? The unsayable is often rooted in character dimension — the core contradiction a character cannot acknowledge. Use the character dimension map to locate it.

If the scene has unexplained emotional intensity that neither character's stated
wants account for, the unsayable is likely at work. Name it.

### Step 5 — Test the Surface
Compare the inner monologue map to the written scene. Is the surface of the
scene (the said) reflecting the inner life accurately enough that the audience
can sense it? Or is the inner life invisible, producing a scene that feels flat
despite technically having conflict?

## Output Format

If the script does not provide enough material to complete this analysis confidently, mark the output [INCONCLUSIVE] at the top of the file, describe what is missing or ambiguous, and flag it for human review before the pipeline continues.

Save as `22_said_unsaid.md`:

```
For each selected scene:

SCENE [X] — INNER LIFE MAP:
Beat 1:
  [Character A says]: "[line]"
  [Character A thinks]: (inner monologue)
  [Character B says]: "[line]"
  [Character B thinks]: (inner monologue)
Beat 2: [etc.]

MISREADINGS:
- Beat [X]: [Character] misreads [other character's action] as [interpretation]
  — Intentional/Accidental — [serves or doesn't serve the turning point]

THE UNSAYABLE (if present): [what neither character can admit, and where it surfaces]

SURFACE TEST: Does the written scene surface the inner life? YES/NO/PARTIALLY
  If partially: [what is visible, what is invisible]

---

OVERALL:
SCENES WHERE INNER LIFE IS WELL-SURFACED: [list]
SCENES WHERE INNER LIFE IS INVISIBLE: [list — these produce flat or
seemingly unmotivated behavior]

PROBLEMS: [specific beats where behavior is driven by inner logic the script
doesn't surface — producing actions that seem arbitrary to the audience]
SUGGESTIONS: [concrete — "Sebastian's manipulation in Scene 5 looks random
because we don't see the inner logic driving it. If his unsaid layer shows
he is running a calculated pattern — finding her attachment points and
exploiting them systematically — his behavior becomes chilling rather than
confusing. One small behavioral tell per scene could surface this."]
TEACHING MOMENT: [why behavior that seems irrational is almost always
logical from inside the character's head — and why the writer's job is to
find that logic and put it into the scene's surface even if it never
becomes speech]
```


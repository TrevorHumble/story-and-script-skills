# Skill 19 — Beat Analysis in Dialogue

## Purpose
A beat is one exchange of action/reaction in character behavior. Every line of
dialogue is an action taken toward a want — and every response is a reaction
that either advances, resists, or redirects. The gerund is the most important
word in this exercise: it names the ACTUAL action being taken, which is almost
never the same as the literal speech.

If the gerund and the literal speech are identical — if a character is demanding
by literally saying "I demand" — the dialogue has no inner life.

Run this exercise on all significant dialogue scenes.

## Inputs
- script.txt
- 15_scene_values.md

## Instructions

If a required input file is missing or does not contain the expected content, halt immediately and report the missing input to the orchestrator — do not proceed with partial context.

### Step 1 — Select the Scene
Work through each significant dialogue exchange in the script. Prioritize scenes that failed the scene value test — scenes without a clear value turn are the most likely to have beat-level problems causing that flatness.

### Step 2 — Assign Gerunds to Each Beat
For each exchange of dialogue (character speaks, other responds):
- Name what the speaking character is DOING (not saying): demanding, flattering,
  deflecting, threatening, pleading, testing, stalling, exposing, retreating
- Name the responding character's action: ignoring, challenging, capitulating,
  redirecting, accepting, attacking, comforting, withdrawing

Write them as pairs: demanding/ignoring, flattering/deflecting.

### Step 3 — Read the Gerund Sequence as a Story
Stack all gerund pairs in order. Read them as a narrative. Does the sequence
have a shape? Does it escalate? Does it reach a turning point?

### Step 4 — Find Flat Passages
Identify consecutive beats where the gerunds are essentially the same action.
Demanding/ignoring → demanding/ignoring → demanding/ignoring = flat.
The scene is not progressing. It is looping.

### Step 5 — Compare Gerunds to Literal Speech
For each beat: how far is the gerund from the literal content of the dialogue?
Large distance = strong subtext.
No distance (character says exactly what the gerund describes) = on the nose.

### Step 6 — Locate the Turning Point
Find the beat where the scene's value shift occurs. Does the dialogue earn
that turning point through the gerund sequence — or does it arrive without
adequate buildup?

## Output Format

If the script does not provide enough material to complete this analysis confidently, mark the output [INCONCLUSIVE] at the top of the file, describe what is missing or ambiguous, and flag it for human review before the pipeline continues.

Save as `19_beat_analysis.md`:

```
For each dialogue scene:

SCENE [X] — BEAT MAP:
Beat 1: [Character A gerund] / [Character B gerund]
Beat 2: [gerund] / [gerund]
...
Turning point: Beat [X] — [what shifts and why]

FLAT PASSAGES: [beats that repeat without progression]
SUBTEXT DISTANCE: [strong / weak — which beats are on the nose]
TURNING POINT EARNED: YES/NO — [explanation]

---

OVERALL DIALOGUE ASSESSMENT:
STRONGEST SCENE BEAT MAP: [which scene has the most shape and why]
FLATTEST SCENE: [which scene loops and needs restructuring]

PROBLEMS: [specific beats that are flat, on the nose, or unearned]
SUGGESTIONS: [concrete — "Scene 5, beats 3-5 are all Florence pleading /
Sebastian deflecting. By beat 3 this has stopped generating new information.
Beat 4 needs Sebastian to do something unexpected — not just deflect differently
but take a new action that forces Florence to change her strategy."]
TEACHING MOMENT: [why the gerund reveals what the literal speech hides —
what it means for dialogue to be a series of actions, not a series of statements]
```


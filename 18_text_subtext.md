# Skill 18 — Full Scene Text and Subtext Audit

## Purpose
Every great scene operates on two levels simultaneously: the TEXT (what is
literally happening — stated action, spoken words, visible behavior) and the
SUBTEXT (what is actually happening beneath — what characters truly want,
fear, and mean). A scene that only has text is shallow. A scene that only has
subtext is obscure. The skill is writing text that makes the subtext legible
without stating it.

Unlike the dialogue exercises (which focus on speech), this exercise audits
ALL layers of a scene: action, behavior, setting, objects, silence, AND dialogue.

## Inputs
- script.txt
- 15_scene_values.md
- 17_gap.md

## Instructions

If a required input file is missing or does not contain the expected content, halt immediately and report the missing input to the orchestrator — do not proceed with partial context.

### Step 1 — State the Text and Subtext for Each Key Scene
For key scenes (scenes that carry significant dramatic or thematic weight):
Write one sentence of text: what literally happens.
Write one sentence of subtext: what is actually happening beneath the surface.
If you cannot write the subtext sentence, the scene may not have one — flag it.

### Step 2 — Audit Each Layer
For each scene, examine:

**Dialogue**: Does the spoken exchange carry the surface topic while allowing
the subtext to be sensed? Is any line stating the subtext directly (on the nose)?

**Action and behavior**: What are characters physically doing? Does their
physical behavior carry the subtext independently of dialogue? A scene where
all subtext lives in speech and nothing is in the body is underwritten.

**Setting and objects**: Does the location or any significant object in the
scene carry thematic or subtext weight? Or is the setting neutral — present
but not working?

**Silence and gaps**: Where do characters NOT speak when they could? Silence
is often the loudest carrier of subtext. Are the silences doing work?

### Step 3 — Test the Balance
Remove all dialogue mentally. Can the subtext still be sensed from behavior,
setting, and action alone? If yes: well-layered. If no: too dependent on speech.

Remove all action and setting mentally. Does the dialogue carry the subtext
alone? If yes: the other layers are not contributing.

### Step 4 — Find the Subtext Surface Moment
Identify the moment in the scene where subtext comes closest to the surface —
where the distance between text and subtext is smallest. Is it at the turning point?
It usually should be.

## Output Format

If the script does not provide enough material to complete this analysis confidently, mark the output [INCONCLUSIVE] at the top of the file, describe what is missing or ambiguous, and flag it for human review before the pipeline continues.

Save as `18_text_subtext.md`:

```
For each key scene:

SCENE [X]:
TEXT: [one sentence — what literally happens]
SUBTEXT: [one sentence — what is actually happening beneath] / ABSENT

LAYER AUDIT:
- Dialogue: Layered / On the nose — [specific line if on the nose]
- Action/behavior: Carrying subtext / Not contributing — [specific]
- Setting/objects: Working / Neutral — [specific]
- Silence: Working / Absent — [specific]

BALANCE TEST:
- Without dialogue, subtext survives: YES/NO
- Without action/setting, dialogue carries it: YES/NO

SUBTEXT SURFACE MOMENT: [beat where text and subtext are closest]

---

OVERALL:
SCENES WITH FULL TEXT/SUBTEXT LAYERING: [count]
SCENES THAT ARE TEXT-ONLY (NO SUBTEXT): [list]
SCENES WHERE SUBTEXT IS PRESENT BUT INVISIBLE: [list]

PROBLEMS: [numbered, with scene and layer references]
SUGGESTIONS: [concrete — "Scene 5's alley sequence has strong subtext in the
dialogue but Florence's physical behavior is descriptively neutral. Her body
should be doing something that contradicts or deepens what she's saying —
even something small like the way she holds herself against the doorframe."]
TEACHING MOMENT: [why the scene that makes the audience feel they're perceiving
something unspoken is the scene they remember — and how all layers working
together creates that sensation]
```


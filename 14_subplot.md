# Skill 14 — Subplot Design Analysis

## Purpose
Subplots are secondary stories that begin in Act One and weave through the central
plot. They must INTERSECT with the central plot — not run parallel to it. A subplot
that runs parallel without intersecting splits the story down the middle. A subplot
that intersects at a crucial moment — either reinforcing the controlling idea or
ironically contradicting it — deepens the story's meaning.

For a short film, subplots are compressed or absent. If absent, note it.
If present, they must earn every moment they take.

## Inputs
- script.txt
- 02_controlling_idea.md
- 05_act_structure.md
- 13_negation.md

## Instructions

If a required input file is missing or does not contain the expected content, halt immediately and report the missing input to the orchestrator — do not proceed with partial context.

### Step 1 — Identify All Subplots
List every subplot — secondary story thread with its own arc.
For a short film, this may be minimal or absent. That is fine.

### Step 2 — Check Origins
Does each subplot begin in Act One? A subplot that starts in Act Two or later
will feel like an intrusion.

### Step 3 — Check Intersection
Does each subplot INTERSECT with the central plot at a crucial moment?
Not just run alongside it — actually affect it or be affected by it?
If no: it is a parallel story, not a subplot.

### Step 4 — Check Timing
When does each subplot end? It should climax and resolve BEFORE the central plot's
climax, or share the same climax. A subplot that extends past the central plot's
climax is pulling attention from the resolution.

### Step 5 — Check Thematic Function
Does the subplot reinforce the controlling idea (same argument from a different
angle) or ironically contradict it (complicating the argument with a counterexample)?
A subplot that is thematically neutral is missing an opportunity.

### Step 6 — Test Removal
If this subplot were removed entirely, would the central plot lose something
irreplaceable? If no, the subplot may not be earning its place.

## Output Format

If the script does not provide enough material to complete this analysis confidently, mark the output [INCONCLUSIVE] at the top of the file, describe what is missing or ambiguous, and flag it for human review before the pipeline continues.

Save as `14_subplot.md`:

```
SUBPLOTS IDENTIFIED: [list, or note if none present]

For each subplot:
SUBPLOT: [name/description]
- Begins in Act One: YES/NO
- Intersects central plot: YES/NO — [where and how]
- Ends before/at climax: YES/NO
- Thematic function: Reinforces / Contradicts / Neutral
- Removal test: Irreplaceable / Removable without loss

NO SUBPLOTS NOTE: [if the script has no subplots, assess whether any secondary
thread could add thematic depth without diluting the central story]

PROBLEMS: [numbered, specific]
SUGGESTIONS: [concrete]
TEACHING MOMENT: [Explain the difference between a parallel story and a subplot. Why intersection — not coexistence — is the test. The contrast: a story that splits into two parallel tracks loses focus; a subplot that crosses into the central plot at a crucial moment deepens the story's argument. Why a subplot that runs alongside without ever intersecting should be cut entirely, no matter how well written it is in isolation.]
```


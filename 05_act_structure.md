# Skill 05 — Act Structure Mapping
# 🔴 PIT STOP AFTER THIS EXERCISE

## Purpose
McKee's structural model: beats build scenes, scenes build sequences, sequences
build acts, acts build the story. Each level climaxes in a more significant value
change than the one below it. This exercise maps the full architecture of the
script and tests whether each structural beat is earning its turn.

For a short film, the structure is compressed but the same rules apply. A short
that skips its crisis or buries its inciting incident fails for exactly the same
reasons a feature does — it just fails faster.

## Inputs
- script.txt
- beat_sheet.txt
- 02_controlling_idea.md
- 03_story_spine.md

## Instructions

If a required input file is missing or does not contain the expected content, halt immediately and report the missing input to the orchestrator — do not proceed with partial context.

### Step 1 — Locate and Label Structural Beats
Working through the script and beat sheet together, identify and label:
- **Inciting Incident**: the event that radically upsets the protagonist's life
- **Act One Climax**: the reversal that ends Act One and locks in the central conflict
- **Midpoint** (if present): a complication or revelation that raises the stakes
- **Act Two Climax**: the reversal that forces the protagonist to the point of no return
- **Crisis**: the moment of irreconcilable choice before the climax
- **Climax**: the final, most extreme, irreversible change
- **Resolution**: what follows the climax

For a short film, some of these may compress into the same moment — note when that happens.

### Step 2 — Test Each Beat
For each structural beat:
- Is it actually present, or is it implied/skipped?
- Is it a decisive value reversal — more extreme than anything within its act?
- Is it irreversible? Can the story go back after this moment?

### Step 3 — Check Proportions
For each act (or act-equivalent in a short): does it feel proportionally weighted?
Is one section carrying too much story while another rushes?
In a short, even a two-minute section that drags is a problem.

### Step 4 — Trace the Spine Through Structure
Using the story spine from Exercise 3: is the protagonist's want driving each
structural beat? Does the inciting incident establish the want? Does the climax
resolve it?

### Step 5 — Test the Climax Against the Controlling Idea
The climax should prove the controlling idea. Ask: does what happens at the
climax demonstrate the argument the story is making? If not, either the climax
is wrong or the controlling idea needs revision.

## Output Format

If the script does not provide enough material to complete this analysis confidently, mark the output [INCONCLUSIVE] at the top of the file, describe what is missing or ambiguous, and flag it for human review before the pipeline continues.

Save as `05_act_structure.md`:

```
STRUCTURAL MAP:
- Inciting Incident: [scene/moment + value it upsets]
- Act One Climax: [scene/moment + reversal]
- Midpoint: [scene/moment + what it raises] OR [NOT PRESENT]
- Act Two Climax: [scene/moment + point of no return]
- Crisis: [the irreconcilable choice]
- Climax: [the final irreversible change]
- Resolution: [what follows]

BEAT TESTS:
- Each beat present: PASS/FAIL per beat
- Each beat decisive: PASS/FAIL per beat
- Each beat irreversible: PASS/FAIL per beat

PROPORTION ASSESSMENT: [which sections are heavy/light and why it matters]

SPINE THROUGH STRUCTURE: [does the want drive each beat?]

CLIMAX VS CONTROLLING IDEA: PASS/FAIL — [explanation]

PROBLEMS:
[Structural beats that are missing, weak, or misplaced — with scene references]

SUGGESTIONS:
[Concrete — "The crisis doesn't register as a genuine dilemma because X.
To earn it, Florence needs to face a choice between Y and Z in Scene 5."]

TEACHING MOMENT:
[Explain why each structural beat must be more extreme than the ones within it.
Why the climax proving the controlling idea is the test of whether the story
is about what you think it's about.]
```

## Note: Pit Stop
This exercise is followed by a pit stop. The orchestrator handles the pause and user review — your job is to complete the analysis, save the output, and report done.


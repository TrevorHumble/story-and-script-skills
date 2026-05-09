# Skill 02 — Controlling Idea Exercise

## Purpose
The controlling idea is the story's irreducible meaning: a single sentence naming
the value the climax brings into the world and the cause that produces it. It is
not a theme word ("love") or a subject ("grief and recovery") — it is an argument.
A claim about how life works, proven by the events of the story.

This runs second because it is the north star every downstream exercise uses.
Scene analysis, character tests, thematic mapping, subplot design — all of them
measure against the controlling idea. If this is wrong or unclear, the whole
analysis drifts.

After this exercise there is a pit stop. You will present the finding and wait
for the user to confirm or revise before proceeding.

## Inputs
- script.txt
- 01_genre_contract.md

## Instructions

If a required input file is missing or does not contain the expected content, halt immediately and report the missing input to the orchestrator — do not proceed with partial context.

### Step 1 — Find the Climax
Read the script to its end. Identify the climactic action — the final, most
decisive, irreversible event. Write it down in one sentence.

### Step 2 — Extract the Value
Ask: as a result of this climactic action, what value comes into the protagonist's
world? State it as a single charged word: love, freedom, destruction, isolation,
connection, survival, loss.

Is it positively or negatively charged at the end?

### Step 3 — Extract the Cause
Ask: what is the chief cause, force, or means by which this value arrives?
What brought it here — what did the protagonist do, fail to do, or discover?

### Step 4 — Compose the Controlling Idea
Write it as one sentence:
"[Value] [charges positive/negative] when [cause]."

### Step 5 — Test It
Run four tests:
1. Is it a complete sentence with a value AND a cause? If not, keep working.
2. Does the opening scene set up the conditions this idea will prove?
3. Does every major scene serve or complicate this argument?
4. Does the subplot support or ironically contradict it?

If any test fails, note which one and why.

### Step 6 — Surface Hidden Arguments
Read the script again with fresh eyes. Ask: is the story actually arguing something
different than what you wrote? Sometimes the script knows something the writer
hasn't consciously chosen yet. If you find a competing controlling idea, name it.

## Output Format

If the script does not provide enough material to complete this analysis confidently, mark the output [INCONCLUSIVE] at the top of the file, describe what is missing or ambiguous, and flag it for human review before the pipeline continues.

Save as `02_controlling_idea.md`:

```
CLIMAX: [one sentence description]
VALUE: [word + positive/negative charge]
CAUSE: [one sentence]

CONTROLLING IDEA: [the full sentence]

TEST RESULTS:
- Complete sentence: PASS/FAIL
- Opening sets up the argument: PASS/FAIL — [explanation]
- Major scenes serve the argument: PASS/FAIL — [which scenes don't and why]
- Subplot relationship: [supports / contradicts / unclear]

HIDDEN ARGUMENT (if found): [competing controlling idea + where it surfaces]

PROBLEMS:
[Numbered list — specific scenes or moments where the controlling idea breaks down]

SUGGESTIONS:
[For each problem: concrete direction — not "clarify the theme" but "the scene
where X happens is pulling the story toward Y argument instead. Consider Z."]

TEACHING MOMENT:
[Explain the difference between theme-as-word and theme-as-argument. Why the
controlling idea must be a sentence. Why finding it matters for every other decision.]
```

## Note: Pit Stop
This exercise is followed by a pit stop. The orchestrator handles the pause and user review — your job is to complete the analysis, save the output, and report done.


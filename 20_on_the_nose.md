# Skill 20 — On-the-Nose Dialogue Diagnosis
# 📋 ONE-PAGER SUMMARY AFTER THIS EXERCISE

## Purpose
On-the-nose dialogue is dialogue without subtext: characters saying exactly what
they mean, feel, and want. McKee: "What people say is always a tactic to get what
they want." People in conflict rarely express their true feelings — they use speech
as a weapon, a shield, or a distraction. On-the-nose dialogue assumes characters
speak sincerely at their most conflicted moments, which is the opposite of reality.

This diagnosis works in concert with the beat analysis from Exercise 19. Where
Exercise 19 maps the whole beat structure, this exercise zooms into specific
on-the-nose lines and finds the fix.

## Inputs
- script.txt
- 19_beat_analysis.md

## Instructions

If a required input file is missing or does not contain the expected content, halt immediately and report the missing input to the orchestrator — do not proceed with partial context.

### Step 1 — Mark On-the-Nose Lines
Read through the dialogue. Mark any line where the character is:
- Stating their exact emotion: "I'm angry at you."
- Stating their exact want: "I need you to help me."
- Stating their exact fear: "I'm scared of being alone."
- Explaining their subtext to the other character: "The real reason I'm here is..."

### Step 2 — Apply the Redundancy Test
For each marked line: if this line were cut entirely, could the audience still
infer the character's emotional state from the surrounding behavior and context?
If yes: the line is redundant AND on the nose. Both problems at once.

### Step 3 — Find the Real Want
For each on-the-nose line: what does the character ACTUALLY want in this moment?
What would they NOT say if they were a real person navigating this situation?

### Step 4 — Find the Tactic
What indirect approach — what tactic — would serve the same want without stating it?
Rewrite the line or exchange so the character pursues the want through action,
not declaration.

### Step 5 — Check Exposition for On-the-Nose Delivery
Look specifically for "As you know, Bob" lines — moments where characters tell
each other things they both already know purely for the audience's benefit.
These are on-the-nose exposition. Flag each one.

## Output Format

If the script does not provide enough material to complete this analysis confidently, mark the output [INCONCLUSIVE] at the top of the file, describe what is missing or ambiguous, and flag it for human review before the pipeline continues.

Save as `20_on_the_nose.md`:

```
ON-THE-NOSE LINES:
Scene [X], [Character]: "[exact line]"
- Real want: [what they're actually after]
- Redundancy test: YES — audience already knows / NO — this is needed
- Suggested rewrite direction: [what tactic would serve the same want indirectly]

[Repeat for each flagged line]

EXPOSITION PROBLEMS: ["As you know Bob" lines — list with scene references]

OVERALL:
COUNT OF ON-THE-NOSE LINES: [number]
MOST DAMAGING INSTANCE: [the line that most undercuts the scene — and why]

PROBLEMS: [numbered]
SUGGESTIONS: [concrete rewrites or rewrite directions — not just "add subtext"
but "instead of Florence saying 'I feel like I'm disappearing,' have her
look at her hands and say nothing. Let the beat carry it."]
TEACHING MOMENT: [why on-the-nose dialogue is not just weak writing but a
trust failure — it tells the audience what to feel rather than letting them
feel it. Why the indirect approach respects the audience's intelligence.]
```

## Note: One-Pager Summary
This exercise is followed by a one-pager summary and a user check-in. The orchestrator handles both — your job is to complete the analysis, save the output, and report done.


# Common Infrastructure — Story Pipeline

Read this file before running any orchestrator. It contains rules and protocols that apply to all phases of the pipeline.

---

## Agent spawning — the four non-negotiables

Every Agent call MUST:

1. **Use `subagent_type: "general-purpose"`**
2. **Pin `model: "opus"`** — pins Opus 4.6 regardless of the parent conversation's model. Without this, the agent inherits the parent's model and quality varies between runs.
3. **Include the OUTPUT STYLE block (below) verbatim** in the prompt
4. **Pass canonical staging from `directors_notes.md` as STAGING ONLY** — no intent or effect framing (see Show-Don't-Tell rule below)

Stage inputs into `outputs/staging/skill_NN/` before each call. Pass file paths in the prompt.

---

## OUTPUT STYLE block — paste verbatim into every agent prompt

```
## OUTPUT STYLE — required, non-negotiable

1. **Be concise.** Tight prose. Short sentences. Lead with the finding. No throat-clearing, no multi-clause hedging, no restating the question before answering.

2. **Define McKee jargon in plain English on first use.** When you first use a term like *controlling idea, true character, dimension, gap, beat, gerund, on-the-nose, the unsayable, scene value, negation of the negation, trialogue* — give a one-sentence plain-English definition first, then apply it. Don't assume the reader knows McKee.

3. **Teaching moment must follow this 4-part structure:**
   - **What this means in plain English** — define the principle without jargon
   - **Why it matters in any story** — the general craft reason
   - **How it operates in THIS script** — point at specific scenes/beats
   - **Takeaway for the writer** — one or two actionable sentences

4. **Problems and Suggestions: scene-specific and direct.** Each item starts with the scene name (and beat reference if relevant), names the issue in one sentence, then briefly explains the impact. Suggestions name a concrete intervention, not a vague direction.

5. **Internal reasoning can be loose. The OUTPUT DOCUMENT must be clean.** The user reads the output, not the chain of thought.
```

---

## Show-don't-tell — the rule that protects analysis integrity

When passing director's notes content into an agent prompt, **describe WHAT THE STAGING IS, not WHAT IT'S MEANT TO ACHIEVE.**

- No: "Sebastian's slow finger gesture is intended to feel intimate and to make Florence's permission visible as a chosen act."
- Yes: "Sebastian raises his thumb to Florence's lips. Holds. Eye contact. Florence's breathing visibly deepens. He slides his index finger in. He works the gum free."

**Why this matters.** Pre-loading intent corrupts analysis. An agent told "this is meant to feel intimate" will report back that it does — confirming the writer's hope rather than checking the page. An agent given only the staging will report what is actually legible.

**No value words** in agent-facing staging: avoid *powerful, intimate, rich, sophisticated, devastating, beautiful*, etc. Mechanical description only.

**No effect framing**: avoid *meant to, intended to, designed to, in order to, so that the audience...* The staging IS the intent; if it isn't legible, the staging needs to change.

The user-facing director's notes follow the same rule (see `templates/directors_notes_template.md`). The orchestrator passes excerpts straight through.

---

## Director's notes lifecycle

`directors_notes.md` is the canonical staging document. Treat it as authorial truth — it supersedes `script.txt` where they conflict.

**When to read it:** before staging inputs for any skill. The agent's understanding of "what's on the page" must include the directors_notes revisions.

**When to update it:** at every pit stop / one-pager / check-in where the user makes a staging decision. Append a new revision section using the template format (mechanical description + source citation). Do not delete superseded sections — mark them as superseded so history is visible.

**What goes in:** decided staging changes only. Open problems live in the "Open Problems" section at the bottom — surface them but don't propose solutions until the user decides.

**Source citation required.** Every revision section ends with `**Source:** [skill file or pit stop reference]`. This is how future-you traces why a decision was made.

---

## Stop protocol behavior

At each stop (pit stop, one-pager, check-in):

1. Surface findings from the recent skills (problems, contradictions, what's working)
2. Capture user decisions in `decisions_log.md`
3. Update `directors_notes.md` with any new staging changes
4. Confirm before continuing

---

## Decisions log

After each pit stop / check-in, append to `decisions_log.md`:

- **Quick table row** for every decision (date, skill/stop, decision, mechanical change, source)
- **Detailed entry** only when the table row can't carry the decision

The orchestrator does this; the user does not have to ask.

---

## Re-run protocol — dependency map

When a directors_notes change overturns an upstream finding, downstream skills may need to rerun. Use this map.

| If you change... | You must rerun... |
|---|---|
| Genre or controlling idea (01–02) | Everything from 03 onward |
| Story spine or act structure (03, 05) | 06–09, 14, 15, 16 |
| Inciting incident or crisis (06, 08) | 07, 15, 17 |
| Conflict levels or character dimension (09, 10, 11) | 12, 18, 19, 22 |
| Antagonism (12) | 14, 22, 23 |
| Subplot (14) | 15, 16, 17 |
| Scene values (15) | 16, 17, 18 |
| Any dialogue scene staging | 18, 19, 20, 21, 22, 23 |
| Final pass: any change | 24 (postmortem must rerun if anything earlier changed) |

### Cross-phase re-runs

If a re-run triggers skills in a different phase than the one you're currently in:

1. Complete the current phase's re-runs first
2. Note which downstream skills in other phases need re-running
3. Tell the user: "[Phase name] skills [list] need to rerun because [upstream change]. Run that phase's orchestrator next."
4. When starting the downstream phase for a re-run, skip the full prerequisite check — the user is continuing from a known state. Instead, verify only that the specific changed upstream outputs exist.

Re-run individual skills with the same staging-folder pattern as the first run. Mark the re-run output with a `## Re-run notice` block citing what triggered it.

---

## Surface problems, don't auto-propose solutions

When reporting back to the user from agent outputs:

- **Surface the problems** the agent flagged — name the scene, the issue, the impact
- **Do NOT auto-propose the agent's suggested solution** unless the user asks
- The user is a thinking partner, not a passive consumer; let them see the problem before being handed a fix

The agent's output document still contains its suggestions — the user can read them. The orchestrator's user-facing report leads with problems.

---

## Notes for the orchestrating agent

- **Confirm before destructive actions.** Re-runs that overwrite outputs need a one-line check with the user.
- **Don't summarize what the user can read.** When pointing the user at a finding, link the file and lead with the headline. The full detail is in the file.
- **Trust the staging folder pattern.** Every skill reads its inputs from `outputs/staging/skill_NN/`. Do not pass long quoted excerpts in the prompt when a file path will do.
- **Memory is your friend.** If you encounter feedback that should apply to future runs (output style, scope, tone), save it as a feedback memory.

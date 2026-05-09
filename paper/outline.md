# The Artist's AI Pipeline

**Working outline.** Status: in progress. Case study (Catalysis) in production through ~mid-2026.

---

## 1. Introduction

The dominant conversation about AI in filmmaking is about **generation** — Sora, Runway, Veo, Midjourney. This paper argues for a different model: AI as **orchestration** across the existing professional toolchain (Blender, DaVinci Resolve, Figma, version control). The artist makes every creative decision; the AI handles file movement, format translation, scene assembly, and analysis.

We demonstrate the model with a complete short-film production pipeline, illustrated with a case study (*Catalysis*).

## 2. Background and prior work

- **Generative video and image** (Sora, Runway, Veo, Midjourney) — output stage only
- **AI script analysis** (Coverfly, Greenlight, Scriptbook) — input stage only
- **AI VFX assistants** (Wonder Dynamics, Runway, etc.) — single mid-pipeline stage

What's missing: **the connective tissue** between stages — and that is exactly where LLM agents excel.

## 3. System architecture

End-to-end through-line:

1. **Script analysis** — McKee-based 24-skill LLM pipeline produces problems, suggestions, postmortem
2. **Decision board** — programmatic FigJam build from postmortem and director's notes
3. **Scene scaffolding** — Blender file generation with naming conventions matching the canonical beat structure
4. **Character placement** — headless Blender Python appends rigs into the right scenes
5. **Multi-pass rendering** — headless batch render with EXR pass output
6. **Timeline assembly** — DaVinci Resolve Python API builds the project, imports media, lays the timeline
7. **Compositing handoff** — Fusion clips wired up; human takes over for the creative comp work

## 4. Design principles (the methodology contribution)

- **Show-don't-tell prompting** — describe what staging IS, not what it's MEANT to do; pre-loaded intent corrupts analysis
- **Canonical documents across tool boundaries** — director's notes survive from McKee analysis through to render schedules
- **Stop protocols and pit stops** — human judgment is load-bearing at decision-anchoring moments
- **Surface problems, don't auto-propose solutions** — keeps the artist in the creative seat
- **Mechanical staging descriptions** — value words (*intimate, powerful, devastating*) banned from agent prompts; concrete actions only
- **Orchestrator pattern** — one master skill coordinates spawned sub-agents with isolated context
- **Stay in tools that script natively, don't add ones that don't** — DaVinci Resolve free version cannot run headlessly (Studio-only feature). When tool A doesn't expose its API, the right move is often tool B inside the same ecosystem (Blender's VSE does the assembly job and is fully scriptable in the same Python environment as the renderer). Adding tools to the pipeline carries hidden cost; consolidating around tools with strong APIs collapses complexity.

## 5. Case study: *Catalysis*

Production walk-through of an animated short. Per stage: what was built, time invested, what the AI surfaced or assembled, what required human craft. Honest about both wins and failures.

## 6. What stays human (and should)

- Performance direction and acting choices
- Final compositing — the creative comp work, not the wiring
- Color grading and look development
- Sound design and the mix
- Taste-level decisions across all stages

The pipeline is designed to *defend* the human creative seat, not erode it.

## 7. Limitations

- Sample size of one
- Single artist, single toolchain (Blender + Resolve + Figma + Claude)
- Specific format (short animated film) — applicability to live action, feature length, series TBD
- Snapshot in time — LLM capabilities and tool APIs change rapidly

## 8. Reproducibility

- Public skills framework at v2 (story-and-script-skills repo, MIT license)
- Templates for intake, director's notes, decisions log, lessons file
- Documented orchestrator pattern others can fork
- The case study analysis (private) is reproducible by anyone running the public skills against their own script

## 9. Future work

- Extending the orchestration to sound design (Fairlight automation)
- Distribution and festival workflow integration
- Multi-artist collaboration (the canonical document model scales naturally to teams)
- The pipeline as a teaching tool — student filmmakers as a target audience

---

## Notes for drafting

- Section 4 is the strongest contribution and should be drafted first; it stands alone as a methods piece.
- Sections 3 and 5 generate naturally as the case study completes — capture wins/failures/timing per stage as we go.
- Section 6 is the section reviewers will most want to attack ("AI shouldn't replace artists") — defend it explicitly with concrete examples of where the pipeline declines to take creative agency.
- Title is the framing weapon. *The Artist's AI Pipeline* — possessive, infrastructure-not-author, counter-stance to "AI artist."

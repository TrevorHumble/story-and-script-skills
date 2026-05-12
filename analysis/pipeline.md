# Analysis Pipeline — Parent Orchestrator

> Part of the [Story Pipeline](../README.md). This document ties together the five analysis phases. Start here for a full analysis run, or jump to any phase if you already have its prerequisites.

Read [`common.md`](../common.md) before proceeding. It contains agent spawning rules, the OUTPUT STYLE block, show-don't-tell staging rules, and the director's notes / decisions log lifecycle.

---

## The five phases

| Phase | Folder | Skills | Question it answers |
|---|---|---|---|
| 1 | [Foundation](01_foundation/orchestrator.md) | 01–05 | What IS this story? |
| 2 | [Narrative Arc](02_narrative_arc/orchestrator.md) | 06–08 | What HAPPENS? |
| 3 | [Character](03_character/orchestrator.md) | 09–13 | WHO are these people under pressure? |
| 4 | [Scene Craft](04_scene_craft/orchestrator.md) | 14–23 | HOW do individual scenes work? |
| 5 | [Synthesis](05_synthesis/orchestrator.md) | 24 + FigJam | What's the verdict, and what does the writer take to rewrite? |

---

## Phase dependencies

```
Phase 1 (Foundation)
  ↓
Phase 2 (Narrative Arc)     Phase 3 (Character)
  needs: 02, 05                needs: 02, 03, 05
  ↓                            ↓
  └──────────┬─────────────────┘
             ↓
Phase 4 (Scene Craft)
  needs: 02, 05, 11, 13
             ↓
Phase 5 (Synthesis)
  needs: all prior outputs
```

**Phase 3 does not depend on Phase 2.** Both depend only on Phase 1. Run them in the order listed (McKee's pedagogical order: events before characters), but if a re-run is triggered in Phase 3 only, Phase 2 does not need to rerun.

---

## Full pipeline run

1. Confirm setup: `script.txt`, `beat_sheet.txt`, `intake.md`, `directors_notes.md`, `decisions_log.md`, `outputs/` directory. If any are missing, halt.
2. Run each phase in order. Each phase orchestrator handles its own skill sequencing, stop protocols, and handoffs.
3. At each stop, surface findings and capture decisions before continuing.
4. After Phase 5, the analysis is complete. The FigJam beat board and director's notes are the primary deliverables.

---

## Single-phase entry

Any phase can be run independently if its prerequisites exist. Each phase orchestrator lists exactly which output files it needs and where they come from. If you're entering mid-pipeline (e.g., you already have a controlling idea and act structure and want to start at Phase 3), the orchestrator will verify the prerequisite files exist before beginning.

---

## Cross-phase re-runs

See the full dependency map in [`common.md`](../common.md). When a re-run is triggered:

1. Complete re-runs within the current phase first
2. Note which skills in downstream phases need re-running
3. Tell the user which phase to invoke next and which skills within it need to rerun
4. Re-runs always flow downstream, never upstream

---

## What comes after analysis

The analysis produces a FigJam beat board and finalized director's notes. From there:

- [Scene Scaffolding](../scaffolding/orchestrator.md) translates the beat board into Blender scene files
- [Render & Assembly](https://github.com/TrevorHumble/Blender-Skills) takes posed scenes and produces a video deliverable

# Story Pipeline

An end-to-end pipeline for screenplays: from Robert McKee story analysis through FigJam beat board to Blender scene scaffolding. AI agents handle the mechanical work; the storyteller makes every meaningful decision.

This process is deliberately multi-hour. You can't automate art about the human condition, but you can give storytellers better tools. The agents surface problems and teach craft concepts in plain English. The stop protocols — pit stops, one-pagers, check-ins — are where the real work happens: the writer decides what to change, what to keep, and what to investigate further.

## Pipeline phases

| Phase | Folder | What it does |
|---|---|---|
| **Analysis** | [`analysis/`](analysis/) | 24 McKee-based skills across 4 orchestrated phases — examines genre, character, structure, dialogue. Produces a FigJam beat board and finalized director's notes. |
| **Scene Scaffolding** | [`scaffolding/`](scaffolding/) | Reads the beat board and director's notes, creates one Blender scene file per beat with characters appended. Mechanical only — the artist poses, lights, and cameras. |
| **Render & Assembly** | [Blender-Skills repo](https://github.com/TrevorHumble/Blender-Skills) | Takes posed scenes and produces a video deliverable. Headless rendering with mid-render vision verification, VSE assembly. Lives in the Blender-Skills repo. |

Each phase can be run independently. Someone might bring their own script and just want a FigJam board. Someone else might bring their own beat board and just want scaffolded scene files. The phases are aware of each other — each orchestrator names the prerequisites and points to where they come from — but none requires the others to have run.

## Quick start

1. Drop `script.txt` and `beat_sheet.txt` in the project root.
2. Copy `templates/intake_template.md` to `intake.md` and fill it in.
3. Copy `templates/directors_notes_template.md` to `directors_notes.md` (carry over the Authorial Intent line from intake).
4. Copy `templates/decisions_log_template.md` to `decisions_log.md`.
5. Start with [`analysis/foundation.md`](analysis/foundation.md) — it tells you everything else.

## Shared infrastructure

[`common.md`](common.md) contains rules that apply across all phases: agent spawning, the OUTPUT STYLE block, show-don't-tell staging, director's notes lifecycle, decisions log protocol, and the re-run dependency map. Every orchestrator reads it first.

## Repository structure

```
common.md                    # Shared infrastructure
analysis/                    # 24-skill McKee analysis (4 phases)
  foundation.md              #   Phase 1: skills 01-05
  character.md               #   Phase 2: skills 06-13
  structure_pacing.md        #   Phase 3: skills 14-17
  dialogue.md                #   Phase 4: skills 18-24 + FigJam
  skills/                    #   The 24 skill files
scaffolding/                 # Scene scaffolding
  orchestrator.md            #   Workflow orchestration
  01_scene_scaffolding.md    #   The scaffolding skill
  scripts/                   #   Reference Python scripts
templates/                   # Project setup templates
```

## Companion repo

The [Blender-Skills](https://github.com/TrevorHumble/Blender-Skills) repo contains production-tested Blender workflows including the Render & Assembly skill that picks up after scene scaffolding.

## Required inputs

- `script.txt` — the screenplay
- `beat_sheet.txt` — beat-level summary

These files are gitignored by default (per-script content stays local).

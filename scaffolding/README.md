# Scene Scaffolding

Takes a FigJam beat board and director's notes — whether produced by the [analysis pipeline](../analysis/README.md) or built independently — and creates one Blender scene file per canonical beat with characters appended at default offset positions.

Mechanical scaffolding only. The script never decides where a character stands, what the camera sees, or how the scene is lit. Those decisions are the artist's.

## How to use

See the [orchestrator](orchestrator.md) for the full workflow, prerequisites, and handoff to rendering.

## Contents

| File | Purpose |
|---|---|
| [orchestrator.md](orchestrator.md) | Workflow orchestration, prerequisites, handoff |
| [01_scene_scaffolding.md](01_scene_scaffolding.md) | The scaffolding skill — 8 steps from board extraction to batched scene files |
| [scripts/](scripts/) | Reference Python scripts for character inspection, appending, and offset |

## What comes next

After scaffolding, the artist poses, lights, and cameras each scene. When scenes are ready to render, the Render & Assembly skill lives at [TrevorHumble/Blender-Skills](https://github.com/TrevorHumble/Blender-Skills).

# Scene Scaffolding Phase

> Part of the [Story Pipeline](../README.md). You can run this phase independently if you have the prerequisites below — you don't need to have run the analysis pipeline if you already have a beat board and director's notes from another source.

This phase translates a FigJam beat board and director's notes into Blender scene files: one `.blend` per canonical scene, with the right characters appended at default offset positions. The artist opens each file and starts posing, camera-blocking, and lighting.

Mechanical scaffolding only. The script never decides where a character stands, what the camera sees, or how the scene is lit. Those decisions are the artist's.

---

## Read first

Read [`common.md`](../common.md) for agent spawning rules. The show-don't-tell and surface-problems-don't-propose rules apply here too — production scaffolding is mechanical translation, not creative decision.

---

## Where you left off

The following must exist before starting this phase:

| Prerequisite | Produced by |
|---|---|
| FigJam beat board (URL or screenshot) | [Analysis — Dialogue](../analysis/dialogue.md) phase, or built independently |
| `directors_notes.md` | Analysis pipeline, or authored independently |
| Character source `.blend` files | Artist's rig library |
| A starting `.blend` template | Artist's preferred scene starting point |
| Path to Blender executable | System install (e.g. `C:\Program Files\Blender Foundation\Blender 5.1\blender.exe`) |

If the FigJam board or director's notes are missing, halt and ask.

---

## Skill

| # | Skill | Summary |
|---|---|---|
| 01 | [Scene Scaffolding](01_scene_scaffolding.md) | Extract scene structure from the board, create scene files from a template, inspect and append characters, test one scene, batch the rest |

The skill has 8 steps with a built-in "test before batch" checkpoint at Step 6.

---

## Reference scripts

| Script | Purpose |
|---|---|
| [`scripts/inspect_character.py`](scripts/inspect_character.py) | Recon character `.blend` structure before appending |
| [`scripts/append_characters.py`](scripts/append_characters.py) | Append named character collections with `bpy.data.libraries.load()` |
| [`scripts/offset_characters.py`](scripts/offset_characters.py) | Translate appended characters to avoid world-origin overlap |

These are reference implementations — paths to your project, character rigs, and Blender executable need to be edited at the top of each.

---

## Handoff

After this phase completes:

- A folder of scaffolded `.blend` scene files, one per canonical beat
- Characters appended and offset, ready for the artist to pose

**What happens next:** The artist poses, lights, and cameras each scene. This is the creative work — it takes as long as it takes.

**When scenes are posed and lit:** The Render & Assembly skill lives at [TrevorHumble/Blender-Skills](https://github.com/TrevorHumble/Blender-Skills). It takes the posed scene files and produces a video deliverable through headless rendering with mid-render vision verification and VSE assembly.

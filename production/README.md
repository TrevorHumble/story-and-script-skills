# Production Skills

Skills that come **after** the story analysis pipeline ends. Where the analysis skills (`01_genre_contract.md` through `24_postmortem.md`) audit a script and surface its problems, the production skills take the canonical artifacts (director's notes, postmortem, FigJam beat board) and turn them into the files an artist actually opens to start animating.

Same design principles as the analysis skills:
- **Show-don't-tell.** Production scaffolding is mechanical translation. Never pre-pose, pre-camera, or pre-light. Those decisions are the artist's.
- **Test before batching.** One scene first to validate, then loop.
- **Append, don't overwrite.** Scenes flagged ` - complete` are protected from automation.
- **Stay in tools that script natively.** Blender's Python API for everything from scaffolding to rendering to VSE assembly. No tools added that don't expose an API.

## Skills

- [`01_scene_scaffolding.md`](01_scene_scaffolding.md) — Reading the FigJam beat board and the director's notes, then creating one Blender scene file per beat with characters appended at default offset positions.
- [`02_render_and_assembly.md`](02_render_and_assembly.md) — Sequential per-scene headless rendering with verification, then Blender VSE assembly into a final video deliverable. Compositing is explicitly deferred to a future skill.

## Reference scripts

[`scripts/`](scripts/) holds the actual Python and Bash used by the skills. They are reference implementations — paths to your project, character rigs, and Blender executable will need to be edited at the top of each file.

| Script | Purpose |
|---|---|
| `inspect_character.py` | Print the collection / object structure of a character `.blend`. Run before appending so you know what to target. |
| `append_characters.py` | Append named character collections into the open scene. Parameterized by command-line args. |
| `offset_characters.py` | Translate appended character collections so they are not overlapping at world origin. |
| `render_scene.py` | Render the open scene to a per-scene PNG sequence. Defaults tuned for animatic speed (50% res, EEVEE). |
| `render_all.sh` | Bash wrapper that runs `render_scene.py` against every scene file in canonical order. |
| `assemble_vse.py` | Stitch every rendered scene folder into one Blender VSE timeline, save as a project file. |

## Status

This skill set is **growing alongside an in-progress short film** ([Catalysis](https://github.com/TrevorHumble/catalysis-analysis), private). Skills will be added as production stages are validated against real work. Current coverage: scene scaffolding. Future: pose blocking aids, camera template scaffolds, render queue management, sound design integration.

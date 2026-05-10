# Production Skill 02 — Headless Rendering and VSE Assembly

## Purpose

Take a folder of scaffolded, posed Blender scene files (the output of Production Skill 01 + the artist's posing work) and produce a deliverable video file. This is the final mechanical step before delivery: no creative decisions are made here; the artist's poses, cameras, and lighting are simply executed at render time, then stitched together in canonical order.

This skill is **deliberately conservative**. Rendering is the slowest mechanical step in the pipeline, and failure recovery costs the most time. We render scenes **one at a time, in canonical order**, verify each scene before continuing to the next, and stop immediately on failure. The opposite (render everything in parallel, hope for the best, debug at the end) is faster on the happy path but catastrophically slower the moment anything breaks. For indie animation where one tool, one machine, and a single artist's attention all coordinate, sequential-with-verification is the right tradeoff.

## Scope and what is deliberately deferred

**Included:**
- Pre-flight checks per scene (camera, frame range, render settings)
- Sequential per-scene rendering to image sequences
- Per-scene render verification before moving on
- Blender VSE assembly of the rendered sequences into one timeline
- Watch-v1, identify-fixes, re-render, re-assemble loop
- Final export to a video file

**Deferred to future skills:**
- **Per-scene compositing.** For an animatic rendered with the Workbench engine (clay-look, unshaded), no compositing is needed — there are no passes to combine, no depth-of-field to apply, no atmospherics. For the final film, each scene gets its own compositor node tree consuming its own multilayer EXR. That is a separate, harder skill (Production Skill 03 or later). **Do not attempt compositing inside this skill.**
- **Audio mixing.** Animatic scratch audio (if any) is dropped into the VSE manually after assembly. Final film sound design happens in a dedicated DAW pass (Blender's Fairlight equivalent or external).
- **Color grading.** Global grade applied at the VSE level happens in a future delivery skill. For animatic, we accept the engine's default look.

If the artist asks for compositing or sound design inside this skill, **do not attempt it inline**. Stop, name the work that's outside scope, and defer to a future skill or a manual pass.

## Inputs

- A folder of Blender scene files in canonical naming convention (e.g., `Act.1-Scene.1-Apartment - complete.blend` through `Act.3-Scene.1-ApartmentFinal.blend`)
- Each scene file must have:
  - An active camera positioned for the shot (artist's responsibility)
  - Frame range (`scene.frame_start`, `scene.frame_end`) set to the scene's intended duration
  - Lighting set up (or, if Workbench engine, lighting is irrelevant — Workbench has its own simple shading)
  - Render settings consistent with project standards (resolution, frame rate)
- Path to the Blender executable (e.g., `C:\Program Files\Blender Foundation\Blender 5.1\blender.exe`)
- An output directory for rendered image sequences
- A target file path for the assembled VSE project
- A target file path for the final exported video

## Stop protocols (formal user check-ins)

This skill has **five required check-ins** with the artist. Do not advance past any of them autonomously without confirmation.

| Check-in | When | What's being confirmed |
|---|---|---|
| **CI-1: Pre-flight** | Before Step 1 | Each scene's camera, frame range, lighting, and render settings are correct. The artist has opened each scene at least once and confirmed it is render-ready. |
| **CI-2: Settings lock** | Before Step 2 | The chosen render engine, resolution, frame rate, and output format are agreed and frozen for this render pass. Changing settings mid-render means re-rendering scenes already done. |
| **CI-3: Mid-render checkpoint** | After every 3rd scene completes | Spot-check the rendered sequences. Frame 1 of the most recent scene should look right (correct camera, characters present, lighting reasonable). If anything looks broken, stop the run and debug before continuing. |
| **CI-4: Pre-assembly** | Before Step 4 | Every scene rendered successfully. Frame counts match expected durations. No scene accidentally rendered to 1 frame because frame range was misset. The artist agrees the renders are ready to assemble. |
| **CI-5: Watch-v1 review** | After Step 5 | The artist watches the assembled v1 end-to-end and names which scenes (if any) need re-rendering or re-blocking. Iteration loop runs only on flagged scenes. |

Each check-in is a hard stop. The orchestrating agent surfaces what needs confirming and waits for an explicit "go" from the artist. No proceeding without it.

## Instructions

### Step 1 — Pre-flight every scene (CI-1 happens after this)

For each scene file in canonical order, run a non-destructive inspection that prints:

- Active camera name (or `[NONE]` — this is a blocker)
- Frame start / frame end / total frame count
- Render engine currently set
- Resolution X × Y at current `resolution_percentage`
- Number of objects in the active scene
- Whether the named character collections (Florence, Sebastian, etc.) are present

Output a table (one row per scene) so the artist can scan it and spot anomalies. Common things this catches:
- Scene without a camera (or camera not set as active)
- Scene with the wrong frame range (e.g., still inheriting placeholder's 1-250 when artist intended a 4-second beat)
- Scene with a stale render engine (e.g., still on Cycles when project standard is Workbench)
- Missing characters that should be present per the director's notes

**CI-1 pause:** Artist reviews the table, fixes anomalies in their copies of the scene files, and confirms when all scenes are pre-flight clean. Do not proceed to Step 2 without this confirmation.

### Step 2 — Lock render settings (CI-2 happens after this)

Choose, name, and document for this render pass:

- **Engine** —
  - **Workbench**: animatic stage. Clay/solid look. No shaders, no lighting calculation. Fastest. **No compositing needed.**
  - **EEVEE / EEVEE Next**: lookdev or fast final. Real-time rasterizer with materials and lighting. Fast. Compositing supported but not required.
  - **Cycles**: photoreal final film. Pathtracer. Slow. Compositing strongly recommended for cleanup.
- **Resolution percentage** — `50` for animatic (half-res), `100` for final
- **Frame rate** — typically 24 fps, must match project standard
- **File format** — `PNG` for sequences (lossless, easy to re-frame), or `FFMPEG` for direct video output (cheaper storage, harder to fix one frame). For sequential per-scene rendering, **PNG sequences are recommended** — they let you re-render a single broken frame without redoing the whole scene.
- **Color management view transform** — note what's set; affects how Workbench/EEVEE results read

**CI-2 pause:** Artist confirms the settings before any rendering starts. Once confirmed, any settings change during the run requires re-rendering already-done scenes.

### Step 3 — Render scenes one at a time, in canonical order (CI-3 happens periodically)

Loop through the scenes in canonical sort order (`Act.1-Scene.1...` first, `Act.3-Scene.1` last). For each scene:

1. Open the scene in headless Blender (`blender --background scene.blend --python render_scene.py -- output_root`)
2. Apply the locked settings from Step 2 (the render script does this)
3. Render the full frame range to `output_root/<scene_label>/<scene_label>_####.png`
4. After Blender exits, verify:
   - Output folder exists and contains the expected number of PNG files (`frame_end - frame_start + 1`)
   - Frame 1 file size > 0 and reads as a valid PNG
   - Last frame file size > 0 and reads as a valid PNG
5. If verification fails: **STOP THE RUN.** Do not continue to the next scene. Surface the failure to the artist with the scene name and what failed.
6. Otherwise, log the scene as done and continue.

**Why sequential, not parallel:** A failed scene that wastes 10 minutes of render time is recoverable. A failed batch that wasted 4 hours of render time across 14 scenes (and the failure was something fixable like a missing camera) is a bad evening. Sequential renders trade some wall-clock time for the ability to catch a problem at scene 2 instead of scene 14.

**CI-3 pause:** Every 3rd scene, spot-check by opening the most recent scene's frame 1 and frame N/2 in an image viewer. Confirm they look right. If they don't, stop and debug.

### Step 4 — Pre-assembly verification (CI-4 happens after this)

After all scenes have rendered, generate a summary table:

| Scene | Expected frames | Actual frames | Frame 1 OK | Last frame OK | Status |
|---|---|---|---|---|---|
| Act.1-Scene.1-Apartment | 96 | 96 | ✓ | ✓ | READY |
| ... |

Any row that isn't `READY` is a blocker. The artist either re-renders the broken scene before assembly, or accepts it knowing the assembly will be incomplete.

**CI-4 pause:** Artist confirms the table before assembly. No assembly until every row is `READY` or explicitly accepted.

### Step 5 — Assemble VSE timeline

Open a new empty Blender file. For each rendered scene folder (in canonical sort order — alphabetical sort works because of the `Act.N-Scene.N` naming):

1. Add an Image Strip to the VSE timeline at channel 1
2. Point it at the first frame of the sequence; append the rest of the frames
3. Place each strip end-to-end starting at frame 1 of the timeline
4. Set scene `frame_start = 1` and `frame_end = total length`
5. Pre-configure the timeline render output: MP4, H.264, target output path
6. Save as the assembly project file

The artist now opens this project, switches to the Video Editing workspace, and watches the cut.

### Step 6 — Watch v1 and identify fixes (CI-5)

The artist watches end-to-end and produces a list:
- Which scenes look right
- Which scenes need re-rendering (e.g., character pose was wrong, camera was off)
- Which scenes need re-blocking (more substantial — pose is wrong creatively, not just technically)

**CI-5 pause:** Artist names the fix list. Re-block work happens outside this skill (back to Production Skill 01 or future skills). Re-render work loops back to Step 3 for the named scenes only.

### Step 7 — Iterate (re-render flagged scenes only)

For each scene flagged in CI-5:
1. Artist updates the scene's `.blend` (re-poses, re-cameras, etc.)
2. Re-run Step 3 on that scene only — the per-scene output folder is overwritten in place
3. Re-open the assembly project in Blender — VSE strips refresh from disk automatically since they point to the same folder

No need to re-assemble from scratch. The VSE strip references survive re-renders cleanly because the file paths and naming conventions don't change.

### Step 8 — Final export

From the assembly project:
1. Confirm the timeline output path includes a version tag and date (e.g., `animatic_v1_2026-05-15.mp4`) so the artist can keep multiple iterations side-by-side
2. `File > Render > Render Animation` (or `bpy.ops.render.render(animation=True)` if scripting)
3. Wait for the FFMPEG export to complete
4. Verify the final file plays end-to-end
5. Deliver

## Standards

- **Sequential per-scene rendering only.** Do not run multiple Blender instances in parallel for this skill. The verification-per-scene safety net depends on serial execution.
- **PNG sequences, not direct-to-video.** A broken frame is fixable in a sequence; a broken video file is rerender-from-scratch.
- **Per-scene output folders.** Never let two scenes write into the same folder. Re-renders must overwrite cleanly without colliding with sibling scenes.
- **Naming convention preserved end to end.** The scene file's name flows through to the render folder name flows through to the VSE strip name. Don't rename anything mid-pipeline; debugging a strip-to-source mapping later is painful.
- **Version + date in final output filename.** No overwriting prior versions silently.
- **Compositing is deferred.** If anyone tries to add comp work inside this skill, refuse and point at the future Production Skill 03.
- **Re-render flagged scenes only.** Don't re-render the full film just because one scene was wrong.

## Failure modes to anticipate

| Symptom | Likely cause | Action |
|---|---|---|
| Scene renders 1 frame instead of N | Frame range never set; still on placeholder defaults | Stop, fix `frame_start`/`frame_end` in the .blend, re-run Step 3 for that scene |
| Scene renders but frames are all black | No active camera, or camera is below ground / inside an object | Open the scene, check `bpy.context.scene.camera`, fix in Blender, re-render |
| Render starts but `bpy.ops.render.render()` errors with "no camera" | Same as above | Same fix |
| Output folder is empty after render | Output filepath wasn't set, or path has invalid characters | Inspect `scene.render.filepath`; fix the render script's path handling |
| Workbench renders look fine but EEVEE/Cycles look wrong | Materials missing or shaders not assigned | This skill stops here. The artist needs to fix shading. Out of scope. |
| VSE assembly produces a project that opens empty | `discover_scene_sequences()` couldn't find PNGs in the expected layout | Verify the render output folder structure matches what `assemble_vse.py` expects |
| Final exported video skips frames or has wrong duration | VSE timeline `frame_end` was set incorrectly during assembly | Re-run Step 5; verify the cumulative frame count math |
| Final exported video has audio drop-outs | This skill doesn't handle audio | Out of scope. Add scratch audio manually in VSE before final export. |

## Teaching Moment

**What this means in plain English.** Rendering is the slowest mechanical step in animation production, and the one where automation is most tempting and most dangerous. Tempting because it's pure file processing — no creative decisions to make. Dangerous because failures compound: a problem that takes 30 seconds to fix at scene 2 takes 40 minutes to fix at scene 14, because every scene since scene 2 has to be re-rendered.

**Why it matters in any production.** The instinct in software engineering is "parallelize the slow thing." That instinct is wrong here. The right move for indie animation is the opposite: serialize the slow thing, verify between each step, and accept the wall-clock cost in exchange for short failure-recovery cycles. One artist with one machine and one render queue does not have the redundancy that justifies parallel rendering — they have a single pipe of attention, and a parallel render that breaks halfway leaves them with no way to know which scenes are good and which need redoing.

**How it operates here.** This skill takes 14 scenes and renders them in order, one at a time, with a verification step between each. The artist gets check-ins at pre-flight, settings-lock, every 3 scenes during render, before assembly, and after watching v1. At every check-in the artist can stop the run, fix a problem, and resume from where it failed — not from scratch. The total wall-clock time is essentially the same as a parallel run when nothing fails (one machine renders one scene at a time either way), but the failure-recovery time is dramatically lower.

**Takeaway for the practitioner.** Define the boundary between mechanical and creative early, defend it, and accept that mechanical doesn't mean "fire and forget." The mechanical steps are mechanical; the *workflow around them* still requires human attention at meaningful checkpoints. Build the check-ins in. Trust them.

---

Follow the orchestrator's OUTPUT STYLE block when reporting back to the user — concise, scene-specific, surface problems don't auto-propose solutions.

# Production Skill 01 — Scene Scaffolding from the FigJam Beat Board

## Purpose

Take the FigJam beat board (final artifact of the McKee analysis pipeline) and the director's notes (canonical authorial state), and produce one scaffolded Blender scene file per beat — with the right characters appended at default offset positions, ready for the artist to start posing, camera-blocking, and lighting.

Mechanical scaffolding only. The script never decides where a character stands, what the camera sees, or how the scene is lit. Those decisions are the artist's.

## Inputs

- The FigJam beat board (URL, or screenshot if MCP rate-limited)
- `directors_notes.md` (canonical staging document)
- A starting `.blend` template (whatever the artist's preferred scene starting point is — could be empty, could have a default ground plane and lighting)
- Character source files — one `.blend` per character with a clean top-level collection
- Path to Blender executable (e.g. `C:\Program Files\Blender Foundation\Blender 5.1\blender.exe`)

## Instructions

### Step 1 — Extract the canonical scene structure from the FigJam board

Read the middle column of the board, top to bottom. For each card extract:

- Scene **order** (vertical position in the column)
- Scene **name** (the location, e.g. "Beach", "BlackVoid")
- Scene **status** — KEPT / CHANGED / NEW (color tag) / [REMOVED-inline] for archaeological markers the artist has placed within the sequence
- Scene **act** (from the act-divider headers)
- Which **characters appear** — derive from the card body text and cross-check `directors_notes.md`

If the FigJam board can't be queried directly (rate limits), fall back to a screenshot and transcribe.

### Step 2 — Establish a naming convention

If a precedent file exists (e.g. the artist has already named one scene), match its convention. Otherwise default to:

```
Act.[N]-Scene.[N]-[Name].blend
```

- Single-word PascalCase location name (e.g. `Apartment`, `BakedBean`, `BlackVoid`)
- Disambiguate repeated locations by suffix (`Apartment`, `ApartmentReturn`, `ApartmentFinal`)
- When a scene is fully built and locked, append ` - complete` to the filename so automation skips it (`Act.1-Scene.1-Apartment - complete.blend`)

### Step 3 — Create the scene files from a template

- Copy the template once per canonical scene with the new names
- For scenes that already exist from a prior draft: replace the placeholder with the real build, then rename to match the canonical convention
- Mark already-built scenes with the ` - complete` suffix so subsequent steps don't touch them

### Step 4 — Inspect character source files (recon before append)

Before any append operation, run a small Python script in headless Blender that prints the collection and top-level object structure of each character source `.blend`. Don't guess at collection names.

See [`scripts/inspect_character.py`](scripts/inspect_character.py) for a reference implementation. It prints:
- Scenes
- Top-level collections (and object counts)
- All collections (including nested)
- Armatures
- Top-level objects in the active scene

### Step 5 — Write a parameterized append script

The script takes character names as command-line args and appends the right collections from the right source files. See [`scripts/append_characters.py`](scripts/append_characters.py).

Key API: `bpy.data.libraries.load(blend_path, link=False)` as a context manager, with `data_to.collections = [collection_name]`. After the context exits, link the collection into `bpy.context.scene.collection.children`.

Rename the appended collection to a meaningful name (e.g. `character1` → `Florence`) so the artist doesn't have to decode the rig file's internal naming.

### Step 6 — TEST on one scene first

Run the append on a single scene before batching. Verify:
- File size grew (signal of successful append — empty scenes are ~100 KB, an appended character is several MB)
- No errors in the Blender stdout
- The collection name landed correctly

If this fails, do not batch. Debug first.

### Step 7 — Batch on the remaining scenes

Once the test passes, loop through the remaining non-completed scenes. Pass the right character args per scene (some scenes may need only one character, others two or more).

Skip scenes flagged ` - complete`.

### Step 8 — Mechanical positioning only

Default `bpy.data.libraries.load` puts everything at world origin. Two characters appended into the same scene will visually overlap.

The mechanical fix: translate each character's collection by a small offset (e.g. ±1m on X). See [`scripts/offset_characters.py`](scripts/offset_characters.py).

**What you do NOT do:**
- Auto-pose any character (creative)
- Add a camera at any specific angle (creative)
- Add lighting beyond a default (creative)
- Pre-arrange characters in scene-specific positions (creative — the artist will move them based on the staging)

The scaffolding's job ends at "two characters in the scene, not overlapping, ready to pose." Everything beyond that is the artist's craft.

## Output

A folder of Blender scene files, one per canonical beat, with characters appended where needed at default offset positions. Scenes already built from prior drafts are preserved unmodified (flagged with ` - complete`).

Per-scene structure inside each `.blend`:
- One collection per character, named after the character (`Florence`, `Sebastian`)
- Characters offset on X so they're not overlapping at origin
- All other scene contents (camera, lighting, environment) inherited from the template — the artist replaces these per scene

## Standards

- **Show-don't-tell still applies.** Production scaffolding is mechanical translation. Never pre-pose, never pre-camera, never pre-light. Those decisions are the artist's.
- **Test before batching.** One scene to validate, then loop.
- **Append, don't overwrite.** Scenes marked ` - complete` are protected.
- **Recon before append.** Inspect character files for collection names; never guess.
- **Single source of truth for characters.** Keep rigs in their own folder. Don't duplicate per scene.
- **Use canonical naming from the precedent file.** If the artist has already named one scene, match it. Don't reinvent.

## Teaching Moment

**What this means in plain English.** The McKee analysis tells you what each scene needs to do dramatically. The director's notes tell you what the staging is. Scene scaffolding is the moment those documents become files an artist can open. The principle: scaffolding is *mechanical translation*, never *creative decision*.

**Why it matters in any production.** When an artist opens a scaffolded scene, they want to start working immediately. If the scaffolding has pre-decided things they will need to undo (a camera at the wrong angle, a character pre-posed in a way they'd never block, lighting that imposes a mood), the scaffolding is anti-help — it adds work. If the scaffolding has only done the mechanical things (the right characters are present, named correctly, not overlapping), the artist starts from a clean canvas with the boilerplate already done.

**How it operates here.** The append script knows which characters belong in which scenes from the director's notes. It does not know how Florence stands at the Beach or what Sebastian's first gesture in the Black Void looks like. It explicitly refuses to guess. The artist opens each scene to find Florence and Sebastian sitting at offset positions, ready to be moved into staging.

**Takeaway for the practitioner.** Define the boundary between mechanical and creative early, and defend it. When you write a scaffolding script, the test is: *if I ran this on someone else's screenplay, would the output still be useful, or would it impose my taste?* If it would impose taste, you've crossed the boundary. Pull back.

---

Follow the orchestrator's OUTPUT STYLE block when reporting back to the user — concise, scene-specific, surface problems don't auto-propose solutions.

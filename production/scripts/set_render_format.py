"""Set the open scene's render engine and image format.

Two-pass: change engine, save, then change format. Some scenes lock the
file_format enum to FFMPEG when the engine/sequencer/compositor is in a
specific state; saving between operations clears the lock.

Usage:
    blender --background scene.blend --python set_render_format.py -- WORKBENCH PNG
"""
import bpy
import sys

argv = sys.argv
args = argv[argv.index("--") + 1:] if "--" in argv else []
if len(args) < 2:
    print("ERROR: usage -- <ENGINE> <FORMAT>")
    raise SystemExit(1)

ENGINE_MAP = {
    "WORKBENCH": "BLENDER_WORKBENCH",
    "EEVEE": "BLENDER_EEVEE",
    "EEVEE_NEXT": "BLENDER_EEVEE_NEXT",
    "CYCLES": "CYCLES",
}

target_engine = ENGINE_MAP.get(args[0].upper(), args[0])
target_fmt = args[1].upper()

scene = bpy.context.scene

print(f"=== Before: engine={scene.render.engine}, format={scene.render.image_settings.file_format}")

# Pass 1 — engine
try:
    scene.render.engine = target_engine
    print(f"=== Pass 1 (engine): set to {target_engine}")
except TypeError as e:
    print(f"=== Pass 1 (engine): FAILED — {e}")

bpy.ops.wm.save_mainfile()

# Pass 2 — format
try:
    scene.render.image_settings.file_format = target_fmt
    print(f"=== Pass 2 (format): set to {target_fmt}")
except TypeError as e:
    # If still locked, try clearing the FFMPEG-binding paths and retry
    print(f"=== Pass 2 (format): first attempt failed — {e}")
    print(f"=== Trying to clear sequencer + compositor bindings then retry")
    try:
        scene.render.use_sequencer = False
        scene.render.use_compositing = False
        scene.render.image_settings.file_format = target_fmt
        print(f"=== Pass 2 (format) RETRY: set to {target_fmt}")
    except TypeError as e2:
        print(f"=== Pass 2 (format) RETRY: FAILED — {e2}")

bpy.ops.wm.save_mainfile()

# Verify
print(f"=== After: engine={scene.render.engine}, format={scene.render.image_settings.file_format}")

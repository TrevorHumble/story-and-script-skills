"""Pre-flight inspection of a Blender scene before rendering.

Usage:
    blender --background scene.blend --python preflight.py

Prints render-relevant settings as one line per field. Output is grep-friendly
so a wrapper script can parse multiple scenes into a table.
"""
import bpy
import os

scene = bpy.context.scene
filename = os.path.basename(bpy.data.filepath)

cam = scene.camera
cam_name = cam.name if cam else "[NONE — BLOCKER]"

engine = scene.render.engine
fmt = scene.render.image_settings.file_format
res_x = scene.render.resolution_x
res_y = scene.render.resolution_y
res_pct = scene.render.resolution_percentage
fps = scene.render.fps
frame_start = scene.frame_start
frame_end = scene.frame_end
frame_count = frame_end - frame_start + 1

# Estimate render time roughly by engine (very rough)
est_per_frame = {
    "BLENDER_WORKBENCH": 0.2,
    "BLENDER_EEVEE": 1.0,
    "BLENDER_EEVEE_NEXT": 1.0,
    "CYCLES": 30.0,
}.get(engine, 5.0)
est_total_sec = frame_count * est_per_frame

# Collections present
collections = [c.name for c in bpy.data.collections]
has_florence = any("florence" in c.lower() or "flo" in c.lower() for c in collections)
has_sebastian = any("sebastian" in c.lower() or "seb" in c.lower() for c in collections)

print(f"PREFLIGHT|filename={filename}")
print(f"PREFLIGHT|camera={cam_name}")
print(f"PREFLIGHT|engine={engine}")
print(f"PREFLIGHT|format={fmt}")
print(f"PREFLIGHT|resolution={res_x}x{res_y}@{res_pct}%")
print(f"PREFLIGHT|fps={fps}")
print(f"PREFLIGHT|frames={frame_start}-{frame_end} ({frame_count} total)")
print(f"PREFLIGHT|est_render_time_sec={est_total_sec:.0f}")
print(f"PREFLIGHT|florence_present={has_florence}")
print(f"PREFLIGHT|sebastian_present={has_sebastian}")
print(f"PREFLIGHT|collections={','.join(collections)}")

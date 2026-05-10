"""Offset named character collections in the open scene so they're not overlapping.

Default: Florence -1m on X, Sebastian +1m on X (2m separation). Adjust the
OFFSETS dict for your characters.

Usage:
    blender --background scene.blend --python offset_characters.py

Operates on root-of-collection objects so child parenting is preserved
(an empty parent moves; everything beneath follows).
"""
import bpy


# === CONFIGURE FOR YOUR PROJECT ===
# Map: collection_name -> (dx, dy, dz) in meters
OFFSETS = {
    "Florence": (-1.0, 0.0, 0.0),
    "Sebastian": (1.0, 0.0, 0.0),
}
# ==================================


def offset_collection(coll_name, dx, dy, dz):
    coll = bpy.data.collections.get(coll_name)
    if coll is None:
        print(f"  SKIP: collection '{coll_name}' not in scene")
        return
    coll_objects = set(coll.all_objects)
    moved = 0
    for obj in coll.all_objects:
        # Move only root-of-collection objects so children follow their parents
        if obj.parent is None or obj.parent not in coll_objects:
            obj.location.x += dx
            obj.location.y += dy
            obj.location.z += dz
            moved += 1
    print(f"  OFFSET '{coll_name}' by ({dx}, {dy}, {dz}) — {moved} root objects moved")


print(f"=== Processing: {bpy.data.filepath}")
for coll_name, (dx, dy, dz) in OFFSETS.items():
    offset_collection(coll_name, dx, dy, dz)
bpy.ops.wm.save_mainfile()
print("=== Saved")

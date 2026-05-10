"""Offset Florence and Sebastian collections in the currently open scene.

Florence: -1m on X. Sebastian: +1m on X. Total separation: 2m.
Operates on top-level objects within the named collections so child
parenting is preserved.
"""
import bpy


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
offset_collection("Florence", -1.0, 0.0, 0.0)
offset_collection("Sebastian", 1.0, 0.0, 0.0)
bpy.ops.wm.save_mainfile()
print("=== Saved")

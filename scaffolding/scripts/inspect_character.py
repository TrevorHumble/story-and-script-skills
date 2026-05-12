"""Inspect a character .blend to learn what to append.

Usage:
    blender --background path/to/character.blend --python inspect_character.py

Prints scenes, top-level collections (with object counts), all collections
including nested, armatures, and top-level objects. Run this once per character
file before writing your append script — never guess at collection names.
"""
import bpy

print("=== SCENES ===")
for s in bpy.data.scenes:
    print(f"  {s.name}")

print("=== TOP-LEVEL COLLECTIONS (in active scene) ===")
for c in bpy.context.scene.collection.children:
    print(f"  {c.name}  (objects: {len(c.all_objects)})")

print("=== ALL COLLECTIONS ===")
for c in bpy.data.collections:
    print(f"  {c.name}  (direct: {len(c.objects)}, all incl children: {len(c.all_objects)})")

print("=== ARMATURES ===")
for a in bpy.data.armatures:
    print(f"  {a.name}")

print("=== TOP-LEVEL OBJECTS (in active scene) ===")
for o in bpy.context.scene.objects:
    if o.parent is None:
        print(f"  [{o.type}] {o.name}")

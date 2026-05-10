"""Deep recon for any sign of a character (Florence) in the open scene.

Looks at: object names, armatures, mesh data, broken library links,
suspicious collection contents.
"""
import bpy

print("=" * 60)
print(f"DEEP RECON: {bpy.data.filepath}")
print("=" * 60)

# 1. All armatures (Florence's rig is named 'rig' in the source file)
print("\n--- ARMATURES (data) ---")
for a in bpy.data.armatures:
    user_objects = [o.name for o in bpy.data.objects if o.data == a]
    print(f"  '{a.name}'  used by objects: {user_objects}")
if not bpy.data.armatures:
    print("  (none)")

# 2. Any object with 'flo', 'char', 'rig' in its name
print("\n--- OBJECTS matching 'flo', 'char', 'rig' (case-insensitive) ---")
hits = [o for o in bpy.data.objects if any(s in o.name.lower() for s in ("flo", "char", "rig"))]
for o in hits:
    in_scene = o.name in bpy.context.scene.objects
    visible = o.visible_get() if in_scene else "n/a"
    print(f"  [{o.type}] '{o.name}'  in_scene={in_scene}  visible={visible}  parent={o.parent.name if o.parent else 'None'}")
if not hits:
    print("  (none)")

# 3. Linked libraries (might be linked-from-external)
print("\n--- LINKED LIBRARIES ---")
for lib in bpy.data.libraries:
    print(f"  '{lib.name}'  filepath={lib.filepath}  users={lib.users}")
if not bpy.data.libraries:
    print("  (none)")

# 4. Mesh data names
print("\n--- MESH DATA matching 'flo', 'char' ---")
mesh_hits = [m for m in bpy.data.meshes if any(s in m.name.lower() for s in ("flo", "char"))]
for m in mesh_hits:
    print(f"  '{m.name}'  users={m.users}")
if not mesh_hits:
    print("  (none)")

# 5. Materials with character names
print("\n--- MATERIALS matching 'flo', 'char', 'skin' ---")
mat_hits = [m for m in bpy.data.materials if any(s in m.name.lower() for s in ("flo", "char", "skin"))]
for m in mat_hits:
    print(f"  '{m.name}'  users={m.users}")
if not mat_hits:
    print("  (none)")

# 6. Look INSIDE every collection for character-shaped contents
print("\n--- COLLECTIONS (deep scan) ---")
for c in bpy.data.collections:
    obj_count = len(c.all_objects)
    has_armature = any(o.type == "ARMATURE" for o in c.all_objects)
    has_char_named = any(any(s in o.name.lower() for s in ("flo", "char", "rig")) for o in c.all_objects)
    flag = ""
    if has_armature:
        flag += " [ARMATURE]"
    if has_char_named:
        flag += " [CHAR-NAME]"
    print(f"  '{c.name}'  objects={obj_count}{flag}")

# 7. Top-level scene objects
print("\n--- SCENE OBJECTS (active scene, top-level only) ---")
for o in bpy.context.scene.objects:
    if o.parent is None:
        print(f"  [{o.type}] '{o.name}'")

# 8. Hidden objects (might be Florence, hidden)
print("\n--- HIDDEN OBJECTS in active scene ---")
hidden = [o for o in bpy.context.scene.objects if o.hide_render or o.hide_viewport or not o.visible_get()]
for o in hidden:
    print(f"  [{o.type}] '{o.name}'  hide_render={o.hide_render}  hide_viewport={o.hide_viewport}")
if not hidden:
    print("  (none)")

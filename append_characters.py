"""Append Florence and/or Sebastian collections into the currently open scene file.

Usage:
    blender --background scene.blend --python append_characters.py -- florence sebastian
    blender --background scene.blend --python append_characters.py -- florence
"""
import bpy
import sys

FLORENCE_PATH = r"C:\Users\thumb\OneDrive - University of Idaho\Paradise Pictures\Catalysis\Scenes\Draft 2\Character\Florence\5-9-27 Rigged Florence.blend"
FLORENCE_COLLECTION = "character1"

SEBASTIAN_PATH = r"C:\Users\thumb\OneDrive - University of Idaho\Paradise Pictures\Catalysis\Scenes\Draft 2\Character\Sebastian\Sebastian.blend"
SEBASTIAN_COLLECTION = "CH-snow"


def parse_args():
    argv = sys.argv
    if "--" in argv:
        return argv[argv.index("--") + 1:]
    return []


def append_collection(blend_path, coll_name, rename_to):
    """Append a collection from a blend file and link it to the active scene."""
    if any(c.name == rename_to for c in bpy.data.collections):
        print(f"  SKIP: collection '{rename_to}' already exists in this scene")
        return None

    with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
        if coll_name not in data_from.collections:
            print(f"  ERROR: collection '{coll_name}' not found in {blend_path}")
            return None
        data_to.collections = [coll_name]

    for coll in data_to.collections:
        if coll is None:
            continue
        bpy.context.scene.collection.children.link(coll)
        coll.name = rename_to
        print(f"  APPENDED: '{coll_name}' as '{rename_to}'")
        return coll
    return None


def main():
    args = [a.lower() for a in parse_args()]
    print(f"=== Processing: {bpy.data.filepath}")
    print(f"=== Args: {args}")

    if "florence" in args:
        append_collection(FLORENCE_PATH, FLORENCE_COLLECTION, "Florence")

    if "sebastian" in args:
        append_collection(SEBASTIAN_PATH, SEBASTIAN_COLLECTION, "Sebastian")

    bpy.ops.wm.save_mainfile()
    print("=== Saved")


main()

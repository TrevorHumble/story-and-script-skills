"""Append named character collections from source .blend files into the open scene.

Usage:
    blender --background scene.blend --python append_characters.py -- name1 name2 ...

Example (Florence + Sebastian):
    blender --background Beach.blend --python append_characters.py -- florence sebastian

Configure the CHARACTERS dict below for your project. Each entry maps a
character keyword (lowercased) to (source_blend_path, source_collection_name,
rename_to). The append picks one collection from the source, links it into
the open scene, and renames it to something the artist will recognize.

Run scripts/inspect_character.py against each source file FIRST to learn
what collection names to target. Don't guess.
"""
import bpy
import sys


# === CONFIGURE FOR YOUR PROJECT ===
# Map: keyword (lowercase) -> (source_blend_path, source_collection_name, rename_to)
CHARACTERS = {
    "florence": (
        r"path\to\Character\Florence\Florence.blend",
        "character1",   # the collection name inside the source file
        "Florence",     # what to call it after appending
    ),
    "sebastian": (
        r"path\to\Character\Sebastian\Sebastian.blend",
        "CH-snow",
        "Sebastian",
    ),
    # Add more characters as needed
}
# ==================================


def parse_args():
    argv = sys.argv
    if "--" in argv:
        return [a.lower() for a in argv[argv.index("--") + 1:]]
    return []


def append_collection(blend_path, coll_name, rename_to):
    """Append a collection from a blend file and link it into the active scene."""
    if any(c.name == rename_to for c in bpy.data.collections):
        print(f"  SKIP: collection '{rename_to}' already exists")
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
    args = parse_args()
    print(f"=== Processing: {bpy.data.filepath}")
    print(f"=== Characters requested: {args}")

    for name in args:
        if name not in CHARACTERS:
            print(f"  UNKNOWN character keyword: '{name}'")
            continue
        blend_path, coll_name, rename_to = CHARACTERS[name]
        append_collection(blend_path, coll_name, rename_to)

    bpy.ops.wm.save_mainfile()
    print("=== Saved")


main()

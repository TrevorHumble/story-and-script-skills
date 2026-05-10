#!/usr/bin/env bash
# Headless-render every scene in Draft 2 to a per-scene output folder.
# Usage:
#   bash render_all.sh
#
# Defaults pull from the constants below; edit if your install path or output
# location changes.

set -e

BLENDER='/c/Program Files/Blender Foundation/Blender 5.1/blender.exe'
SCRIPT='/c/Users/thumb/OneDrive/Documents/Story Skills - Copy/render_scene.py'
DRAFT2='/c/Users/thumb/OneDrive - University of Idaho/Paradise Pictures/Catalysis/Scenes/Draft 2'
OUTPUT_ROOT='/c/Users/thumb/OneDrive - University of Idaho/Paradise Pictures/Catalysis/renders'

mkdir -p "$OUTPUT_ROOT"

# Render in canonical order so log output reads top to bottom of the film
SCENES=(
    "Act.1-Scene.1-Apartment - complete"
    "Act.1-Scene.2-BakedBean - complete"
    "Act.1-Scene.3-Meadow - complete"
    "Act.1-Scene.4-Flight - complete"
    "Act.1-Scene.5-Beach"
    "Act.2-Scene.1-Riverwalk"
    "Act.2-Scene.2-BlackVoid"
    "Act.2-Scene.3-Ballroom"
    "Act.2-Scene.4-ApartmentReturn"
    "Act.2-Scene.5-London"
    "Act.2-Scene.6-FeverDream"
    "Act.2-Scene.7-BarbieBox"
    "Act.2-Scene.8-Swallow"
    "Act.3-Scene.1-ApartmentFinal"
)

for scene in "${SCENES[@]}"; do
    blend="$DRAFT2/${scene}.blend"
    if [ ! -f "$blend" ]; then
        echo ">>> SKIP (file missing): $scene"
        continue
    fi
    echo ""
    echo "================================================================"
    echo ">>> $scene"
    echo "================================================================"
    "$BLENDER" --background "$blend" --python "$SCRIPT" -- "$OUTPUT_ROOT" 2>&1 | grep -E "^(===|Append|Fra:)" || true
done

echo ""
echo "All scenes rendered to: $OUTPUT_ROOT"

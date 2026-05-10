"""EXR-to-PNG conversion for mid-render vision checks.

When the render output format is ``OPEN_EXR`` or ``OPEN_EXR_MULTILAYER``,
vision models cannot consume the raw EXR.  This module converts a single EXR
frame to a temporary PNG using Blender's image API so that:

* The scene's colour-management view transform is applied (HDR → 8-bit sRGB).
* For multilayer EXR: the Combined / beauty pass is selected before saving,
  not a non-visual pass like depth or AO.
* The temp PNG is written to the system temp directory and its path returned.
  The caller is responsible for deleting it after the vision check completes.

**The full EXR sequence is never modified.**  Only a temporary PNG is created
and discarded.

Runtime requirement: must be imported inside a Blender Python session
(requires ``bpy``).
"""

from __future__ import annotations

import os
import tempfile
from typing import Optional


def to_temp_png(exr_path: str, scene: "bpy.types.Scene") -> str:
    """Convert the EXR at *exr_path* to a temporary PNG and return its path.

    The PNG is written using ``image.save_render()`` (NOT ``image.save()``) so
    that the scene's colour-management view transform is applied.  This ensures
    HDR linear-light values are tone-mapped into the 8-bit range the vision
    model expects.

    For multilayer EXR: ensures the "Combined" render layer is active before
    conversion so a non-visual pass (depth, normals, AO) is not accidentally
    sent to the vision model.

    Args:
        exr_path: Absolute path to the EXR file to convert.
        scene:    The current Blender scene (``bpy.context.scene``).  Used for
                  colour-management settings and image API access.

    Returns:
        Absolute path to the temporary PNG.  The caller must delete this file
        after use::

            png_path = to_temp_png(exr_path, scene)
            try:
                verdict, reason = verify_frame(png_path, context)
            finally:
                os.unlink(png_path)

    Raises:
        RuntimeError: If the EXR cannot be loaded or the PNG cannot be saved.
        ImportError:  If ``bpy`` is not available (called outside Blender).
    """
    try:
        import bpy  # type: ignore[import]
    except ImportError as exc:
        raise ImportError(
            "exr_convert.to_temp_png() requires a Blender Python session (bpy)."
        ) from exc

    # Load the EXR into Blender's image datablock.
    image = _load_image(bpy, exr_path)
    try:
        # For multilayer EXR: ensure Combined (beauty) pass is active.
        _ensure_combined_layer(image, scene)

        # Write to a temp PNG using save_render() to apply view transform.
        png_path = _save_as_png(bpy, image, scene)
    finally:
        # Always remove the loaded image from Blender's data to avoid leaks.
        bpy.data.images.remove(image)

    return png_path


# ---------------------------------------------------------------------------
# Internals
# ---------------------------------------------------------------------------


def _load_image(bpy: "types.ModuleType", exr_path: str) -> "bpy.types.Image":
    """Load an EXR into Blender's image data and return the datablock."""
    if not os.path.isfile(exr_path):
        raise RuntimeError(f"EXR file not found: {exr_path}")

    image = bpy.data.images.load(exr_path)
    # Force the image to be fully read into memory.
    image.update()
    return image


def _ensure_combined_layer(image: "bpy.types.Image", scene: "bpy.types.Scene") -> None:
    """For multilayer EXR: activate the Combined pass before PNG conversion.

    If the image has multiple layers (e.g. from ``OPEN_EXR_MULTILAYER``), set
    the active render layer to the "Combined" pass so that
    ``save_render()`` picks up the beauty output rather than a technical pass.

    For plain (single-layer) EXR this function is a no-op.

    Args:
        image:  Loaded Blender image datablock.
        scene:  Current scene (unused here but kept for signature consistency).
    """
    # Multilayer EXR exposes render_slots or layers through image.layers.
    # In Blender 5.x the attribute is image.layers for multilayer images.
    layers = getattr(image, "layers", None)
    if not layers:
        return  # Single-layer EXR — nothing to do.

    layer_names = [layer.name for layer in layers]
    # Prefer exact match; fall back to any layer containing "Combined".
    target: Optional[str] = None
    for name in layer_names:
        if name == "Combined":
            target = name
            break
    if target is None:
        for name in layer_names:
            if "combined" in name.lower():
                target = name
                break

    if target is None:
        # Couldn't find Combined; log a warning and proceed with whatever is active.
        print(
            "=== WARNING [exr_convert]: Could not find 'Combined' layer in multilayer EXR. "
            f"Available layers: {layer_names}. Proceeding with active layer."
        )
        return

    # Set the active layer by index.
    for idx, layer in enumerate(layers):
        if layer.name == target:
            image.active_render_layer_index = idx
            break


def _save_as_png(
    bpy: "types.ModuleType",
    image: "bpy.types.Image",
    scene: "bpy.types.Scene",
) -> str:
    """Save *image* as a temporary PNG using ``save_render()`` (view-transform applied).

    Uses a NamedTemporaryFile so we get a unique path that the caller can
    clean up after the vision check.

    Args:
        bpy:    The ``bpy`` module.
        image:  Loaded Blender image datablock.
        scene:  Current scene, used for colour-management settings.

    Returns:
        Absolute path to the saved PNG.
    """
    # Create a temp file with a .png suffix.  delete=False so the caller
    # can read it after this function returns.
    fd, png_path = tempfile.mkstemp(suffix=".png", prefix="visioncheck_")
    os.close(fd)  # Close the raw file descriptor; Blender opens it separately.

    # save_render() applies the scene's colour management (view transform,
    # exposure, gamma) unlike image.save() which writes raw linear values.
    # This ensures the PNG looks like what the artist sees in the viewport.
    image.save_render(filepath=png_path, scene=scene)

    return png_path

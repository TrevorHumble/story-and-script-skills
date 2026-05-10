"""Last-ditch attempt to unlock the file_format enum."""
import bpy

scene = bpy.context.scene

print("=== ATTEMPT 1: reset ffmpeg properties to defaults ===")
try:
    scene.render.ffmpeg.format = "MKV"  # neutral container
    scene.render.image_settings.file_format = "PNG"
    print("  SUCCESS via ffmpeg.format reset")
    bpy.ops.wm.save_mainfile()
    raise SystemExit(0)
except Exception as e:
    print(f"  FAILED: {e}")

print("\n=== ATTEMPT 2: set via operator-ish path ===")
try:
    # Try setting through bpy.context override
    scene.render.image_settings.file_format = "PNG"
    print("  SUCCESS via direct retry")
    bpy.ops.wm.save_mainfile()
    raise SystemExit(0)
except Exception as e:
    print(f"  FAILED: {e}")

print("\n=== ATTEMPT 3: copy scene to a new one with default render settings ===")
try:
    old_scene = bpy.context.scene
    old_camera = old_scene.camera
    old_frame_start = old_scene.frame_start
    old_frame_end = old_scene.frame_end
    old_engine = old_scene.render.engine
    old_res_x = old_scene.render.resolution_x
    old_res_y = old_scene.render.resolution_y

    bpy.ops.scene.new(type="EMPTY")
    new_scene = bpy.context.scene
    new_scene.name = "Scene_PNG"
    new_scene.render.engine = old_engine
    new_scene.render.resolution_x = old_res_x
    new_scene.render.resolution_y = old_res_y
    new_scene.frame_start = old_frame_start
    new_scene.frame_end = old_frame_end
    # Try setting format on the NEW scene
    new_scene.render.image_settings.file_format = "PNG"
    print(f"  SUCCESS: new scene has format={new_scene.render.image_settings.file_format}")
    print(f"  Old scene still: format={old_scene.render.image_settings.file_format}")
    print("  But this approach abandons the old scene's contents — not viable.")
except Exception as e:
    print(f"  FAILED: {e}")

print("\n=== ATTEMPT 4: explicitly clear the render-output overrides ===")
try:
    # Some addons set "use_render_cache" or similar that lock things
    scene = bpy.data.scenes[0]
    for prop in ("use_render_cache", "use_motion_blur", "use_persistent_data"):
        if hasattr(scene.render, prop):
            try:
                setattr(scene.render, prop, False)
            except Exception:
                pass
    scene.render.image_settings.file_format = "PNG"
    print("  SUCCESS via override clear")
    bpy.ops.wm.save_mainfile()
    raise SystemExit(0)
except Exception as e:
    print(f"  FAILED: {e}")

print("\n=== ALL ATTEMPTS FAILED ===")
print("File requires manual GUI fix.")

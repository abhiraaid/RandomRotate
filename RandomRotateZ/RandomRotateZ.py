bl_info = {
    "name": "Random Rotate Z",
    "author": "abhiraaid",
    "version": (1, 1),
    "blender": (3, 5, 1),
    "location": "View3D > Sidebar > Random Rotate Z",
    "description": "Randomize rotation of selected objects",
    "category": "Object",
}

import bpy
import math
import random
import mathutils
from bpy.props import FloatProperty

class RandomRotateZOperator(bpy.types.Operator):
    bl_idname = "object.random_rotate_z"
    bl_label = "Random Rotate Z"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        if not selected_objects:
            self.report({"WARNING"}, "No objects selected.")
            return {"CANCELLED"}

        min_angle_z = context.scene.random_rotate_z_min_angle
        max_angle_z = context.scene.random_rotate_z_max_angle

        # Perform the random rotation for each object
        for obj in selected_objects:
            rotation_angle_z = math.radians(random.uniform(min_angle_z, max_angle_z))
            obj.rotation_euler.rotate_axis("Z", rotation_angle_z)

        return {"FINISHED"}

class RandomRotateZPanel(bpy.types.Panel):
    bl_label = "Random Rotate Z"
    bl_idname = "OBJECT_PT_random_rotate_z_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Random Rotate"

    def draw(self, context):
        layout = self.layout

        # Draw the minimum and maximum angle properties for Z axis
        layout.prop(context.scene, "random_rotate_z_min_angle")
        layout.prop(context.scene, "random_rotate_z_max_angle")

        # Draw the random rotate Z operator button
        layout.operator("object.random_rotate_z")

addon_keymaps = []

def register():
    bpy.utils.register_class(RandomRotateZOperator)
    bpy.utils.register_class(RandomRotateZPanel)

    # Create scene properties for minimum and maximum angles
    bpy.types.Scene.random_rotate_z_min_angle = FloatProperty(
        name="Minimum Z Angle",
        description="Minimum rotation angle in degrees for Z axis",
        default=20.0,
        min=-360.0,
        soft_max=360.0,
    )

    bpy.types.Scene.random_rotate_z_max_angle = FloatProperty(
        name="Maximum Z Angle",
        description="Maximum rotation angle in degrees for Z axis",
        default=90.0,
        min=-360.0,
        soft_max=360.0,
    )

    # Add keymap entry
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = kc.keymaps.new(name="Object Mode", space_type="EMPTY")
        kmi = km.keymap_items.new("object.random_rotate_z", "Q", "PRESS", alt=True)
        addon_keymaps.append((km, kmi))

def unregister():
    bpy.utils.unregister_class(RandomRotateZOperator)
    bpy.utils.unregister_class(RandomRotateZPanel)

    # Remove scene properties
    del bpy.types.Scene.random_rotate_z_min_angle
    del bpy.types.Scene.random_rotate_z_max_angle

    # Remove keymap entry
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)

        addon_keymaps.clear()

if __name__ == "__main__":
    register()


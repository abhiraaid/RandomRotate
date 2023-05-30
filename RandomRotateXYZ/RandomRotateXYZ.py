bl_info = {
    "name": "Random Rotate XYZ",
    "author": "abhiraaid",
    "version": (1, 0),
    "blender": (3, 5, 1),
    "location": "View3D > Sidebar > Random Rotate XYZ",
    "description": "Randomize rotation of selected objects",
    "category": "Object",
}

import bpy
import math
import random
import mathutils
from bpy.props import FloatProperty, EnumProperty, BoolProperty, PointerProperty


class RandomRotateXYZOperator(bpy.types.Operator):
    bl_idname = "object.random_rotate_xyz"
    bl_label = "Random Rotate XYZ"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        if not selected_objects:
            self.report({"WARNING"}, "No objects selected.")
            return {"CANCELLED"}

        min_angle_x = context.scene.random_rotate_xyz_min_angle_x
        max_angle_x = context.scene.random_rotate_xyz_max_angle_x
        min_angle_y = context.scene.random_rotate_xyz_min_angle_y
        max_angle_y = context.scene.random_rotate_xyz_max_angle_y
        min_angle_z = context.scene.random_rotate_xyz_min_angle_z
        max_angle_z = context.scene.random_rotate_xyz_max_angle_z

        # Store the initially selected objects
        initial_selection = bpy.context.selected_objects[:]

        # Perform the random rotation for each object
        for obj in selected_objects:
            self.select(obj)
            rotation_mode = context.scene.random_rotate_xyz_rotation_mode
            if rotation_mode == 'GLOBAL':
                rotation_angle_x = math.radians(random.uniform(min_angle_x, max_angle_x))
                rotation_angle_y = math.radians(random.uniform(min_angle_y, max_angle_y))
                rotation_angle_z = math.radians(random.uniform(min_angle_z, max_angle_z))
                euler_rotation = mathutils.Euler((rotation_angle_x, rotation_angle_y, rotation_angle_z), 'XYZ')
                obj.rotation_euler.rotate(euler_rotation)
            elif rotation_mode == 'LOCAL':
                rotation_angle_x = math.radians(random.uniform(min_angle_x, max_angle_x))
                rotation_angle_y = math.radians(random.uniform(min_angle_y, max_angle_y))
                rotation_angle_z = math.radians(random.uniform(min_angle_z, max_angle_z))
                obj.rotation_euler.rotate_axis('X', rotation_angle_x)
                obj.rotation_euler.rotate_axis('Y', rotation_angle_y)
                obj.rotation_euler.rotate_axis('Z', rotation_angle_z)
            elif rotation_mode == 'CUSTOM':
                custom_object = context.scene.random_rotate_xyz_custom_object
                if custom_object is None:
                    self.report({"WARNING"}, "Custom object not selected.")
                    continue
                obj.rotation_euler = custom_object.rotation_euler
                rotation_angle_x = math.radians(random.uniform(min_angle_x, max_angle_x))
                rotation_angle_y = math.radians(random.uniform(min_angle_y, max_angle_y))
                rotation_angle_z = math.radians(random.uniform(min_angle_z, max_angle_z))
                obj.rotation_euler.rotate_axis('X', rotation_angle_x)
                obj.rotation_euler.rotate_axis('Y', rotation_angle_y)
                obj.rotation_euler.rotate_axis('Z', rotation_angle_z)

        # Restore the initial selection
        self.restore_selection(initial_selection)

        return {"FINISHED"}

    def select(self, obj):
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

    def restore_selection(self, objects):
        bpy.ops.object.select_all(action='DESELECT')
        for obj in objects:
            obj.select_set(True)


class RandomRotateXYZPanel(bpy.types.Panel):
    bl_label = "Random Rotate XYZ"
    bl_idname = "OBJECT_PT_random_rotate_xyz_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Random Rotate"

    def draw(self, context):
        layout = self.layout

        # Draw the minimum and maximum angle properties for X axis
        layout.prop(context.scene, "random_rotate_xyz_min_angle_x")
        layout.prop(context.scene, "random_rotate_xyz_max_angle_x")

        # Draw the minimum and maximum angle properties for Y axis
        layout.prop(context.scene, "random_rotate_xyz_min_angle_y")
        layout.prop(context.scene, "random_rotate_xyz_max_angle_y")

        # Draw the minimum and maximum angle properties for Z axis
        layout.prop(context.scene, "random_rotate_xyz_min_angle_z")
        layout.prop(context.scene, "random_rotate_xyz_max_angle_z")

        # Draw the rotation mode property
        layout.prop(context.scene, "random_rotate_xyz_rotation_mode")

        # Draw the custom object property
        if context.scene.random_rotate_xyz_rotation_mode == 'CUSTOM':
            layout.prop(context.scene, "random_rotate_xyz_custom_object")

        # Draw the "Rotate Random" button with documentation
        layout.operator("object.random_rotate_xyz", text="Rotate Random")


def register():
    bpy.utils.register_class(RandomRotateXYZOperator)
    bpy.utils.register_class(RandomRotateXYZPanel)

    bpy.types.Scene.random_rotate_xyz_min_angle_x = FloatProperty(
        name="Minimum X Angle",
        description="Minimum rotation angle in degrees for X axis",
        default=0.0,
        min=0.0,
        soft_max=180.0,
    )

    bpy.types.Scene.random_rotate_xyz_max_angle_x = FloatProperty(
        name="Maximum X Angle",
        description="Maximum rotation angle in degrees for X axis",
        default=0.0,
        min=0.0,
        soft_max=180.0,
    )

    bpy.types.Scene.random_rotate_xyz_min_angle_y = FloatProperty(
        name="Minimum Y Angle",
        description="Minimum rotation angle in degrees for Y axis",
        default=0.0,
        min=0.0,
        soft_max=180.0,
    )

    bpy.types.Scene.random_rotate_xyz_max_angle_y = FloatProperty(
        name="Maximum Y Angle",
        description="Maximum rotation angle in degrees for Y axis",
        default=0.0,
        min=0.0,
        soft_max=180.0,
    )

    bpy.types.Scene.random_rotate_xyz_min_angle_z = FloatProperty(
        name="Minimum Z Angle",
        description="Minimum rotation angle in degrees for Z axis",
        default=20.0,
        min=0.0,
        soft_max=180.0,
    )

    bpy.types.Scene.random_rotate_xyz_max_angle_z = FloatProperty(
        name="Maximum Z Angle",
        description="Maximum rotation angle in degrees for Z axis",
        default=90.0,
        min=0.0,
        soft_max=180.0,
    )

    bpy.types.Scene.random_rotate_xyz_rotation_mode = EnumProperty(
        name="Rotation Mode",
        description="Rotation mode for random rotation",
        items=[
            ('GLOBAL', "Global", "Rotate objects in global space"),
            ('LOCAL', "Local", "Rotate objects in local space"),
            ('CUSTOM', "Custom", "Rotate objects to match custom object"),
        ],
        default='LOCAL',
    )

    bpy.types.Scene.random_rotate_xyz_custom_object = PointerProperty(
        name="Custom Object",
        description="Custom object to match rotation",
        type=bpy.types.Object,
    )

    # Register the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new('object.random_rotate_xyz', 'Q', 'PRESS', alt=True)
    kmi.active = True


def unregister():
    bpy.utils.unregister_class(RandomRotateXYZOperator)
    bpy.utils.unregister_class(RandomRotateXYZPanel)

    del bpy.types.Scene.random_rotate_xyz_min_angle_x
    del bpy.types.Scene.random_rotate_xyz_max_angle_x
    del bpy.types.Scene.random_rotate_xyz_min_angle_y
    del bpy.types.Scene.random_rotate_xyz_max_angle_y
    del bpy.types.Scene.random_rotate_xyz_min_angle_z
    del bpy.types.Scene.random_rotate_xyz_max_angle_z
    del bpy.types.Scene.random_rotate_xyz_rotation_mode
    del bpy.types.Scene.random_rotate_xyz_custom_object

    # Remove the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.get('Object Mode')
    if km:
        km.keymap_items.remove(km.keymap_items.find('object.random_rotate_xyz'))
        if not km.keymap_items:
            wm.keyconfigs.addon.keymaps.remove(km)


if __name__ == "__main__":
    register()

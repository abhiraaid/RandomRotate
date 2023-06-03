bl_info = {
    "name": "Random Rotate XYZ",
    "author": "abhiraaid",
    "version": (2, 0),
    "blender": (3, 5, 1),
    "location": "View3D > Sidebar > Random Rotate XYZ",
    "description": "Randomize rotation of selected objects",
    "category": "Object",
}

import bpy
import math
import random
import mathutils

def calculate_increment_angle(increment_angle):
    if increment_angle == 0 or increment_angle == 360 or increment_angle == -360:
        return 0
        
    else:
        max_multiplier = int(360 / increment_angle)
        random_multiplier = random.randint(1, max_multiplier)
        return random_multiplier * increment_angle

class RandomRotateXYZPanel(bpy.types.Panel):
    bl_label = "Random Rotate XYZ"
    bl_idname = "OBJECT_PT_random_rotate_xyz_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Random Rotate"

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene, "random_rotate_xyz_use_increment", text="Use Increment")

        if not context.scene.random_rotate_xyz_use_increment:
            layout.prop(context.scene, "random_rotate_xyz_min_angle_x")
            layout.prop(context.scene, "random_rotate_xyz_max_angle_x")
            layout.prop(context.scene, "random_rotate_xyz_min_angle_y")
            layout.prop(context.scene, "random_rotate_xyz_max_angle_y")
            layout.prop(context.scene, "random_rotate_xyz_min_angle_z")
            layout.prop(context.scene, "random_rotate_xyz_max_angle_z")
        else:
            layout.prop(context.scene, "random_rotate_xyz_increment_angle_x")
            layout.prop(context.scene, "random_rotate_xyz_increment_angle_y")
            layout.prop(context.scene, "random_rotate_xyz_increment_angle_z")

        layout.prop(context.scene, "random_rotate_xyz_rotation_mode")

        if context.scene.random_rotate_xyz_rotation_mode == 'CUSTOM':
            layout.prop_search(context.scene, "random_rotate_xyz_custom_object", bpy.data, "objects", text="")

        layout.operator("object.random_rotate_xyz", text="Rotate Random")


class RandomRotateXYZOperator(bpy.types.Operator):
    """Randomly rotates the selected objects around XYZ axes"""
    bl_idname = "object.random_rotate_xyz"
    bl_label = "Random Rotate XYZ"
    bl_options = {'UNDO'}

    def restore_selection(self, initial_selection):
        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')
        # Select the initially selected objects
        for obj in initial_selection:
            obj.select_set(True)
            
    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        if not selected_objects:
            self.report({"WARNING"}, "No objects selected.")
            return {"CANCELLED"}
        
        initial_selection = bpy.context.selected_objects[:]
        
        use_increment = context.scene.random_rotate_xyz_use_increment
        if use_increment:
            increment_angle_x = context.scene.random_rotate_xyz_increment_angle_x
            increment_angle_y = context.scene.random_rotate_xyz_increment_angle_y
            increment_angle_z = context.scene.random_rotate_xyz_increment_angle_z

            for obj in selected_objects:
                self.select(obj)
                rotation_mode = context.scene.random_rotate_xyz_rotation_mode
                if rotation_mode == 'GLOBAL':
                    self.rotate_increment_global(obj, increment_angle_x, increment_angle_y, increment_angle_z)
                elif rotation_mode == 'LOCAL':
                    self.rotate_increment_local(obj, increment_angle_x, increment_angle_y, increment_angle_z)
                elif rotation_mode == 'CUSTOM':
                    custom_object = context.scene.random_rotate_xyz_custom_object
                    if custom_object is None:
                        self.report({"WARNING"}, "Custom object not selected.")
                        continue
                    self.rotate_increment_custom(obj, custom_object, increment_angle_x, increment_angle_y, increment_angle_z)
        else:
            min_angle_x = context.scene.random_rotate_xyz_min_angle_x
            max_angle_x = context.scene.random_rotate_xyz_max_angle_x
            min_angle_y = context.scene.random_rotate_xyz_min_angle_y
            max_angle_y = context.scene.random_rotate_xyz_max_angle_y
            min_angle_z = context.scene.random_rotate_xyz_min_angle_z
            max_angle_z = context.scene.random_rotate_xyz_max_angle_z

            for obj in selected_objects:
                self.select(obj)
                rotation_mode = context.scene.random_rotate_xyz_rotation_mode
                if rotation_mode == 'GLOBAL':
                    self.rotate_random_global(obj, min_angle_x, max_angle_x, min_angle_y, max_angle_y, min_angle_z, max_angle_z)
                elif rotation_mode == 'LOCAL':
                    self.rotate_random_local(obj, min_angle_x, max_angle_x, min_angle_y, max_angle_y, min_angle_z, max_angle_z)
                elif rotation_mode == 'CUSTOM':
                    custom_object = context.scene.random_rotate_xyz_custom_object
                    if custom_object is None:
                        self.report({"WARNING"}, "Custom object not selected.")
                        continue
                    self.rotate_random_custom(obj, custom_object, min_angle_x, max_angle_x, min_angle_y, max_angle_y, min_angle_z, max_angle_z)
        
        # Restore the initial selection
        self.restore_selection(initial_selection)
        
        return {"FINISHED"}

    def rotate_increment_global(self, obj, increment_angle_x, increment_angle_y, increment_angle_z):
        rotation_angle_x = math.radians(calculate_increment_angle(increment_angle_x))
        rotation_angle_y = math.radians(calculate_increment_angle(increment_angle_y))
        rotation_angle_z = math.radians(calculate_increment_angle(increment_angle_z))
        
        euler_rotation = mathutils.Euler((rotation_angle_x, rotation_angle_y, rotation_angle_z), 'XYZ')
        obj.rotation_euler.rotate(euler_rotation)

    def rotate_increment_local(self, obj, increment_angle_x, increment_angle_y, increment_angle_z):
        rotation_angle_x = math.radians(calculate_increment_angle(increment_angle_x))
        rotation_angle_y = math.radians(calculate_increment_angle(increment_angle_y))
        rotation_angle_z = math.radians(calculate_increment_angle(increment_angle_z))
        
        obj.rotation_euler.rotate_axis('X', rotation_angle_x)
        obj.rotation_euler.rotate_axis('Y', rotation_angle_y)
        obj.rotation_euler.rotate_axis('Z', rotation_angle_z)
        
    def rotate_increment_custom(self, obj, custom_object, increment_angle_x, increment_angle_y, increment_angle_z):
 
        obj.rotation_euler = custom_object.rotation_euler
        

        rotation_angle_x = math.radians(calculate_increment_angle(increment_angle_x))
        rotation_angle_y = math.radians(calculate_increment_angle(increment_angle_y))
        rotation_angle_z = math.radians(calculate_increment_angle(increment_angle_z))
        
        obj.rotation_euler.rotate_axis('X', rotation_angle_x)
        obj.rotation_euler.rotate_axis('Y', rotation_angle_y)
        obj.rotation_euler.rotate_axis('Z', rotation_angle_z)

    def rotate_random_global(self, obj, min_angle_x, max_angle_x, min_angle_y, max_angle_y, min_angle_z, max_angle_z):
        rotation_angle_x = math.radians(random.uniform(min_angle_x, max_angle_x))
        rotation_angle_y = math.radians(random.uniform(min_angle_y, max_angle_y))
        rotation_angle_z = math.radians(random.uniform(min_angle_z, max_angle_z))
        
        euler_rotation = mathutils.Euler((rotation_angle_x, rotation_angle_y, rotation_angle_z), 'XYZ')
        obj.rotation_euler.rotate(euler_rotation)

    def rotate_random_local(self, obj, min_angle_x, max_angle_x, min_angle_y, max_angle_y, min_angle_z, max_angle_z):
        rotation_angle_x = math.radians(random.uniform(min_angle_x, max_angle_x))
        rotation_angle_y = math.radians(random.uniform(min_angle_y, max_angle_y))
        rotation_angle_z = math.radians(random.uniform(min_angle_z, max_angle_z))
        
        obj.rotation_euler.rotate_axis('X', rotation_angle_x)
        obj.rotation_euler.rotate_axis('Y', rotation_angle_y)
        obj.rotation_euler.rotate_axis('Z', rotation_angle_z)

    def rotate_random_custom(self, obj, custom_object, min_angle_x, max_angle_x, min_angle_y, max_angle_y, min_angle_z, max_angle_z):
        #custom_object = context.scene.random_rotate_xyz_custom_object

        obj.rotation_euler = custom_object.rotation_euler

        rotation_angle_x = math.radians(random.uniform(min_angle_x, max_angle_x))
        rotation_angle_y = math.radians(random.uniform(min_angle_y, max_angle_y))
        rotation_angle_z = math.radians(random.uniform(min_angle_z, max_angle_z))
        
        obj.rotation_euler.rotate_axis('X', rotation_angle_x)
        obj.rotation_euler.rotate_axis('Y', rotation_angle_y)
        obj.rotation_euler.rotate_axis('Z', rotation_angle_z)
        
    def select(self, obj):
        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')
        # Select the object
        obj.select_set(True)


# Register the operator and panel classes
def register():
    bpy.utils.register_class(RandomRotateXYZOperator)
    bpy.utils.register_class(RandomRotateXYZPanel)

    bpy.types.Scene.random_rotate_xyz_min_angle_x = bpy.props.FloatProperty(
        name="Minimum X Angle",
        description="Minimum rotation angle in degrees for X axis",
        default=-2.0,
        min=-360.0,
        soft_max=360.0,
    )

    bpy.types.Scene.random_rotate_xyz_max_angle_x = bpy.props.FloatProperty(
        name="Maximum X Angle",
        description="Maximum rotation angle in degrees for X axis",
        default=2.0,
        min=-360.0,
        soft_max=360.0,
    )

    bpy.types.Scene.random_rotate_xyz_min_angle_y = bpy.props.FloatProperty(
        name="Minimum Y Angle",
        description="Minimum rotation angle in degrees for Y axis",
        default=-2.0,
        min=-360.0,
        soft_max=360.0,
    )

    bpy.types.Scene.random_rotate_xyz_max_angle_y = bpy.props.FloatProperty(
        name="Maximum Y Angle",
        description="Maximum rotation angle in degrees for Y axis",
        default=2.0,
        min=0.0,
        soft_max=180.0,
    )

    bpy.types.Scene.random_rotate_xyz_min_angle_z = bpy.props.FloatProperty(
        name="Minimum Z Angle",
        description="Minimum rotation angle in degrees for Z axis",
        default=-2.0,
        min=-360.0,
        soft_max=360.0,
    )

    bpy.types.Scene.random_rotate_xyz_max_angle_z = bpy.props.FloatProperty(
        name="Maximum Z Angle",
        description="Maximum rotation angle in degrees for Z axis",
        default=2.0,
        min=-360.0,
        soft_max=360.0,
    )

    bpy.types.Scene.random_rotate_xyz_rotation_mode = bpy.props.EnumProperty(
        name="Rotation Mode",
        description="Rotation mode for objects",
        items=[
            ('GLOBAL', "Global", "Rotate objects in global coordinates"),
            ('LOCAL', "Local", "Rotate objects in local coordinates"),
            ('CUSTOM', "Custom", "Rotate objects relative to a custom object"),
        ],
        default='GLOBAL',
    )

    bpy.types.Scene.random_rotate_xyz_custom_object = bpy.props.PointerProperty(
        name="Custom Object",
        description="Custom object used for rotation",
        type=bpy.types.Object,
    )

    bpy.types.Scene.random_rotate_xyz_increment_angle_x = bpy.props.FloatProperty(
        name="Increment X Angle",
        description="Rotation increment angle in degrees for X axis",
        default=180.0,
        min=-360.0,
        soft_max=360.0,
    )

    bpy.types.Scene.random_rotate_xyz_increment_angle_y = bpy.props.FloatProperty(
        name="Increment Y Angle",
        description="Rotation increment angle in degrees for Y axis",
        default=180.0,
        min=-360.0,
        soft_max=360.0,
    )

    bpy.types.Scene.random_rotate_xyz_increment_angle_z = bpy.props.FloatProperty(
        name="Increment Z Angle",
        description="Rotation increment angle in degrees for Z axis",
        default=180.0,
        min=-360.0,
        soft_max=360.0,
    )

    bpy.types.Scene.random_rotate_xyz_use_increment = bpy.props.BoolProperty(
        name="Use Increment",
        description="Enable rotation increment",
        default=False,
    )
    
    # Register the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new('object.random_rotate_xyz', 'Q', 'PRESS', alt=True)
    kmi.active = True

    
    

# Unregister the operator and panel classes
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
    del bpy.types.Scene.random_rotate_xyz_increment_angle_x
    del bpy.types.Scene.random_rotate_xyz_increment_angle_y
    del bpy.types.Scene.random_rotate_xyz_increment_angle_z
    del bpy.types.Scene.random_rotate_xyz_use_increment
    
    # Remove the keymap item
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.get('Object Mode')
    if km:
        keymap_item = km.keymap_items.find('object.random_rotate_xyz')
        if keymap_item:
            km.keymap_items.remove(keymap_item)
        if not km.keymap_items:
            wm.keyconfigs.addon.keymaps.remove(km)

if __name__ == "__main__":
    register()

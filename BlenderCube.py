import bpy
import math
from mathutils import Vector

# Cleanup scene
def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

# Create cube with material based on recursion level
def create_cube(location, size, level, name="MengerCube"):
    # Create cube object
    bpy.ops.mesh.primitive_cube_add(size=size, location=location)
    obj = bpy.context.object
    obj.name = name
    
    # Assign color material based on level
    mat_name = f"MengerMaterial_L{level}"
    if mat_name not in bpy.data.materials:
        mat = bpy.data.materials.new(mat_name)
        hue = level / 5  # Color varies with depth
        mat.diffuse_color = (hue, 0.7, 1.0, 1.0)
    else:
        mat = bpy.data.materials[mat_name]
    
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    return obj

# Recursive Menger Sponge generator
def create_menger_sponge(iterations, location, size):
    def recursive_menger(objects, level, size):
        if level <= 0:
            return
        new_objects = []
        for obj in objects:
            loc = obj.location
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    for z in [-1, 0, 1]:
                        if abs(x) + abs(y) + abs(z) > 1:
                            offset = Vector((x, y, z)) * size
                            new_loc = loc + offset
                            cube = create_cube(new_loc, size, level, f"MengerCube_L{level}")
                            new_objects.append(cube)
        recursive_menger(new_objects, level - 1, size / 3)

    # Start recursive generation
    initial_cube = create_cube(location, size, iterations, "BaseCube")
    recursive_menger([initial_cube], iterations, size / 3)

# Boolean subtraction example
def create_boolean_sponge():
    # Create base cube
    bpy.ops.mesh.primitive_cube_add(size=3, location=(0, 0, 0))
    base = bpy.context.object
    
    # Create cube to subtract
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    cutter = bpy.context.object
    
    # Add boolean modifier
    modifier = base.modifiers.new(name="MengerCut", type='BOOLEAN')
    modifier.operation = 'DIFFERENCE'
    modifier.object = cutter
    
    # Hide the cutter object
    cutter.hide_set(True)
    cutter.hide_render = True

# Setup animated camera and lighting
def setup_scene():
    # Create camera
    camera_data = bpy.data.cameras.new("Camera")
    camera = bpy.data.objects.new("Camera", camera_data)
    bpy.context.collection.objects.link(camera)
    camera.location = (10, -10, 10)
    camera.rotation_euler = (math.radians(60), 0, math.radians(45))
    bpy.context.scene.camera = camera

    # Create parent empty for animation
    bpy.ops.object.empty_add(location=(0, 0, 0))
    empty = bpy.context.object
    empty.name = "MengerParent"
    
    # Parent all objects to empty
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            obj.parent = empty

    # Animate rotation
    empty.rotation_euler = (0, 0, 0)
    empty.keyframe_insert(data_path="rotation_euler", frame=1)
    
    empty.rotation_euler = (0, 0, math.radians(360))
    empty.keyframe_insert(data_path="rotation_euler", frame=100)
    
    # Set animation length
    bpy.context.scene.frame_end = 100

    # Add lighting
    light_data = bpy.data.lights.new(name="SunLight", type='SUN')
    light = bpy.data.objects.new(name="SunLight", object_data=light_data)
    bpy.context.collection.objects.link(light)
    light.location = (15, -15, 15)
    light.rotation_euler = (math.radians(50), math.radians(30), 0)

# Parameters
iterations = 3  # Warning: Higher iterations (e.g., 4+) may crash Blender!
size = 3
location = (0, 0, 0)

# Execute
clear_scene()
create_menger_sponge(iterations, location, size)
# create_boolean_sponge()  # Uncomment for boolean example
setup_scene()

bl_info = {
    "name": "Starsiege Tribes DTS",
    "author": "CanisUrsa",
    "version": (0, 0, 1),
    "blender": (2, 90, 1),
    "location": "File > Import-Export > Starsiege Tribes DTS (.dts)",
    "description": "Imports a Starsiege Tribes DTS Shape",
    "category": "Import-Export",
}

import bpy
from bpy import context

from . import dts

from bpy.props import (
    BoolProperty,
    FloatProperty,
    StringProperty,
    EnumProperty,
)

from bpy_extras.io_utils import (
    ImportHelper,
    ExportHelper,
)

import mathutils
from math import radians

import os

def console_print(*args, **kwargs):
    for a in context.screen.areas:
        if a.type == 'CONSOLE':
            c = {}
            c['area'] = a
            c['space_data'] = a.spaces.active
            c['region'] = a.regions[-1]
            c['window'] = context.window
            c['screen'] = context.screen
            s = " ".join([str(arg) for arg in args])
            for line in s.split("\n"):
                bpy.ops.console.scrollback_append(c, text=line)


def print(*args, **kwargs):
    console_print(*args, **kwargs)


class ImportDTS(bpy.types.Operator, ImportHelper):
    """Load a Starsiege Tribes DTS File"""
    bl_idname = "import_scene.dts"
    bl_label = "Import DTS"
    bl_options = {"PRESET", "UNDO"}

    filename_ext = ".dts"
    filter_glob: StringProperty(
        default="*.dts",
        options={"HIDDEN"})

    def execute(self, context):
        keywords = self.as_keywords()
        filepath = keywords['filepath']
        
        shape = None
        with open(filepath, "rb") as f:
            shape = dts.DTSHeader()
            shape.read(f.read(), 0)

        if shape is None:
            return {"FINISHED"}

        blender_collections = bpy.data.collections
        blender_objects = bpy.data.objects
        
        name_map = {}
        material_name_map = {}
        shape = shape.data

        # Need to create the materials before hand
        for mat in shape.material_list.data.materials_list:
            # Get the name of the material
            mat_name = dts.make_string(mat.map_file)
            # Expect the material to be located next to the dts
            full_path = os.path.join(os.path.dirname(filepath), mat_name)

            # Create the material in blender
            blender_material = bpy.data.materials.new(mat_name)
            # Create a map of the name from dts world to blender world
            material_name_map[mat_name] = blender_material.name
            # Set the blender material to utilize nodes
            blender_material.use_nodes = True
            # Get the node from the material
            blender_bsdf = blender_material.node_tree.nodes["Principled BSDF"]
            # Setup the texture shader
            blender_texture = blender_material.node_tree.nodes.new("ShaderNodeTexImage")
            # Load the image into blender
            blender_texture.image = bpy.data.images.load(filepath=full_path)
            # Link the bsdf shader base color to the textures color (link material to the texture)
            blender_material.node_tree.links.new(blender_bsdf.inputs['Base Color'], blender_texture.outputs['Color'])

        # Need to create the objects now        
        blender_obj = None
        for obj in shape.object_list:
            # Get the name of the object
            obj_name = shape.name_list[obj.name_index].decode()
            # Get the mesh
            mesh = shape.mesh_list[obj.mesh_index].data
            # Get the node
            node = shape.node_list[obj.node_index]
            # Get the node name
            node_name = shape.name_list[node.name_index].decode()

            # Setup some lists for future use as the object is unpacked
            blender_vertex_list = []
            blender_edge_list = []
            blender_face_list = []
            face_to_texture_vertex = {}
            texture_vertex_list = []
            material_index = None

            # bounds doesn't have an actual mesh, need to reconstruct it, we can use the mesh or the bounds listed
            # in the shape. They differ. Don't know why....
            if obj_name.lower() == "bounds":
                dts_frame = mesh.frame_list[0]
                # Use the actual mesh vertices
                # bounds_min, normal = mesh.vertex_list[0].decode(dts_frame.scale, dts_frame.origin)
                # bounds_max, normal = mesh.vertex_list[1].decode(dts_frame.scale, dts_frame.origin)
                # Use the bounds in the shape
                bounds_min = shape.bounds.min.decode()
                bounds_max = shape.bounds.max.decode()
                blender_vertex_list.append((bounds_min[0], bounds_min[1], bounds_max[2]))
                blender_vertex_list.append((bounds_min[0], bounds_max[1], bounds_max[2]))
                blender_vertex_list.append((bounds_max[0], bounds_max[1], bounds_max[2]))
                blender_vertex_list.append((bounds_max[0], bounds_min[1], bounds_max[2]))
                blender_vertex_list.append((bounds_min[0], bounds_min[1], bounds_min[2]))
                blender_vertex_list.append((bounds_min[0], bounds_max[1], bounds_min[2]))
                blender_vertex_list.append((bounds_max[0], bounds_max[1], bounds_min[2]))
                blender_vertex_list.append((bounds_max[0], bounds_min[1], bounds_min[2]))
                blender_face_list.append([0, 1, 2])
                blender_face_list.append([2, 3, 0])
                blender_face_list.append([4, 5, 6])
                blender_face_list.append([6, 7, 4])
                blender_face_list.append([0, 3, 7])
                blender_face_list.append([7, 4, 0])
                blender_face_list.append([1, 2, 6])
                blender_face_list.append([6, 5, 1])
                blender_face_list.append([3, 2, 6])
                blender_face_list.append([6, 7, 3])
                blender_face_list.append([0, 1, 5])
                blender_face_list.append([5, 4, 0])

            # Create the vertex list
            for vertex_index in range(mesh.vertex_count):
                frame_index = int(vertex_index / mesh.vertex_per_frame_count)
                frame = mesh.frame_list[frame_index]
                vertex, normal = mesh.vertex_list[vertex_index].decode(frame.scale, frame.origin)
                blender_vertex_list.append(vertex)

            # Create a list of texture vertices
            for texture_vertex in mesh.texture_vertex_list:
                texture_vertex_list.append((texture_vertex.x, texture_vertex.y))

            # Create the face list
            for face in mesh.face_list:
                # Add the face to the face list
                blender_face_list.append(face.vertex_index_list)
                # Need a map of each face to each texture vertex so we can properly edit the UV later on
                face_vertices = (face.vertex_index_list[0], face.vertex_index_list[1], face.vertex_index_list[2])
                texture_vertices = (face.texture_index_list[0], face.texture_index_list[1], face.texture_index_list[2])
                face_to_texture_vertex[face_vertices] = texture_vertices
                # Assume there will be only a single material per mesh but each mesh can have its own material
                # This is probably a safe assumption but who knows!
                if material_index is None:
                    material_index = face.material

            # Create the mesh and container object
            blender_mesh = bpy.data.meshes.new(obj_name)
            blender_obj = blender_objects.new(blender_mesh.name, blender_mesh)
            # Add the name to the name map
            name_map[obj_name] = blender_obj.name
            # Link the container object to the collection
            blender_collections[0].objects.link(blender_obj)

            # Edit the mesh using the default_transform
            transform = shape.transform_list[node.default_transform_index]
            bpy.context.view_layer.objects.active = blender_obj
            blender_mesh.from_pydata(blender_vertex_list, blender_edge_list, blender_face_list)
            # Translate the mesh using the object offset
            vec = obj.offset.decode()
            blender_obj.location += mathutils.Vector(vec)
            # Translate the mesh using the default transform
            vec = transform.translate.decode() 
            blender_obj.location += mathutils.Vector(vec)
            # Rotate the mesh using the quaternion
            quat = transform.quat.decode()
            blender_obj.rotation_mode = 'QUATERNION'
            blender_obj.rotation_quaternion[0] = quat[0]
            blender_obj.rotation_quaternion[1] = quat[1]
            blender_obj.rotation_quaternion[2] = quat[2]
            blender_obj.rotation_quaternion[3] = quat[3]
            # Apply object sub sequence if applicable
            if obj.sub_sequence_count > 0:
                # Get the first sub sequence
                sub_sequence = shape.sub_sequence_list[obj.first_sub_sequence_index]
                # Apply key frame if applicable
                if sub_sequence.key_frame_count > 0:
                    key_frame = shape.key_frame_list[sub_sequence.first_key_frame_index]
                    # Generate a warning if the position is not 0.0
                    if key_frame.position != 0.0:
                        print(f"Default key frame for object {obj_name} has a non 0.0 position ({key_frame.position}).")
                    # Get the transform that applies to this key frame
                    transform = shape.transform_list[key_frame.key_value_index]
                    # Translate the mesh using the transform
                    vec = transform.translate.decode()
                    blender_obj.location += mathutils.Vector(vec)
                    # Rotate the mesh using the quaternion
                    quat = transform.quat.decode()
                    blender_obj.rotation_quaternion.rotate(mathutils.Quaternion())

            # Apply material to the mesh
            if material_index is not None:
                # Get the dts material name
                material_name = dts.make_string(shape.material_list.data.materials_list[material_index].map_file)
                # Get the blender material name from the dts material name
                material_name = material_name_map[material_name]
                # Get the previously created blender material
                blender_material = bpy.data.materials[material_name]
                # Assign the blender material to the blender object
                if blender_obj.data.materials:
                    blender_obj.data.materials[0] = blender_material
                else:
                    blender_obj.data.materials.append(blender_material)

                # Assign uv coordinates
                blender_uv = blender_obj.data.uv_layers.new()
                # Make the new uv layer the active one
                blender_obj.data.uv_layers.active = blender_uv
                # Iterate through each face in the mesh
                for face in blender_obj.data.polygons:
                    # This probably doesn't work all that well, will need to chang ethis
                    temp = (face.vertices[0], face.vertices[1], face.vertices[2])
                    texture_vertices = face_to_texture_vertex[temp]
                    # Update each uv texture coordinate to match what is in the dts
                    blender_uv.data[face.loop_indices[0]].uv = texture_vertex_list[texture_vertices[0]]
                    blender_uv.data[face.loop_indices[1]].uv = texture_vertex_list[texture_vertices[1]]
                    blender_uv.data[face.loop_indices[2]].uv = texture_vertex_list[texture_vertices[2]]

        # Create parent order
        # if the object name and node name differ then the object is a parent of that node
        # if the object name and node name are the same then the object is a parent of another node
        for obj in shape.object_list:
            obj_name = shape.name_list[obj.name_index].decode()
            node = shape.node_list[obj.node_index]
            node_name = shape.name_list[node.name_index].decode()

            if obj_name != node_name:
                # The object name and node name are different so the parent is obvious
                blender_objects[name_map[obj_name]].parent = blender_objects[name_map[node_name]]
            elif node.parent_index != -1:
                # The node has a parent
                parent = shape.node_list[node.parent_index]
                parent_name = shape.name_list[parent.name_index].decode()

                if parent_name not in name_map:
                    # If the parent doesn't exist then we may need to create it as a new blender object
                    blender_obj = blender_objects.new(parent_name, None)
                    name_map[parent_name] = blender_obj.name
                    blender_collections[0].objects.link(blender_obj)
                
                blender_objects[name_map[obj_name]].parent = blender_objects[name_map[parent_name]]
        
        # Set the frame rate
        bpy.context.scene.render.fps = 20

        # Animations are tied to nodes so work from the node to the animation
        for node in shape.node_list:
            # Get the node name
            node_name = shape.name_list[node.name_index].decode()
            # Get the blender object that maps to the node
            # This is the object that we are going to manipulate
            blender_obj = bpy.data.objects[name_map[node_name]]
            # Create the animation data for the blender object
            blender_obj.animation_data_create()
            # Iterate through each sub sequence in the node
            for sub_sequence_index in range(node.sub_sequence_count):
                # Get the sub sequence
                sub_sequence = shape.sub_sequence_list[node.first_sub_sequence_index + sub_sequence_index]
                # Get the sequence
                sequence = shape.sequence_list[sub_sequence.sequence_index]
                # Get the sequence name
                sequence_name = shape.name_list[sequence.name_index].decode()

                # Create a track for this animation
                blender_track = blender_obj.animation_data.nla_tracks.new()
                blender_track.name = sequence_name
                # Create an action for this animation
                blender_action = bpy.data.actions.new(sequence_name)
                # Assign the track and action to the object
                blender_obj.animation_data.action = blender_action
                blender_obj.animation_data.nla_tracks.active = blender_track

                # Iterate through the key frames
                for key_frame_index in range(sub_sequence.key_frame_count):
                    # Get the key frame
                    key_frame = shape.key_frame_list[sub_sequence.first_key_frame_index + key_frame_index]
                    # Get the transform
                    transform = shape.transform_list[key_frame.key_value_index]
                    # Determine the frame number at 20 frames per second
                    bpy.context.scene.frame_set(int(key_frame.position / 0.05))
                    # Translate the object
                    blender_obj.location = mathutils.Vector(transform.translate.decode())
                    # Rotate the object
                    blender_obj.rotation_quaternion = mathutils.Quaternion(transform.quat.decode())
                    # Insert the translation key frame
                    blender_obj.keyframe_insert(data_path="location", index=-1)
                    # Insert the rotation key frame
                    blender_obj.keyframe_insert(data_path="rotation_quaternion", index=-1)
                
                # Move action into the track
                blender_track.strips.new(blender_action.name, blender_action.frame_range[0], blender_action)
        
        return {"FINISHED"}

    def draw(self, context):
        pass


def menu_func_import(self, context):
    self.layout.operator(ImportDTS.bl_idname, text="Starsiege Tribes DTS (.dts)")


def register():
    bpy.utils.register_class(ImportDTS)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

    bpy.utils.unregister_class(ImportDTS)


if __name__ == "__main__":
    register()

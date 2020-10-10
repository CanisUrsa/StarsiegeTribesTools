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
        
        # name_map = {}
        shape = shape.data
        # collection_name_map = {}

        for dts_obj in shape.object_list:
            dts_name = shape.name_list[dts_obj.name_index].decode()
            dts_obj_offset = dts_obj.offset
            dts_mesh = shape.mesh_list[dts_obj.mesh_index].data
            dts_node = shape.node_list[dts_obj.node_index]
            dts_transform = shape.transform_list[dts_node.default_transform_index]
            dts_quat = dts_transform.quat.decode()

            # dts_node_name = shape.name_list[dts_node.name_index].decode()
            # if dts_node_name not in collection_name_map:
            #     c = bpy.data.collections.new(dts_node_name)
            #     collection_name_map[dts_node_name] = c.name

            new_vertex_list = []
            new_edge_list = []
            new_face_list = []

            if dts_name.lower() == "bounds":
                dts_frame = dts_mesh.frame_list[0]
                bounds_min, normal = dts_mesh.vertex_list[0].decode(dts_frame.scale, dts_frame.origin)
                bounds_max, normal = dts_mesh.vertex_list[1].decode(dts_frame.scale, dts_frame.origin)
                new_vertex_list.append((bounds_min[0], bounds_min[1], bounds_max[2]))
                new_vertex_list.append((bounds_min[0], bounds_max[1], bounds_max[2]))
                new_vertex_list.append((bounds_max[0], bounds_max[1], bounds_max[2]))
                new_vertex_list.append((bounds_max[0], bounds_min[1], bounds_max[2]))
                new_vertex_list.append((bounds_min[0], bounds_min[1], bounds_min[2]))
                new_vertex_list.append((bounds_min[0], bounds_max[1], bounds_min[2]))
                new_vertex_list.append((bounds_max[0], bounds_max[1], bounds_min[2]))
                new_vertex_list.append((bounds_max[0], bounds_min[1], bounds_min[2]))
                new_face_list.append([0, 1, 2])
                new_face_list.append([2, 3, 0])
                new_face_list.append([4, 5, 6])
                new_face_list.append([6, 7, 4])
                new_face_list.append([0, 3, 7])
                new_face_list.append([7, 4, 0])
                new_face_list.append([1, 2, 6])
                new_face_list.append([6, 5, 1])
                new_face_list.append([3, 2, 6])
                new_face_list.append([6, 7, 3])
                new_face_list.append([0, 1, 5])
                new_face_list.append([5, 4, 0])

            dts_frame_index = 0
            dts_frame = dts_mesh.frame_list[dts_frame_index]
            for dts_vertex_index in range(dts_mesh.vertex_count):
                if (dts_frame_index + 1) < dts_mesh.frame_count and \
                    dts_mesh.frame_list[dts_frame_index + 1].first_vertex_index == dts_vertex_index:
                    dts_frame_index += 1
                    dts_frame = dts_mesh.frame_list[dts_frame_index]
                
                dts_vertex, dts_normal = dts_mesh.vertex_list[dts_vertex_index].decode(dts_frame.scale, dts_frame.origin)
                new_vertex_list.append(dts_vertex)

            for dts_face in dts_mesh.face_list:
                new_face_list.append(dts_face.vertex_index_list)

            new_mesh = bpy.data.meshes.new(dts_name)
            new_obj = bpy.data.objects.new(new_mesh.name, new_mesh)
            # name_map[dts_name] = new_mesh.name
            bpy.data.collections[0].objects.link(new_obj)
            bpy.context.view_layer.objects.active = new_obj
            new_mesh.from_pydata(new_vertex_list, new_edge_list, new_face_list)
            new_obj.rotation_mode = 'QUATERNION'
            new_obj.rotation_quaternion[0] = dts_quat[0]
            new_obj.rotation_quaternion[1] = dts_quat[1]
            new_obj.rotation_quaternion[2] = dts_quat[2]
            new_obj.rotation_quaternion[3] = dts_quat[3]

            # translates = []
            # translates.append(mathutils.Vector((dts_obj_offset.x, dts_obj_offset.y, dts_obj_offset.z)))
            # translates.append(mathutils.Vector((dts_transform.translate.x, dts_transform.translate.y, dts_transform.translate.z)))
            # quats = []
            # quats.append(mathutils.Quaternion((dts_quat[3], dts_quat[0], dts_quat[1], dts_quat[2])))
            # new_obj.location += mathutils.Vector((dts_obj_offset.x, dts_obj_offset.y, dts_obj_offset.z))
            # new_obj.location += mathutils.Vector((dts_transform.translate.x, dts_transform.translate.y, dts_transform.translate.z))

            # while dts_node.parent_index != -1:
            #     dts_node = shape.node_list[dts_node.parent_index]
            #     dts_transform = shape.transform_list[dts_node.default_transform_index]
            #     dts_quat = dts_transform.quat.decode()

                # new_obj_rot.rotate(mathutils.Quaternion((dts_quat[3], dts_quat[0], dts_quat[1], dts_quat[2])))
                # quats.append(mathutils.Quaternion((dts_quat[3], dts_quat[0], dts_quat[1], dts_quat[2])))
                
                # translates.append(mathutils.Vector((dts_transform.translate.x, dts_transform.translate.y, dts_transform.translate.z)))
                # new_obj.location += mathutils.Vector((dts_transform.translate.x, dts_transform.translate.y, dts_transform.translate.z))

            
            # for t in translates:
            #     new_obj.location += t
            # new_obj.location += translates[0]

            # new_obj_rot = None
            # for q in reversed(quats):
            #     if new_obj_rot is None:
            #         new_obj_rot = q
            #     else:
            #         # pass
            #         new_obj_rot.rotate(q)
            
            # new_obj.rotation_quaternion[0] = new_obj_rot[0]
            # new_obj.rotation_quaternion[1] = new_obj_rot[1]
            # new_obj.rotation_quaternion[2] = new_obj_rot[2]
            # new_obj.rotation_quaternion[3] = new_obj_rot[3]

            

            

            # dts_vertex_list = shape.data.mesh_list[-1].data.vertex_list
            # scale = shape.data.mesh_list[-1].data.frame_list[-1].scale
            # origin = shape.data.mesh_list[-1].data.frame_list[-1].origin
            # for i in range(shape.data.mesh_list[-1].data.vertex_count):
            #     vertex, normal = dts_vertex_list[i].decode(scale, origin)
            #     new_vertex_list.append((vertex.x, vertex.y, vertex.z))

            # dts_face_list = shape.data.mesh_list[-1].data.face_list
            # for i in range(shape.data.mesh_list[-1].data.face_count):
            #     dts_face = dts_face_list[i]
            #     new_face_list.append(dts_face.vertex_index_list)

            # mesh = bpy.data.meshes.new("importedmesh")
            # obj = bpy.data.objects.new(mesh.name, mesh)
            # col = bpy.data.collections[0]
            # col.objects.link(obj)
            # bpy.context.view_layer.objects.active = obj

            # mesh.from_pydata(new_vertex_list, new_edge_list, new_face_list)

        # print("Linking now...")
        # print(f"{name_map}")

        # for dts_obj in shape.object_list:
        #     dts_node = shape.node_list[dts_obj.node_index]

        #     print(f"Linking node [{dts_obj.node_index}] with [{dts_node.parent_index}]")

        #     if dts_node.parent_index != -1:
        #         parent_node = shape.node_list[dts_node.parent_index]
        #         parent_name = shape.name_list[parent_node.name_index].decode()
        #         new_obj.parent = bpy.data.objects[name_map[parent_name]]
        #         print(f"Linking {parent_name} to {name_map[parent_name]}")
        
        return {"FINISHED"}

# import bpy

# mesh = bpy.data.meshes.new("myBeautifulMesh")  # add the new mesh
# obj = bpy.data.objects.new(mesh.name, mesh)
# col = bpy.data.collections.get("Collection")
# col.objects.link(obj)
# bpy.context.view_layer.objects.active = obj

# verts = [( 1.0,  1.0,  0.0), 
#          ( 1.0, -1.0,  0.0),
#          (-1.0, -1.0,  0.0),
#          (-1.0,  1.0,  0.0),
#          ]  # 4 verts made with XYZ coords
# edges = []
# faces = [[0, 1, 2, 3]]

# mesh.from_pydata(verts, edges, faces)

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

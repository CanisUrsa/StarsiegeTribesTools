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
        
        shape = shape.data
        for dts_obj in shape.object_list:
            dts_name = shape.name_list[dts_obj.name_index].decode()
            if dts_name.lower() == "bounds":
                continue
            dts_obj_offset = dts_obj.offset
            dts_mesh = shape.mesh_list[dts_obj.mesh_index].data

            new_vertex_list = []
            new_edge_list = []
            new_face_list = []

            dts_frame_index = 0
            dts_frame = dts_mesh.frame_list[dts_frame_index]
            for dts_vertex_index in range(dts_mesh.vertex_count):
                if (dts_frame_index + 1) < dts_mesh.frame_count and \
                    dts_mesh.frame_list[dts_frame_index + 1].first_vertex_index == dts_vertex_index:
                    dts_frame_index += 1
                    dts_frame = dts_mesh.frame_list[dts_frame_index]
                
                dts_vertex, dts_normal = dts_mesh.vertex_list[dts_vertex_index].decode(dts_frame.scale, dts_frame.origin)
                new_vertex_list.append((dts_vertex.x + dts_obj_offset.x, dts_vertex.y + dts_obj_offset.y, dts_vertex.z + dts_obj_offset.z))

            for dts_face in dts_mesh.face_list:
                new_face_list.append(dts_face.vertex_index_list)

            new_mesh = bpy.data.meshes.new(dts_name)
            new_obj = bpy.data.objects.new(new_mesh.name, new_mesh)
            bpy.data.collections[0].objects.link(new_obj)
            bpy.context.view_layer.objects.active = new_obj
            new_mesh.from_pydata(new_vertex_list, new_edge_list, new_face_list)

            
            

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

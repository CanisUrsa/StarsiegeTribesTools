import struct

###############################################################################
# File Format:
###############################################################################
#  tag                                  : I32                               This is always PERS (0x50455253).
#  length                               : I32                               The length of the data in bytes.
#  name_size                            : I16                               The size of the name.
#  name                                 : Str[name_size]                    The name of the class this data is for. 
#                                                                           If name_size is odd, this is actually 1 more character in length.
#  version                              : I32                               The version number of the tag data.
#  data  --------------------------------                                   -
#    node_count                         : I32                               -
#    sequence_count                     : I32                               -
#    sub_sequence_count                 : I32                               -
#    key_frame_count                    : I32                               -
#    transform_count                    : I32                               -
#    name_count                         : I32                               -
#    object_count                       : I32                               -
#    detail_count                       : I32                               -
#    mesh_count                         : I32                               -
#    transition_count                   : I32                               -
#    frame_trigger_count                : I32                               -
#    radius                             : F32                               This is used for gross clipping and detail selection.
#    center -----------------------------                                   The center of the shape.
#      x                                : F32                               -
#      y                                : F32                               -
#      z                                : F32                               -
#    bounds -----------------------------                                   The bounds of the shape.
#      min ------------------------------                                   -
#        x                              : F32                               -
#        y                              : F32                               -
#        z                              : F32                               -
#      max ------------------------------                                   -
#        x                              : F32                               -
#        y                              : F32                               -
#        z                              : F32                               -
#    node_list -------------------------- [node_count]                      -
#      name_index                       : I16                               The index into the name list for the name of the node.
#      parent_index                     : I16                               The index into the node list for the parent node.
#      sub_sequence_count               : I16                               The number of sub sequences in the node.
#      first_sub_sequence_index         : I16                               The index into the sub sequence list for the first sub sequence of the node.
#      default_transform_index          : I16                               The index into the transform list for the default transform.
#    sequence_list ---------------------- [sequence_count]                  -
#      name_index                       : I32                               The index into the name list for the name of the sequence.
#      cyclic                           : I32                               ????
#      duration                         : F32                               The duration of the sequence in seconds.
#      priority                         : I32                               ????
#      first_frame_trigger_index        : I32                               The index into the frame trigger list for the first frame trigger of the sequence.
#      frame_trigger_count              : I32                               The number of frame triggers in the sequence.
#      IFL_sub_sequence_count           : I32                               The number of IFL (Image File List) sub sequences in the sequence. 
#                                                                           https://knowledge.autodesk.com/support/3ds-max/learn-explore/caas/CloudHelp/cloudhelp/2016/ENU/3DSMax/files/GUID-CA63616D-9E87-42FC-8E84-D67E1990EE71-htm.html
#      first_IFL_sub_sequence_index     : I32                               The index into the sub sequence list for the first IFL sub sequence of the sequence.
#    sub_sequence_list ------------------ [sub_sequence_count]              -
#      sequence_index                   : I32                               The index into the sequence list this sub sequence relates to. 
#      key_frame_count                  : I32                               The number of key frames in the sub sequences.
#      first_key_frame_index            : I32                               The index of the first key frame of the sub sequence.
#    key_frame_list --------------------- [key_frame_count]                 -
#      position                         : F32                               ????
#      key_value_index                  : U16                               The index into the transform array for node sub sequences.
#                                                                           The index into the mesh array for cel sub sequences.
#      material_index                   : U16                               The material index of the key frame with additional meta data.
#                                                                           Bit 15 indicates visibility.
#                                                                           Bit 14 indicates cares about visibility.
#                                                                           Bit 13 indicates cares about material.
#                                                                           Bit 12 indicates cares about frame.
#                                                                           Bit 11:0 is the material index. Not relavent for node sub sequences.
#    transform_list --------------------- [transform_count]                 -
#      quat -----------------------------                                   The rotation quaternion for the transform.
#        x                              : I16                               -
#        y                              : I16                               -
#        z                              : I16                               -
#        w                              : I16                               -
#      translate ------------------------                                   The translation for the transform.
#        x                              : F32                               -
#        y                              : F32                               -
#        z                              : F32                               -
#    name_list -------------------------- [name_count]                      -
#      name                             : Str[24]                           The name of the named thing (node, sequence, etc.).
#    object_list ------------------------ [object_count]                    -
#      name_index                       : I16                               The index into the name list for the name of the object.
#      flags                            : I16                               ????
#                                                                           Bit 0 : Default Invisible.
#      mesh_index                       : I32                               The index into the mesh list for the mesh of the object.
#      node_index                       : I16                               The index into the node list for the node of the object.
#      padding                          : I16                               Byte alignment padding.
#      offset ---------------------------                                   ????
#        x                              : F32                               -
#        y                              : F32                               -
#        z                              : F32                               -
#      sub_sequence_count               : I16                               The number of sub sequences for the object.
#      first_sub_sequence_index         : I16                               The index of the first sub sequence for the object.
#    detail_list ------------------------ [detail_count]                    -
#      root_node_index                  : I32                               The index into the node list that represents the root node of the detail.
#      min_size                         : F32                               The minimum projected size of the detail.
#    transition_list -------------------- [transition_count]                -
#      start_sequence_index             : I32                               The index into the sequence array indicating the first sequence in the transition.
#      end_sequence_index               : I32                               The index into the sequence array indicating the last sequence in the transition.
#      start_position                   : F32                               The first position of the transition.
#      end_position                     : F32                               The last position of the transition.
#      duration                         : F32                               The duration of the sequence in seconds.
#      transform ------------------------                                   -
#        quat ---------------------------                                   The rotation quaternion for the transition.
#          x                            : I16                               -
#          y                            : I16                               -
#          z                            : I16                               -
#          w                            : I16                               -
#        translate ----------------------                                   The translation for the transition.
#          x                            : F32                               -
#          y                            : F32                               -
#          z                            : F32                               -
#    frame_trigger_list ----------------- [frame_trigger_count]             -
#      position                         : F32                               ????
#      value                            : I32                               ????
#    default_materials                  : I32                               The number of default materials for the shape.
#    always_node                        : I32                               The index of the node to always animate and draw regardless of detail. -1 indicates no always node.
#    mesh_list -------------------------- [mesh_count]                      -
#      tag                              : I32                               This is always PERS (0x50455253).
#      length                           : I32                               The length of the data in bytes.
#      name_size                        : I16                               The size of the name.
#      name                             : Str[name_size]                    The name of the class this data is for. 
#                                                                           If name_size is odd, this is actually 1 more character in length.
#      version                          : I32                               The version number of the tag data.
#      data -----------------------------                                   -
#        vertex_count                   : I32                               The number of verticies in the mesh.
#        vertex_per_frame_count         : I32                               The number of verticies per frame in the mesh.
#        texture_vertex_count           : I32                               The number of texture veriticies in the mesh.
#        face_count                     : I32                               The number of faces in the mesh.
#        frame_count                    : I32                               The number of frames in the mesh.
#        texture_vertex_per_frame_count : I32                               The number of texture verticies per frame in the mesh.
#        radius                         : F32                               Used for clipping sphere.
#        vertex_list -------------------- [vertex_count]                    -
#          x                            : U8                                The vertex x position. Needs to be scaled and offset with the scale and origin found in the related frame.
#          y                            : U8                                The vertex y position. Needs to be scaled and offset with the scale and origin found in the related frame.
#          z                            : U8                                The vertex z position. Needs to be scaled and offset with the scale and origin found in the related frame.
#          normal                       : U8                                The vertex normal. Tribes apparently only supports 256 unique normals. Table of supported normals can be found below.
#        texture_vertex_list ------------ [texture_vertex_count]            -
#          x                            : F32                               The texture vertex x position.
#          y                            : F32                               The texture vertex y position.
#        face_list ---------------------- [face_count]                      -
#          vertex_index_list            : I32[3]                            The 3 vertex indicies that make up the face.
#          texture_index_list           : I32[3]                            The 3 texture vertex indicies that make up the texture of the face.
#          material                     : I32                               The material of the face.
#        frame_list --------------------- [frame_count]                     -
#          first_vertex_index           : I32                               The index of the first vertex in the frame. Use vertex_per_frame_count to know how many verticies apply to this frame.
#          scale ------------------------                                   The scale to use for the verticies that apply to this frame.
#            x                          : F32                               -
#            y                          : F32                               -
#            z                          : F32                               -
#          origin -----------------------                                   The offset to use for the verticies that apply to this frame.
#            x                          : F32                               -
#            y                          : F32                               -
#            z                          : F32                               -
#    has_materials                      : I32                               If 1 then the shape has a material list. Otherwise the following material won't be contained in the file.
#    material_list ----------------------                                   -
#      tag                              : I32                               This is always PERS (0x50455253).
#      length                           : I32                               The length of the data in bytes.
#      name_size                        : I16                               The size of the name.
#      name                             : Str[name_size]                    The name of the class this data is for. 
#                                                                           If name_size is odd, this is actually 1 more character in length.
#      version                          : I32                               The version number of the tag data.
#      data -----------------------------                                   -
#        detail_count                   : I32                               The number of details in the material.
#        material_count                 : I32                               The number of materials per detail.
#        material_list ------------------ [detail_count * material_count]   -
#          flags                        : I32                               ????
#          alpha                        : F32                               ????
#          index                        : I32                               Apparently used for palette types.
#          color_r                      : U8                                Amount of red.
#          color_g                      : U8                                Amount of green.
#          color_b                      : U8                                Amount of blue.
#          color_flags                  : U8                                Flags for RGB types.
#          map_file                     : Str[32]                           The name of the map file for the material.
#          type                         : I32                               The type of the material.
#          elasticity                   : F32                               The elasticity of the material.
#          friction                     : F32                               The friction of the material.
#          use_default_props            : U32                               If 0 the material doesn't use default properties, otherwise it does.
#
# Other things of interest
# MatType
#   MatFlags = 0x0F
#   MatNull = 0x00
#   MatPalette = 0x01
#   MatRGB = 0x02
#   MatTexture = 0x03
# ShadingType
#   ShadingFlags = 0xF00
#   ShadingNone = 0x100
#   ShadingFlag = 0x200
#   ShadingSmooth = 0x300
# TextureType
#   TextureFlags = 0xF000
#   TextureTransparent = 0x1000
#   TextureTranslucent = 0x2000
# SurfaceType
#   DefaultType = 0x0
#   ConcreteType = 0x1
#   CarpetType = 0x2
#   MetalType = 0x3
#   GlassType = 0x4
#   PlasticType = 0x5
#   WoodType = 0x6
#   MarbleType = 0x7
#   SnowType = 0x8
#   IceType = 0x9
#   SandType = 0xA
#   MudType = 0xB
#   StoneType = 0xC
#   SoftEarthType = 0xD
#   PackedEarthType = 0xE

###############################################################################
# DTS Base
###############################################################################
class DTSBase():
    """Base class for DTS data structures."""

    def __init__(self, format):
        self.format = format

    def size(self):
        if isinstance(self.format, list):
            return sum([struct.calcsize(x) for x in self.format])
        else:
            return struct.calcsize(self.format)


###############################################################################
# DTS Header
###############################################################################
class DTSHeader(DTSBase):
    """DTS Header data structure."""

    def __init__(self):
        super().__init__(["<iih", "<0s", "<i"])
        self.tag = 0       # I32
        self.length = 0    # I32
        self.name_size = 0 # I16
        self.name = ""     # Str
        self.version = 0   # I32
        self.data = None   # Variable depending on name

    def pretty(self, level=0, max_level=9999):
        if level > max_level:
            return ""
        return \
f"""DTSHeader(
{"  " * level}  tag={self.tag},
{"  " * level}  length={self.length},
{"  " * level}  name_size={self.name_size},
{"  " * level}  name={self.name},
{"  " * level}  version={self.version},
{"  " * level}  data={self.data.pretty(level + 2, max_level)}
{"  " * level})"""

    def size(self):
        t = super().size()
        if self.data is not None:
            t += self.data.size()
        return t
    
    def read(self, buffer, offset):
        self.tag, \
        self.length, \
        self.name_size = struct.unpack_from(self.format[0], buffer, offset)
        offset += struct.calcsize(self.format[0])
        
        self.format[1] = f"<{(self.name_size + 1) & (~1)}s"
        self.name, = struct.unpack_from(self.format[1], buffer, offset)
        offset += struct.calcsize(self.format[1])
        
        self.version, = struct.unpack_from(self.format[2], buffer, offset)
        offset += struct.calcsize(self.format[2])

        if self.name == b'TS::Shape\00':
            self.data = DTSTSShape()
        elif self.name == b'TS::CelAnimMesh\00':
            self.data = DTSTSCelAnimMesh()
        elif self.name == b'TS::MaterialList':
            self.data = DTSTSMaterialList()
        else:
            raise ValueError(f"Unsupported name {self.name}")
        offset = self.data.read(buffer, offset)

        return offset

    def write(self, buffer, offset):
        struct.pack_into(self.format[0], buffer, offset, 
                         self.tag,
                         self.length,
                         self.name_size)
        offset += struct.calcsize(self.format[0])

        struct.pack_into(self.format[1], buffer, offset,
                         self.name)
        offset += struct.calcsize(self.format[1])

        struct.pack_into(self.format[2], buffer, offset,
                         self.version)
        offset += struct.calcsize(self.format[2])

        offset = self.data.write(buffer, offset)
        
        return offset



###############################################################################
# DTS TS Shape
###############################################################################
class DTSTSShape(DTSBase):
    def __init__(self):
        super().__init__(["<iiiiiiiiiiif", "<ii", "<i"])
        self.node_count = 0              # I32
        self.sequence_count = 0          # I32
        self.sub_sequence_count = 0      # I32
        self.key_frame_count = 0         # I32
        self.transform_count = 0         # I32
        self.name_count = 0              # I32
        self.object_count = 0            # I32
        self.detail_count = 0            # I32
        self.mesh_count = 0              # I32
        self.transition_count = 0        # I32
        self.frame_trigger_count = 0     # I32
        self.radius = 0.0                # F32
        self.center = DTSPoint3F()       # DTSPoint3F
        self.bounds = DTSBox3F()         # Box3F
        self.node_list = []              # list[DTSNode]
        self.sequence_list = []          # list[DTSSequence]
        self.sub_sequence_list = []      # list[DTSSubSequence]
        self.key_frame_list = []         # list[DTSKeyFrame]
        self.transform_list = []         # list[DTSTransform]
        self.name_list = []              # list[DTSName]
        self.object_list = []            # list[DTSObject]
        self.detail_list = []            # list[DTSDetail]
        self.transition_list = []        # list[DTSTransition]
        self.frame_trigger_list = []     # list[DTSFrameTrigger]
        self.default_materials = 0       # I32
        self.always_node = 0             # I32
        self.mesh_list = []              # list[DTSHeader]
        self.has_materials = 0           # I32
        self.material_list = DTSHeader() # DTSHeader

    def pretty(self, level=0, max_level=9999):
        if level > max_level:
            return ""
        material_list_str = "None"
        if self.has_materials != 0:
            material_list_str = self.material_list.pretty(level + 2, max_level)
        return \
f"""DTSTSShape(
{"  " * level}  node_count={self.node_count}, 
{"  " * level}  sequence_count={self.sequence_count}, 
{"  " * level}  sub_sequence_count={self.sub_sequence_count},
{"  " * level}  key_frame_count={self.key_frame_count},
{"  " * level}  transform_count={self.transform_count},
{"  " * level}  name_count={self.name_count},
{"  " * level}  object_count={self.object_count},
{"  " * level}  detail_count={self.detail_count},
{"  " * level}  mesh_count={self.mesh_count},
{"  " * level}  transition_count={self.transition_count},
{"  " * level}  frame_trigger_count={self.frame_trigger_count},
{"  " * level}  radius={self.radius},
{"  " * level}  center={self.center.pretty(level + 2, max_level)},
{"  " * level}  bounds={self.bounds.pretty(level + 2, max_level)},
{"  " * level}  node_list=[{','.join([x.pretty(level + 2, max_level) for x in self.node_list])}
{"  " * level}  ],
{"  " * level}  sequence_list=[{','.join([x.pretty(level + 2, max_level) for x in self.sequence_list])}
{"  " * level}  ],
{"  " * level}  sub_sequence_list=[{','.join([x.pretty(level + 2, max_level) for x in self.sub_sequence_list])}
{"  " * level}  ],
{"  " * level}  key_frame_list=[{','.join([x.pretty(level + 2, max_level) for x in self.key_frame_list])}
{"  " * level}  ],
{"  " * level}  transform_list=[{','.join([x.pretty(level + 2, max_level) for x in self.transform_list])}
{"  " * level}  ],
{"  " * level}  name_list=[{','.join([x.pretty(level + 2, max_level) for x in self.name_list])}
{"  " * level}  ],
{"  " * level}  object_list=[{','.join([x.pretty(level + 2, max_level) for x in self.object_list])}
{"  " * level}  ],
{"  " * level}  detail_list=[{','.join([x.pretty(level + 2, max_level) for x in self.detail_list])}
{"  " * level}  ],
{"  " * level}  transition_list=[{','.join([x.pretty(level + 2, max_level) for x in self.transition_list])}
{"  " * level}  ],
{"  " * level}  frame_trigger_list=[{','.join([x.pretty(level + 2, max_level) for x in self.frame_trigger_list])}
{"  " * level}  ],
{"  " * level}  default_materials={self.default_materials},
{"  " * level}  always_node={self.always_node},
{"  " * level}  mesh_list=[{','.join([x.pretty(level + 2, max_level) for x in self.mesh_list])}
{"  " * level}  ],
{"  " * level}  has_materials={self.has_materials},
{"  " * level}  material_list={material_list_str}
{"  " * level})"""

    def size(self):
        return struct.calcsize(self.format[0]) + \
               self.center.size() + \
               self.bounds.size() + \
               sum([x.size() for x in self.node_list]) + \
               sum([x.size() for x in self.sequence_list]) + \
               sum([x.size() for x in self.sub_sequence_list]) + \
               sum([x.size() for x in self.key_frame_list]) + \
               sum([x.size() for x in self.transform_list]) + \
               sum([x.size() for x in self.name_list]) + \
               sum([x.size() for x in self.object_list]) + \
               sum([x.size() for x in self.detail_list]) + \
               sum([x.size() for x in self.transition_list]) + \
               sum([x.size() for x in self.frame_trigger_list]) + \
               struct.calcsize(self.format[1]) + \
               sum([x.size() for x in self.mesh_list]) + \
               struct.calcsize(self.format[2]) + \
               self.material_list.size()

    def read(self, buffer, offset):       
        self.node_count, \
        self.sequence_count, \
        self.sub_sequence_count, \
        self.key_frame_count, \
        self.transform_count, \
        self.name_count, \
        self.object_count, \
        self.detail_count, \
        self.mesh_count, \
        self.transition_count, \
        self.frame_trigger_count, \
        self.radius = struct.unpack_from(self.format[0], buffer, offset)
        offset += struct.calcsize(self.format[0])

        offset = self.center.read(buffer, offset)
        offset = self.bounds.read(buffer, offset)

        self.node_list, offset = read_many(DTSNode, self.node_count, buffer, offset)
        self.sequence_list, offset = read_many(DTSSequence, self.sequence_count, buffer, offset)
        self.sub_sequence_list, offset = read_many(DTSSubSequence, self.sub_sequence_count, buffer, offset)
        self.key_frame_list, offset = read_many(DTSKeyFrame, self.key_frame_count, buffer, offset)
        self.transform_list, offset = read_many(DTSTransform, self.transform_count, buffer, offset)
        self.name_list, offset = read_many(DTSName, self.name_count, buffer, offset)
        self.object_list, offset = read_many(DTSObject, self.object_count, buffer, offset)
        self.detail_list, offset = read_many(DTSDetail, self.detail_count, buffer, offset)
        self.transition_list, offset = read_many(DTSTransition, self.transition_count, buffer, offset)
        self.frame_trigger_list, offset = read_many(DTSFrameTrigger, self.frame_trigger_count, buffer, offset)

        self.default_materials, \
        self.always_node = struct.unpack_from(self.format[1], buffer, offset)
        offset += struct.calcsize(self.format[1])

        self.mesh_list, offset = read_many(DTSHeader, self.mesh_count, buffer, offset)

        self.has_materials, = struct.unpack_from(self.format[2], buffer, offset)
        offset += struct.calcsize(self.format[2])

        if self.has_materials != 0:
            offset = self.material_list.read(buffer, offset)
        
        return offset

    def write(self, buffer, offset):
        struct.pack_into(self.format[0], buffer, offset,
                         self.node_count,
                         self.sequence_count,
                         self.sub_sequence_count,
                         self.key_frame_count,
                         self.transform_count,
                         self.name_count,
                         self.object_count,
                         self.detail_count,
                         self.mesh_count,
                         self.transition_count,
                         self.frame_trigger_count,
                         self.radius)
        offset += struct.calcsize(self.format[0])

        offset = self.center.write(buffer, offset)
        offset = self.bounds.write(buffer, offset)

        offset = write_many(self.node_list, buffer, offset)
        offset = write_many(self.sequence_list, buffer, offset)
        offset = write_many(self.sub_sequence_list, buffer, offset)
        offset = write_many(self.key_frame_list, buffer, offset)
        offset = write_many(self.transform_list, buffer, offset)
        offset = write_many(self.name_list, buffer, offset)
        offset = write_many(self.object_list, buffer, offset)
        offset = write_many(self.detail_list, buffer, offset)
        offset = write_many(self.transition_list, buffer, offset)
        offset = write_many(self.frame_trigger_list, buffer, offset)

        struct.pack_into(self.format[1], buffer, offset,
                         self.default_materials,
                         self.always_node)
        offset += struct.calcsize(self.format[1])

        offset = write_many(self.mesh_list, buffer, offset)

        struct.pack_into(self.format[2], buffer, offset,
                         self.has_materials)
        offset += struct.calcsize(self.format[2])

        if self.has_materials != 0:
            offset = self.material_list.write(buffer, offset)
        
        return offset


###############################################################################
# DTS Point 3F
###############################################################################
class DTSPoint3F(DTSBase):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        super().__init__("<fff")
        self.x = x # F32
        self.y = y # F32
        self.z = z # F32

    def pretty(self, level=0, max_level=9999):
        if level > max_level:
            return ""
        return \
f"""DTSPoint3F(
{"  " * level}  x={self.x},
{"  " * level}  y={self.y},
{"  " * level}  z={self.z}
{"  " * level})"""

    def read(self, buffer, offset):
        self.x, \
        self.y, \
        self.z = struct.unpack_from(self.format, buffer, offset)
        offset += struct.calcsize(self.format)

        return offset

    def write(self, buffer, offset):
        struct.pack_into(self.format, buffer, offset,
                         self.x,
                         self.y,
                         self.z)
        offset += struct.calcsize(self.format)

        return offset


###############################################################################
# DTS Box 3F
###############################################################################
class DTSBox3F(DTSBase):
    def __init__(self):
        super().__init__("<")
        self.min = DTSPoint3F() # DTSPoint3F
        self.max = DTSPoint3F() # DTSPoint3F

    def pretty(self, level=0, max_level=9999):
        if level > max_level:
            return ""
        return \
f"""DTSBox3F(
{"  " * level}  min={self.min.pretty(level + 1, max_level)},
{"  " * level}  max={self.max.pretty(level + 1, max_level)}
{"  " * level})"""

    def size(self):
        return self.min.size() + \
               self.max.size()

    def read(self, buffer, offset):
        offset = self.min.read(buffer, offset)
        offset = self.max.read(buffer, offset)
        
        return offset

    def write(self, buffer, offset):
        offset = self.min.write(buffer, offset)
        offset = self.max.write(buffer, offset)
        
        return offset


###############################################################################
# DTS Node
###############################################################################
class DTSNode(DTSBase):
    def __init__(self):
        super().__init__("<hhhhh")
        self.name_index = 0               # I16
        self.parent_index = 0             # I16
        self.sub_sequence_count = 0       # I16 
        self.first_sub_sequence_index = 0 # I16
        self.default_transform_index = 0  # I16

    def pretty(self, level=0, max_level=9999):
        if level > max_level:
            return ""
        return \
f"""DTSNode(
{"  " * level}  name_index={self.name_index},
{"  " * level}  parent_index={self.parent_index},
{"  " * level}  sub_sequence_count={self.sub_sequence_count},
{"  " * level}  first_sub_sequence_index={self.first_sub_sequence_index},
{"  " * level}  default_transform_index={self.default_transform_index}
{"  " * level})"""

    def read(self, buffer, offset):
        self.name_index, \
        self.parent_index, \
        self.sub_sequence_count, \
        self.first_sub_sequence_index, \
        self.default_transform_index = struct.unpack_from(self.format, buffer, offset)
        offset += struct.calcsize(self.format)

        return offset

    def write(self, buffer, offset):
        struct.pack_into(self.format, buffer, offset,
                         self.name_index,
                         self.parent_index,
                         self.sub_sequence_count,
                         self.first_sub_sequence_index,
                         self.default_transform_index)
        offset += struct.calcsize(self.format)

        return offset


###############################################################################
# DTS Sequence
###############################################################################
class DTSSequence(DTSBase):
    def __init__(self):
        super().__init__("<iifiiiii")
        self.name_index = 0                   # I32
        self.cyclic = 0                       # I32
        self.duration = 0.0                   # F32
        self.priority = 0                     # I32
        self.first_frame_trigger_index = 0    # I32
        self.frame_trigger_count = 0          # I32
        self.IFL_sub_sequence_count = 0       # I32
        self.first_IFL_sub_sequence_index = 0 # I32

    def pretty(self, level=0, max_level=9999):
        if level > max_level:
            return ""
        return \
f"""DTSSequence(
{"  " * level}  name_index={self.name_index},
{"  " * level}  cyclic={self.cyclic},
{"  " * level}  duration={self.duration},
{"  " * level}  priority={self.priority},
{"  " * level}  first_frame_trigger_index={self.first_frame_trigger_index},
{"  " * level}  frame_trigger_count={self.frame_trigger_count},
{"  " * level}  IFL_sub_sequence_count={self.IFL_sub_sequence_count},
{"  " * level}  first_IFL_sub_sequence_index={self.first_IFL_sub_sequence_index}
{"  " * level})"""

    def read(self, buffer, offset):
        self.name_index, \
        self.cyclic, \
        self.duration, \
        self.priority, \
        self.first_frame_trigger_index, \
        self.frame_trigger_count, \
        self.IFL_sub_sequence_count, \
        self.first_IFL_sub_sequence_index = struct.unpack_from(self.format, buffer, offset)
        offset += struct.calcsize(self.format)

        return offset

    def write(self, buffer, offset):
        struct.pack_into(self.format, buffer, offset,
                         self.name_index,
                         self.cyclic,
                         self.duration,
                         self.priority,
                         self.first_frame_trigger_index,
                         self.frame_trigger_count,
                         self.IFL_sub_sequence_count,
                         self.first_IFL_sub_sequence_index)
        offset += struct.calcsize(self.format)

        return offset


###############################################################################
# DTS Sub Sequence
###############################################################################
class DTSSubSequence(DTSBase):
    def __init__(self):
        super().__init__("<hhh")
        self.sequence_index = 0        # I16
        self.key_frames = 0            # I16 ????
        self.first_key_frame_index = 0 # I16

    def pretty(self, level=0, max_level=9999):
        if level > max_level:
            return ""
        return \
f"""DTSSubSequence(
{"  " * level}  sequence_index={self.sequence_index},
{"  " * level}  key_frames={self.key_frames},
{"  " * level}  first_key_frame_index={self.first_key_frame_index}
{"  " * level})"""

    def read(self, buffer, offset):
        self.sequence_index, \
        self.key_frames, \
        self.first_key_frame_index = struct.unpack_from(self.format, buffer, offset)
        offset += struct.calcsize(self.format)

        return offset

    def write(self, buffer, offset):
        struct.pack_into(self.format, buffer, offset,
                         self.sequence_index,
                         self.key_frames,
                         self.first_key_frame_index)
        offset += struct.calcsize(self.format)

        return offset


###############################################################################
# DTS KeyFrame
###############################################################################
class DTSKeyFrame(DTSBase):
    def __init__(self):
        super().__init__("<fHH")
        self.position = 0.0      # F32
        self.key_value_index = 0 # U16
                                 # Index into shapes transform array for node sub sequences
                                 # Index into meshes frame array for cel sub sequences
        self.material_index = 0  # U16
                                 # Bit 15 : visibility
                                 # Bit 14 : cares about visibility
                                 # Bit 13 : cares about material
                                 # Bit 12 : cares about frame
                                 # Bit 11-0 : material index, not relavent for node sub sequences
    
    def pretty(self, level=0, max_level=9999):
        if level > max_level:
            return ""
        return \
f"""DTSKeyFrame(
{"  " * level}  position={self.position},
{"  " * level}  key_value_index={self.key_value_index},
{"  " * level}  material_index={self.material_index},
{"  " * level}    visibility={(self.material_index & 0x8000) != 0},
{"  " * level}    cares_about_visibility={(self.material_index & 0x4000) != 0},
{"  " * level}    cares_about_material={(self.material_index & 0x2000) != 0},
{"  " * level}    cares_about_frame={(self.material_index & 0x1000) != 0},
{"  " * level}    material_index={self.material_index & 0x0FFF}
{"  " * level})"""

    def read(self, buffer, offset):
        self.position, \
        self.key_value_index, \
        self.material_index = struct.unpack_from(self.format, buffer, offset)
        offset += struct.calcsize(self.format)

        return offset

    def write(self, buffer, offset):
        struct.pack_into(self.format, buffer, offset,
                         self.position,
                         self.key_value_index,
                         self.material_index)
        offset += struct.calcsize(self.format)

        return offset


###############################################################################
# DTS Transform
###############################################################################
class DTSTransform(DTSBase):
    def __init__(self):
        super().__init__("<")
        self.quat = DTSQuat16()       # DTSQuat16
        self.translate = DTSPoint3F() # DTSPoint3F

    def pretty(self, level=0, max_level=9999):
        if level > max_level:
            return ""
        return \
f"""DTSTransform(
{"  " * level}  quat={self.quat.pretty(level + 1, max_level)},
{"  " * level}  translate={self.translate.pretty(level + 1, max_level)}
{"  " * level})"""

    def size(self):
        return self.quat.size() + \
               self.translate.size()

    def read(self, buffer, offset):
        offset = self.quat.read(buffer, offset)
        offset = self.translate.read(buffer, offset)

        return offset    

    def write(self, buffer, offset):
        offset = self.quat.write(buffer, offset)
        offset = self.translate.write(buffer, offset)
        
        return offset


###############################################################################
# DTS Quat 16
###############################################################################
class DTSQuat16(DTSBase):
    def __init__(self):
        super().__init__("<hhhh")
        self.x = 0 # I16
        self.y = 0 # I16
        self.z = 0 # I16
        self.w = 0 # I16

    def pretty(self, level=0, max_level=9999):
        if level > max_level:
            return ""
        return \
f"""DTSQuat16(
{"  " * level}  x={self.x},
{"  " * level}  y={self.y},
{"  " * level}  z={self.z},
{"  " * level}  w={self.w}
{"  " * level})"""

    def read(self, buffer, offset):
        self.x, \
        self.y, \
        self.z, \
        self.w = struct.unpack_from(self.format, buffer, offset)
        offset += struct.calcsize(self.format)

        return offset

    def write(self, buffer, offset):
        struct.pack_into(self.format, buffer, offset,
                         self.x,
                         self.y,
                         self.z,
                         self.w)
        offset += struct.calcsize(self.format)

        return offset


###############################################################################
# DTS Name
###############################################################################
class DTSName(DTSBase):
    def __init__(self):
        super().__init__("<24s")
        self.name = "" # Str 24 characters long with null character

    def decode(self):
        return make_string(self.name)

    def pretty(self, level=0, max_level=9999):
        if level > max_level:
            return ""
        return \
f"""DTSName(
{"  " * level}  name="{make_string(self.name)}"
{"  " * level})"""

    def read(self, buffer, offset):
        self.name, = struct.unpack_from(self.format, buffer, offset)
        offset += struct.calcsize(self.format)

        return offset

    def write(self, buffer, offset):
        struct.pack_into(self.format, buffer, offset,
                         self.name)
        offset += struct.calcsize(self.format)

        return offset    


###############################################################################
# DTS Object
###############################################################################
class DTSObject(DTSBase):
    def __init__(self):
        super().__init__(["<hhihh", "<hh"])
        self.name_index = 0               # I16
        self.flags = 0                    # I16
        self.mesh_index = 0               # I32
        self.node_index = 0               # I16
        self.padding = 0                  # I16
        self.offset = DTSPoint3F()        # DTSPoint3F
        self.sub_sequence_count = 0       # I16
        self.first_sub_sequence_index = 0 # I16

    def pretty(self, level=0, max_level=9999):
        if level > max_level:
            return ""
        return \
f"""DTSObject(
{"  " * level}  name_index={self.name_index},
{"  " * level}  flags={self.flags},
{"  " * level}  mesh_index={self.mesh_index},
{"  " * level}  node_index={self.node_index},
{"  " * level}  padding={self.padding},
{"  " * level}  offset={self.offset.pretty(level + 1, max_level)},
{"  " * level}  sub_sequence_count={self.sub_sequence_count},
{"  " * level}  first_sub_sequence_index={self.first_sub_sequence_index}
{"  " * level})"""

    def size(self):
        return struct.calcsize(self.format[0]) + \
               self.offset.size() + \
               struct.calcsize(self.format[1])

    def read(self, buffer, offset):
        self.name_index, \
        self.flags, \
        self.mesh_index, \
        self.node_index, \
        self.padding = struct.unpack_from(self.format[0], buffer, offset)
        offset += struct.calcsize(self.format[0])

        offset = self.offset.read(buffer, offset)
        
        self.sub_sequence_count, \
        self.first_sub_sequence_index = struct.unpack_from(self.format[1], buffer, offset)
        offset += struct.calcsize(self.format[1])
        
        return offset

    def write(self, buffer, offset):
        struct.pack_into(self.format[0], buffer, offset,
                         self.name_index,
                         self.flags,
                         self.mesh_index,
                         self.node_index,
                         self.padding)
        offset += struct.calcsize(self.format[0])
        
        offset = self.offset.write(buffer, offset)
        
        struct.pack_into(self.format[1], buffer, offset,
                         self.sub_sequence_count,
                         self.first_sub_sequence_index)
        offset += struct.calcsize(self.format[1])
        
        return offset


###############################################################################
# DTS Detail
###############################################################################
class DTSDetail(DTSBase):
    def __init__(self):
        super().__init__("<if")
        self.root_node_index = 0 # I32
        self.min_size = 0.0      # F32

    def pretty(self, level=0, max_level=9999):
        if level > max_level:
            return ""
        return \
f"""DTSDetail(
{"  " * level}  root_node_index={self.root_node_index},
{"  " * level}  min_size={self.min_size}
{"  " * level})"""

    def read(self, buffer, offset):
        self.root_node_index, \
        self.min_size = struct.unpack_from(self.format, buffer, offset)
        offset += struct.calcsize(self.format)

        return offset

    def write(self, buffer, offset):
        struct.pack_into(self.format, buffer, offset,
                         self.root_node_index,
                         self.min_size)
        offset += struct.calcsize(self.format)

        return offset


###############################################################################
# DTS Transition
###############################################################################
class DTSTransition(DTSBase):
    def __init__(self):
        super().__init__("<iifff")
        self.start_sequence_index = 0   # I32
        self.end_sequence_index = 0     # I32
        self.start_position = 0.0       # F32
        self.end_position = 0.0         # F32
        self.duration = 0.0             # F32
        self.transform = DTSTransform() # DTSTransform

    def pretty(self, level=0, max_level=9999):
        if level > max_level:
            return ""
        return \
f"""DTSTransition(
{"  " * level}  start_sequence_index={self.start_sequence_index},
{"  " * level}  end_sequence_index={self.end_sequence_index},
{"  " * level}  start_position={self.start_position},
{"  " * level}  end_position={self.end_position},
{"  " * level}  duration={self.duration},
{"  " * level}  transform={self.transform.pretty(level + 1, max_level)}
{"  " * level})"""

    def size(self):
        return struct.calcsize(self.format) + \
               self.transform.size()

    def read(self, buffer, offset):
        self.start_sequence_index, \
        self.end_sequence_index, \
        self.start_position, \
        self.end_position, \
        self.duration = struct.unpack_from(self.format, buffer, offset)
        offset += struct.calcsize(self.format)

        offset = self.transform.read(buffer, offset)
        
        return offset

    def write(self, buffer, offset):
        struct.pack_into(self.format, buffer, offset,
                         self.start_sequence_index,
                         self.end_sequence_index,
                         self.start_position,
                         self.end_position,
                         self.duration)
        offset += struct.calcsize(self.format)

        offset = self.transform.write(buffer, offset)
        
        return offset


###############################################################################
# DTS Frame Trigger
###############################################################################
class DTSFrameTrigger(DTSBase):
    def __init__(self):
        super().__init__("<fi")
        self.position = 0.0 # F32
        self.value = 0      # I32

    def pretty(self, level=0, max_level=9999):
        if level > max_level:
            return ""
        return \
f"""DTSFrameTrigger(
{"  " * level}  position={self.position},
{"  " * level}  value={self.value}
{"  " * level})"""

    def read(self, buffer, offset):
        self.position, \
        self.value = struct.unpack_from(self.format, buffer, offset)
        offset += struct.calcsize(self.format)

        return offset

    def write(self, buffer, offset):
        struct.pack_into(self.format, buffer, offset,
                         self.position,
                         self.value)
        offset += struct.calcsize(self.format)

        return offset


###############################################################################
# DTS TS::CelAnimMesh
###############################################################################
class DTSTSCelAnimMesh(DTSBase):
    def __init__(self):
        super().__init__("<iiiiiif")
        self.vertex_count = 0                   # I32
        self.vertex_per_frame_count = 0         # I32
        self.texture_vertex_count = 0           # I32
        self.face_count = 0                     # I32
        self.frame_count = 0                    # I32
        self.texture_vertex_per_frame_count = 0 # I32 ????
        self.radius = 0.0                       # F32
        self.vertex_list = []                   # list[DTSVertex]
        self.texture_vertex_list = []           # list[DTSTextureVertex]
        self.face_list = []                     # list[DTSFace]
        self.frame_list = []                    # list[DTSFrame]

    def pretty(self, level=0, max_level=9999):
        if level > max_level:
            return ""
        return \
f"""DTSTSCelAnimMesh(
{"  " * level}  vertex_count={self.vertex_count},
{"  " * level}  vertex_per_frame_count={self.vertex_per_frame_count},
{"  " * level}  texture_vertex_count={self.texture_vertex_count},
{"  " * level}  face_count={self.face_count},
{"  " * level}  frame_count={self.frame_count},
{"  " * level}  texture_vertex_per_frame_count={self.texture_vertex_per_frame_count},
{"  " * level}  radius={self.radius},
{"  " * level}  vertex_list=[{','.join([x.pretty(level + 2, max_level, self.frame_list[-1].scale, self.frame_list[-1].origin) for x in self.vertex_list])}
{"  " * level}  ],
{"  " * level}  texture_vertex_list=[{','.join([x.pretty(level + 2, max_level) for x in self.texture_vertex_list])}
{"  " * level}  ],
{"  " * level}  face_list=[{','.join([x.pretty(level + 2, max_level) for x in self.face_list])}
{"  " * level}  ],
{"  " * level}  frame_list=[{','.join([x.pretty(level + 2, max_level) for x in self.frame_list])}
{"  " * level}  ]
{"  " * level})"""

    def size(self):
        return struct.calcsize(self.format) + \
               sum([x.size() for x in self.vertex_list]) + \
               sum([x.size() for x in self.texture_vertex_list]) + \
               sum([x.size() for x in self.face_list]) + \
               sum([x.size() for x in self.frame_list])

    def read(self, buffer, offset):
        self.vertex_count, \
        self.vertex_per_frame_count, \
        self.texture_vertex_count, \
        self.face_count, \
        self.frame_count, \
        self.texture_vertex_per_frame_count, \
        self.radius = struct.unpack_from(self.format, buffer, offset)
        offset += struct.calcsize(self.format)

        self.vertex_list, offset = read_many(DTSVertex, self.vertex_count, buffer, offset)
        self.texture_vertex_list, offset = read_many(DTSTextureVertex, self.texture_vertex_count, buffer, offset)
        self.face_list, offset = read_many(DTSFace, self.face_count, buffer, offset)
        self.frame_list, offset = read_many(DTSFrame, self.frame_count, buffer, offset)
        
        return offset

    def write(self, buffer, offset):
        struct.pack_into(self.format, buffer, offset,
                         self.vertex_count,
                         self.vertex_per_frame_count,
                         self.texture_vertex_count,
                         self.face_count,
                         self.frame_count,
                         self.texture_vertex_per_frame_count,
                         self.radius)
        offset += struct.calcsize(self.format)
        
        offset = write_many(self.vertex_list, buffer, offset)
        offset = write_many(self.texture_vertex_list, buffer, offset)
        offset = write_many(self.face_list, buffer, offset)
        offset = write_many(self.frame_list, buffer, offset)
        
        return offset


###############################################################################
# DTS Vertex
###############################################################################
class DTSVertex(DTSBase):
    def __init__(self):
        super().__init__("<BBBB")
        self.x = 0      # U8
        self.y = 0      # U8
        self.z = 0      # U8
        self.normal = 0 # U8

    def decode(self, scale, origin):
        return DTSPoint3F(self.x * scale.x + origin.x,
                          self.y * scale.y + origin.y,
                          self.z * scale.z + origin.z), \
               NORMAL_TABLE[self.normal]
    
    def pretty(self, level=0, max_level=9999, scale=None, origin=None):
        if level > max_level:
            return ""
        normal = NORMAL_TABLE[self.normal]
        if scale is None and origin is None:
            return \
f"""DTSVertex(
{"  " * level}  x={self.x},
{"  " * level}  y={self.y},
{"  " * level}  z={self.z},
{"  " * level}  normal={self.normal} -> ({normal.x}, {normal.y}, {normal.z})
{"  " * level})"""
        else:
            return \
f"""DTSVertex(
{"  " * level}  x={self.x} -> {self.x * scale.x + origin.x},
{"  " * level}  y={self.y} -> {self.y * scale.y + origin.y},
{"  " * level}  z={self.z} -> {self.z * scale.z + origin.z},
{"  " * level}  normal={self.normal} -> ({normal.x}, {normal.y}, {normal.z})
{"  " * level})"""

    def read(self, buffer, offset):
        self.x, \
        self.y, \
        self.z, \
        self.normal = struct.unpack_from(self.format, buffer, offset)
        offset += struct.calcsize(self.format)

        return offset

    def write(self, buffer, offset):
        struct.pack_into(self.format, buffer, offset,
                         self.x,
                         self.y,
                         self.z,
                         self.normal)
        offset += struct.calcsize(self.format)

        return offset


###############################################################################
# DTS Texture Vertex
###############################################################################
class DTSTextureVertex(DTSBase):
    def __init__(self):
        super().__init__("<ff")
        self.x = 0.0 # F32
        self.y = 0.0 # F32

    def pretty(self, level=0, max_level=9999):
        if level > max_level:
            return ""
        return \
f"""DTSTextureVertex(
{"  " * level}  x={self.x},
{"  " * level}  y={self.y}
{"  " * level})"""

    def read(self, buffer, offset):
        self.x, \
        self.y = struct.unpack_from(self.format, buffer, offset)
        offset += struct.calcsize(self.format)

        return offset

    def write(self, buffer, offset):
        struct.pack_into(self.format, buffer, offset,
                         self.x,
                         self.y)
        offset += struct.calcsize(self.format)
        
        return offset


###############################################################################
# DTS Face
###############################################################################
class DTSFace(DTSBase):
    def __init__(self):
        super().__init__("<iiiiiii")
        self.vertex_index_list = [0, 0, 0]  # list[I32] 3
        self.texture_index_list = [0, 0, 0] # list[I32] 3
        self.material = 0                   # I32

    def pretty(self, level=0, max_level=9999):
        if level > max_level:
            return ""
        return \
f"""DTSFace(
{"  " * level}  vertex_index_list={self.vertex_index_list},
{"  " * level}  texture_index_list={self.texture_index_list},
{"  " * level}  material={self.material}
{"  " * level})"""

    def read(self, buffer, offset):
        self.vertex_index_list[0], \
        self.texture_index_list[0], \
        self.vertex_index_list[1], \
        self.texture_index_list[1], \
        self.vertex_index_list[2], \
        self.texture_index_list[2], \
        self.material = struct.unpack_from(self.format, buffer, offset)
        offset += struct.calcsize(self.format)

        return offset
    
    def write(self, buffer, offset):
        struct.pack_into(self.format, buffer, offset,
                         self.vertex_index_list[0],
                         self.texture_index_list[0],
                         self.vertex_index_list[1],
                         self.texture_index_list[1],
                         self.vertex_index_list[2],
                         self.texture_index_list[2],
                         self.material)
        offset += struct.calcsize(self.format)
        
        return offset


###############################################################################
# DTS Frame
###############################################################################
class DTSFrame(DTSBase):
    def __init__(self):
        super().__init__("<i")
        self.first_vertex_index = 0 # I32
        self.scale = DTSPoint3F()   # DTSPoint3F
        self.origin = DTSPoint3F()  # DTSPoint3F

    def pretty(self, level=0, max_level=9999):
        if level > max_level:
            return ""
        return \
f"""DTSFrame(
{"  " * level}  first_vertex_index={self.first_vertex_index},
{"  " * level}  scale={self.scale.pretty(level + 2, max_level)},
{"  " * level}  origin={self.origin.pretty(level + 2, max_level)}
{"  " * level})"""

    def size(self):
        return struct.calcsize(self.format) + \
               self.scale.size() + \
               self.origin.size()

    def read(self, buffer, offset):
        self.first_vertex_index, = struct.unpack_from(self.format, buffer, offset)
        offset += struct.calcsize(self.format)

        offset = self.scale.read(buffer, offset)
        offset = self.origin.read(buffer, offset)
        
        return offset

    def write(self, buffer, offset):
        struct.pack_into(self.format, buffer, offset,
                         self.first_vertex_index)
        offset += struct.calcsize(self.format)
        
        offset = self.scale.write(buffer, offset)
        offset = self.origin.write(buffer, offset)
        
        return offset


###############################################################################
# DTS TS::MaterialList
###############################################################################
class DTSTSMaterialList(DTSBase):
    def __init__(self):
        super().__init__("<ii")
        self.detail_count = 0    # I32
        self.material_count = 0       # I32
        self.materials_list = [] # list[DTSMaterial]

    def pretty(self, level=0, max_level=9999):
        if level > max_level:
            return ""
        return \
f"""DTSTSMaterialList(
{"  " * level}  detail_count={self.detail_count},
{"  " * level}  material_count={self.material_count},
{"  " * level}  materials_list=[{','.join([x.pretty(level + 2, max_level) for x in self.materials_list])}
{"  " * level}  ]
{"  " * level})"""

    def size(self):
        return struct.calcsize(self.format) + \
               sum([x.size() for x in self.materials_list])

    def read(self, buffer, offset):
        self.detail_count, \
        self.material_count = struct.unpack_from(self.format, buffer, offset)
        offset += struct.calcsize(self.format)
        
        self.materials_list, offset = read_many(DTSMaterial, self.detail_count * self.material_count, buffer, offset)
        
        return offset

    def write(self, buffer, offset):
        struct.pack_into(self.format, buffer, offset,
                         self.detail_count,
                         self.material_count)
        offset += struct.calcsize(self.format)
        
        offset = write_many(self.materials_list, buffer, offset)
        
        return offset


###############################################################################
# DTS Material
###############################################################################
class DTSMaterial(DTSBase):
    def __init__(self):
        super().__init__("<ifiBBBB32siffI")
        self.flags = 0             # I32
        self.alpha = 0.0           # F32
        self.index = 0             # I32
        self.color_r = 0           # U8
        self.color_g = 0           # U8
        self.color_b = 0           # U8
        self.color_flags = 0       # U8
        self.map_file = ""         # Str len 31 + 1 NULL
        self.type = 0              # I32
        self.elasticity = 0.0      # F32
        self.friction = 0.0        # F32
        self.use_default_props = 0 # U32

    def decode(self):
        return make_string(self.map_file)

    def pretty(self, level=0, max_level=9999):
        if level > max_level:
            return ""
        return \
f"""DTSMaterial(
{"  " * level}  flags={self.flags},
{"  " * level}  alpha={self.alpha},
{"  " * level}  index={self.index},
{"  " * level}  color_r={self.color_r},
{"  " * level}  color_g={self.color_g},
{"  " * level}  color_b={self.color_b},
{"  " * level}  color_flags={self.color_flags},
{"  " * level}  map_file={self.map_file},
{"  " * level}  type={self.type},
{"  " * level}  elasticity={self.elasticity},
{"  " * level}  friction={self.friction},
{"  " * level}  use_default_props={self.use_default_props}
{"  " * level})"""

    def read(self, buffer, offset):
        self.flags, \
        self.alpha, \
        self.index, \
        self.color_r, \
        self.color_g, \
        self.color_b, \
        self.color_flags, \
        self.map_file, \
        self.type, \
        self.elasticity, \
        self.friction, \
        self.use_default_props = struct.unpack_from(self.format, buffer, offset)
        offset += struct.calcsize(self.format)

        return offset

    def write(self, buffer, offset):
        struct.pack_into(self.format, buffer, offset,
                         self.flags,
                         self.alpha,
                         self.index,
                         self.color_r,
                         self.color_g,
                         self.color_b,
                         self.color_flags,
                         self.map_file,
                         self.type,
                         self.elasticity,
                         self.friction,
                         self.use_default_props)
        offset += struct.calcsize(self.format)
        
        return offset


###############################################################################
# Helpers
###############################################################################
def read_many(thing, count, buffer, offset):
    things = []
    for i in range(count):
        t = thing()
        offset = t.read(buffer, offset)
        things.append(t)
    return things, offset

def write_many(things, buffer, offset):
    for thing in things:
        offset = thing.write(buffer, offset)
    return offset

def make_string(buffer):
    for i, b in enumerate(buffer):
        if b == 0:
            return buffer[0:i].decode('ascii')
    return buffer.decode('ascii')

NORMAL_TABLE = [
    DTSPoint3F(0.565061, -0.270644, -0.779396),
    DTSPoint3F(-0.309804, -0.731114, 0.607860),
    DTSPoint3F(-0.867412, 0.472957, 0.154619),
    DTSPoint3F(-0.757488, 0.498188, -0.421925),
    DTSPoint3F(0.306834, -0.915340, 0.260778),
    DTSPoint3F(0.098754, 0.639153, -0.762713),
    DTSPoint3F(0.713706, -0.558862, -0.422252),
    DTSPoint3F(-0.890431, -0.407603, -0.202466),
    DTSPoint3F(0.848050, -0.487612, -0.207475),
    DTSPoint3F(-0.232226, 0.776855, 0.585293),
    DTSPoint3F(-0.940195, 0.304490, -0.152706),
    DTSPoint3F(0.602019, -0.491878, -0.628991),
    DTSPoint3F(-0.096835, -0.494354, -0.863850),
    DTSPoint3F(0.026630, -0.323659, -0.945799),
    DTSPoint3F(0.019208, 0.909386, 0.415510),
    DTSPoint3F(0.854440, 0.491730, 0.167731),
    DTSPoint3F(-0.418835, 0.866521, -0.271512),
    DTSPoint3F(0.465024, 0.409667, 0.784809),
    DTSPoint3F(-0.674391, -0.691087, -0.259992),
    DTSPoint3F(0.303858, -0.869270, -0.389922),
    DTSPoint3F(0.991333, 0.090061, -0.095640),
    DTSPoint3F(-0.275924, -0.369550, 0.887298),
    DTSPoint3F(0.426545, -0.465962, 0.775202),
    DTSPoint3F(-0.482741, -0.873278, -0.065920),
    DTSPoint3F(0.063616, 0.932012, -0.356800),
    DTSPoint3F(0.624786, -0.061315, 0.778385),
    DTSPoint3F(-0.530300, 0.416850, 0.738253),
    DTSPoint3F(0.312144, -0.757028, -0.573999),
    DTSPoint3F(0.399288, -0.587091, -0.704197),
    DTSPoint3F(-0.132698, 0.482877, 0.865576),
    DTSPoint3F(0.950966, 0.306530, 0.041268),
    DTSPoint3F(-0.015923, -0.144300, 0.989406),
    DTSPoint3F(-0.407522, -0.854193, 0.322925),
    DTSPoint3F(-0.932398, 0.220464, 0.286408),
    DTSPoint3F(0.477509, 0.876580, 0.059936),
    DTSPoint3F(0.337133, 0.932606, -0.128796),
    DTSPoint3F(-0.638117, 0.199338, 0.743687),
    DTSPoint3F(-0.677454, 0.445349, 0.585423),
    DTSPoint3F(-0.446715, 0.889059, -0.100099),
    DTSPoint3F(-0.410024, 0.909168, 0.072759),
    DTSPoint3F(0.708462, 0.702103, -0.071641),
    DTSPoint3F(-0.048801, -0.903683, -0.425411),
    DTSPoint3F(-0.513681, -0.646901, 0.563606),
    DTSPoint3F(-0.080022, 0.000676, -0.996793),
    DTSPoint3F(0.066966, -0.991150, -0.114615),
    DTSPoint3F(-0.245220, 0.639318, -0.728793),
    DTSPoint3F(0.250978, 0.855979, 0.452006),
    DTSPoint3F(-0.123547, 0.982443, -0.139791),
    DTSPoint3F(-0.794825, 0.030254, -0.606084),
    DTSPoint3F(-0.772905, 0.547941, 0.319967),
    DTSPoint3F(0.916347, 0.369614, -0.153928),
    DTSPoint3F(-0.388203, 0.105395, 0.915527),
    DTSPoint3F(-0.700468, -0.709334, 0.078677),
    DTSPoint3F(-0.816193, 0.390455, 0.425880),
    DTSPoint3F(-0.043007, 0.769222, -0.637533),
    DTSPoint3F(0.911444, 0.113150, 0.395560),
    DTSPoint3F(0.845801, 0.156091, -0.510153),
    DTSPoint3F(0.829801, -0.029340, 0.557287),
    DTSPoint3F(0.259529, 0.416263, 0.871418),
    DTSPoint3F(0.231128, -0.845982, 0.480515),
    DTSPoint3F(-0.626203, -0.646168, 0.436277),
    DTSPoint3F(-0.197047, -0.065791, 0.978184),
    DTSPoint3F(-0.255692, -0.637488, -0.726794),
    DTSPoint3F(0.530662, -0.844385, -0.073567),
    DTSPoint3F(-0.779887, 0.617067, -0.104899),
    DTSPoint3F(0.739908, 0.113984, 0.662982),
    DTSPoint3F(-0.218801, 0.930194, -0.294729),
    DTSPoint3F(-0.374231, 0.818666, 0.435589),
    DTSPoint3F(-0.720250, -0.028285, 0.693137),
    DTSPoint3F(0.075389, 0.415049, 0.906670),
    DTSPoint3F(-0.539724, -0.106620, 0.835063),
    DTSPoint3F(-0.452612, -0.754669, -0.474991),
    DTSPoint3F(0.682822, 0.581234, -0.442629),
    DTSPoint3F(0.002435, -0.618462, -0.785811),
    DTSPoint3F(-0.397631, 0.110766, -0.910835),
    DTSPoint3F(0.133935, -0.985438, 0.104754),
    DTSPoint3F(0.759098, -0.608004, 0.232595),
    DTSPoint3F(-0.825239, -0.256087, 0.503388),
    DTSPoint3F(0.101693, -0.565568, 0.818408),
    DTSPoint3F(0.386377, 0.793546, -0.470104),
    DTSPoint3F(-0.520516, -0.840690, 0.149346),
    DTSPoint3F(-0.784549, -0.479672, 0.392935),
    DTSPoint3F(-0.325322, -0.927581, -0.183735),
    DTSPoint3F(-0.069294, -0.428541, 0.900861),
    DTSPoint3F(0.993354, -0.115023, -0.004288),
    DTSPoint3F(-0.123896, -0.700568, 0.702747),
    DTSPoint3F(-0.438031, -0.120880, -0.890795),
    DTSPoint3F(0.063314, 0.813233, 0.578484),
    DTSPoint3F(0.322045, 0.889086, -0.325289),
    DTSPoint3F(-0.133521, 0.875063, -0.465228),
    DTSPoint3F(0.637155, 0.564814, 0.524422),
    DTSPoint3F(0.260092, -0.669353, 0.695930),
    DTSPoint3F(0.953195, 0.040485, -0.299634),
    DTSPoint3F(-0.840665, -0.076509, 0.536124),
    DTSPoint3F(-0.971350, 0.202093, 0.125047),
    DTSPoint3F(-0.804307, -0.396312, -0.442749),
    DTSPoint3F(-0.936746, 0.069572, 0.343027),
    DTSPoint3F(0.426545, -0.465962, 0.775202),
    DTSPoint3F(0.794542, -0.227450, 0.563000),
    DTSPoint3F(-0.892172, 0.091169, -0.442399),
    DTSPoint3F(-0.312654, 0.541264, 0.780564),
    DTSPoint3F(0.590603, -0.735618, -0.331743),
    DTSPoint3F(-0.098040, -0.986713, 0.129558),
    DTSPoint3F(0.569646, 0.283078, -0.771603),
    DTSPoint3F(0.431051, -0.407385, -0.805129),
    DTSPoint3F(-0.162087, -0.938749, -0.304104),
    DTSPoint3F(0.241533, -0.359509, 0.901341),
    DTSPoint3F(-0.576191, 0.614939, 0.538380),
    DTSPoint3F(-0.025110, 0.085740, 0.996001),
    DTSPoint3F(-0.352693, -0.198168, 0.914515),
    DTSPoint3F(-0.604577, 0.700711, 0.378802),
    DTSPoint3F(0.465024, 0.409667, 0.784809),
    DTSPoint3F(-0.254684, -0.030474, -0.966544),
    DTSPoint3F(-0.604789, 0.791809, 0.085259),
    DTSPoint3F(-0.705147, -0.399298, 0.585943),
    DTSPoint3F(0.185691, 0.017236, -0.982457),
    DTSPoint3F(0.044588, 0.973094, 0.226052),
    DTSPoint3F(-0.405463, 0.642367, 0.650357),
    DTSPoint3F(-0.563959, 0.599136, -0.568319),
    DTSPoint3F(0.367162, -0.072253, -0.927347),
    DTSPoint3F(0.960429, -0.213570, -0.178783),
    DTSPoint3F(-0.192629, 0.906005, 0.376893),
    DTSPoint3F(-0.199718, -0.359865, -0.911378),
    DTSPoint3F(0.485072, 0.121233, -0.866030),
    DTSPoint3F(0.467163, -0.874294, 0.131792),
    DTSPoint3F(-0.638953, -0.716603, 0.279677),
    DTSPoint3F(-0.622710, 0.047813, -0.780990),
    DTSPoint3F(0.828724, -0.054433, -0.557004),
    DTSPoint3F(0.130241, 0.991080, 0.028245),
    DTSPoint3F(0.310995, -0.950076, -0.025242),
    DTSPoint3F(0.818118, 0.275336, 0.504850),
    DTSPoint3F(0.676328, 0.387023, 0.626733),
    DTSPoint3F(-0.100433, 0.495114, -0.863004),
    DTSPoint3F(-0.949609, -0.240681, -0.200786),
    DTSPoint3F(-0.102610, 0.261831, -0.959644),
    DTSPoint3F(-0.845732, -0.493136, 0.203850),
    DTSPoint3F(0.672617, -0.738838, 0.041290),
    DTSPoint3F(0.380465, 0.875938, 0.296613),
    DTSPoint3F(-0.811223, 0.262027, -0.522742),
    DTSPoint3F(-0.074423, -0.775670, -0.626736),
    DTSPoint3F(-0.286499, 0.755850, -0.588735),
    DTSPoint3F(0.291182, -0.276189, -0.915933),
    DTSPoint3F(-0.638117, 0.199338, 0.743687),
    DTSPoint3F(0.439922, -0.864433, -0.243359),
    DTSPoint3F(0.177649, 0.206919, 0.962094),
    DTSPoint3F(0.277107, 0.948521, 0.153361),
    DTSPoint3F(0.507629, 0.661918, -0.551523),
    DTSPoint3F(-0.503110, -0.579308, -0.641313),
    DTSPoint3F(0.600522, 0.736495, -0.311364),
    DTSPoint3F(-0.691096, -0.715301, -0.103592),
    DTSPoint3F(-0.041083, -0.858497, 0.511171),
    DTSPoint3F(0.207773, -0.480062, -0.852274),
    DTSPoint3F(0.795719, 0.464614, 0.388543),
    DTSPoint3F(-0.100433, 0.495114, -0.863004),
    DTSPoint3F(0.703249, 0.065157, -0.707951),
    DTSPoint3F(-0.324171, -0.941112, 0.096024),
    DTSPoint3F(-0.134933, -0.940212, 0.312722),
    DTSPoint3F(-0.438240, 0.752088, -0.492249),
    DTSPoint3F(0.964762, -0.198855, 0.172311),
    DTSPoint3F(-0.831799, 0.196807, 0.519015),
    DTSPoint3F(-0.508008, 0.819902, 0.263986),
    DTSPoint3F(0.471075, -0.001146, 0.882092),
    DTSPoint3F(0.919512, 0.246162, -0.306435),
    DTSPoint3F(-0.960050, 0.279828, -0.001187),
    DTSPoint3F(0.110232, -0.847535, -0.519165),
    DTSPoint3F(0.208229, 0.697360, 0.685806),
    DTSPoint3F(-0.199680, -0.560621, 0.803637),
    DTSPoint3F(0.170135, -0.679985, -0.713214),
    DTSPoint3F(0.758371, -0.494907, 0.424195),
    DTSPoint3F(0.077734, -0.755978, 0.649965),
    DTSPoint3F(0.612831, -0.672475, 0.414987),
    DTSPoint3F(0.142776, 0.836698, -0.528726),
    DTSPoint3F(-0.765185, 0.635778, 0.101382),
    DTSPoint3F(0.669873, -0.419737, 0.612447),
    DTSPoint3F(0.593549, 0.194879, 0.780847),
    DTSPoint3F(0.646930, 0.752173, 0.125368),
    DTSPoint3F(0.837721, 0.545266, -0.030127),
    DTSPoint3F(0.541505, 0.768070, 0.341820),
    DTSPoint3F(0.760679, -0.365715, -0.536301),
    DTSPoint3F(0.381516, 0.640377, 0.666605),
    DTSPoint3F(0.565794, -0.072415, -0.821361),
    DTSPoint3F(-0.466072, -0.401588, 0.788356),
    DTSPoint3F(0.987146, 0.096290, 0.127560),
    DTSPoint3F(0.509709, -0.688886, -0.515396),
    DTSPoint3F(-0.135132, -0.988046, -0.074192),
    DTSPoint3F(0.600499, 0.476471, -0.642166),
    DTSPoint3F(-0.732326, -0.275320, -0.622815),
    DTSPoint3F(-0.881141, -0.470404, 0.048078),
    DTSPoint3F(0.051548, 0.601042, 0.797553),
    DTSPoint3F(0.402027, -0.763183, 0.505891),
    DTSPoint3F(0.404233, -0.208288, 0.890624),
    DTSPoint3F(-0.311793, 0.343843, 0.885752),
    DTSPoint3F(0.098132, -0.937014, 0.335223),
    DTSPoint3F(0.537158, 0.830585, -0.146936),
    DTSPoint3F(0.725277, 0.298172, -0.620538),
    DTSPoint3F(-0.882025, 0.342976, -0.323110),
    DTSPoint3F(-0.668829, 0.424296, -0.610443),
    DTSPoint3F(-0.408835, -0.476442, -0.778368),
    DTSPoint3F(0.809472, 0.397249, -0.432375),
    DTSPoint3F(-0.909184, -0.205938, -0.361903),
    DTSPoint3F(0.866930, -0.347934, -0.356895),
    DTSPoint3F(0.911660, -0.141281, -0.385897),
    DTSPoint3F(-0.431404, -0.844074, -0.318480),
    DTSPoint3F(-0.950593, -0.073496, 0.301614),
    DTSPoint3F(-0.719716, 0.626915, -0.298305),
    DTSPoint3F(-0.779887, 0.617067, -0.104899),
    DTSPoint3F(-0.475899, -0.542630, 0.692151),
    DTSPoint3F(0.081952, -0.157248, -0.984153),
    DTSPoint3F(0.923990, -0.381662, -0.024025),
    DTSPoint3F(-0.957998, 0.120979, -0.260008),
    DTSPoint3F(0.306601, 0.227975, -0.924134),
    DTSPoint3F(-0.141244, 0.989182, 0.039601),
    DTSPoint3F(0.077097, 0.186288, -0.979466),
    DTSPoint3F(-0.630407, -0.259801, 0.731499),
    DTSPoint3F(0.718150, 0.637408, 0.279233),
    DTSPoint3F(0.340946, 0.110494, 0.933567),
    DTSPoint3F(-0.396671, 0.503020, -0.767869),
    DTSPoint3F(0.636943, -0.245005, 0.730942),
    DTSPoint3F(-0.849605, -0.518660, -0.095724),
    DTSPoint3F(-0.388203, 0.105395, 0.915527),
    DTSPoint3F(-0.280671, -0.776541, -0.564099),
    DTSPoint3F(-0.601680, 0.215451, -0.769131),
    DTSPoint3F(-0.660112, -0.632371, -0.405412),
    DTSPoint3F(0.921096, 0.284072, 0.266242),
    DTSPoint3F(0.074850, -0.300846, 0.950731),
    DTSPoint3F(0.943952, -0.067062, 0.323198),
    DTSPoint3F(-0.917838, -0.254589, 0.304561),
    DTSPoint3F(0.889843, -0.409008, 0.202219),
    DTSPoint3F(-0.565849, 0.753721, -0.334246),
    DTSPoint3F(0.791460, 0.555918, -0.254060),
    DTSPoint3F(0.261936, 0.703590, -0.660568),
    DTSPoint3F(-0.234406, 0.952084, 0.196444),
    DTSPoint3F(0.111205, 0.979492, -0.168014),
    DTSPoint3F(-0.869844, -0.109095, -0.481113),
    DTSPoint3F(-0.337728, -0.269701, -0.901777),
    DTSPoint3F(0.366793, 0.408875, -0.835634),
    DTSPoint3F(-0.098749, 0.261316, 0.960189),
    DTSPoint3F(-0.272379, -0.847100, 0.456324),
    DTSPoint3F(-0.319506, 0.287444, -0.902935),
    DTSPoint3F(0.873383, -0.294109, 0.388203),
    DTSPoint3F(-0.088950, 0.710450, 0.698104),
    DTSPoint3F(0.551238, -0.786552, 0.278340),
    DTSPoint3F(0.724436, -0.663575, -0.186712),
    DTSPoint3F(0.529741, -0.606539, 0.592861),
    DTSPoint3F(-0.949743, -0.282514, 0.134809),
    DTSPoint3F(0.155047, 0.419442, -0.894443),
    DTSPoint3F(-0.562653, -0.329139, -0.758346),
    DTSPoint3F(0.816407, -0.576953, 0.024576),
    DTSPoint3F(0.178550, -0.950242, -0.255266),
    DTSPoint3F(0.479571, 0.706691, 0.520192),
    DTSPoint3F(0.391687, 0.559884, -0.730145),
    DTSPoint3F(0.724872, -0.205570, -0.657496),
    DTSPoint3F(-0.663196, -0.517587, -0.540624),
    DTSPoint3F(-0.660054, -0.122486, -0.741165),
    DTSPoint3F(-0.531989, 0.374711, -0.759328),
    DTSPoint3F(0.194979, -0.059120, 0.979024)
]


if __name__ == "__main__":
    input_data = None
    with open("egg.DTS", "rb") as f:
    # with open("casinoHat_01.DTS", "rb") as f:
    # with open("rpgmalehuman.dts", "rb") as f:
        input_data = f.read()
    shape = DTSHeader()
    shape.read(input_data, 0)
    print(shape.pretty(max_level=5))
    print(f"File Size {len(input_data)}. Shape Size {shape.size()}.")
    # with open("egg_copy.dts", "wb") as f:
    # with open("casinoHat_01_copy.dts", "wb") as f:
    # with open("rpgmalehuman_copy.dts", "wb") as f:
    #     buffer = bytearray(shape.size())
    #     shape.write(buffer, 0)
    #     f.write(buffer)

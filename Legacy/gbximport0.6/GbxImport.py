import bpy
import struct
import mathutils


bl_info = \
    {
        "name" : ".gbxmodel Importer",
        "author" : "Fulsam <mrfulsy@gmail.com>, based heavily on a MaxScript by TheGhost <papamarcos@gmail.com>",
        "version" : (0, 6, 0),
        "blender" : (2, 5, 7),
        "location" : "View 3D > Object Mode > Tool Shelf",
        "description" :
            "Import a .gbxmodel",
        "warning" : "",
        "wiki_url" : "",
        "tracker_url" : "",
        "category" : "Import-Export",
    }

testBool = False

modelLoaded = False
marker_blocks = 0
marker_name = []
marker_instance_blocks = []
marker_instance_region_index = []
marker_instance_permutation_index = []
marker_instance_node_index = []
marker_instance_translation = []
marker_instance_rotation = []

node_blocks = 0
node_name = []
node_next_sibling_node_index = []
node_first_child_node_index = []
node_parent_node_index = []
node_translation = []
node_rotation = []
node_distance_from_parent = []

region_blocks = 0
region_name = []
region_permutation_blocks = []
region_permutation_name = []
region_permutation_LOD_indices = []
region_permutation_marker_blocks = []
region_permutation_marker_name = []
region_permutation_marker_node_index =[]
region_permutation_marker_rotation = []
region_permutation_marker_translation = []


geometry_blocks = 0
geometry_part_blocks = []
geometry_part_shader_index = []
geometry_part_data_offset = []
geometry_part_uncompressed_vertex_blocks = []
geometry_part_compressed_vertex_blocks = []
geometry_part_triangle_blocks = []
geometry_part_local_nodes = []

shader_blocks = 0
shader_name = []

node_array = []
marker_array = []

node_list_checksum = 0
local_nodes = False
u_scale = 1.0
v_scale = 1.0
modelPath = ""
ceRoot = "TESTSTRING"           #Maybe these might work later
#tagLoc = ""           



def readShortB(strType):                        #Read a short byte in in Big Endianness. MUST BE BIG ENDIANNESS!
    
    if strType == "signedType":
        (b1,) = struct.unpack('>h', F.read(2))
    elif strType == "unsignedType":
            (b1,) = struct.unpack('>H', F.read(2))
    return b1

def readLongB(strType):                         #Ditto, but for long bytes.
    
    if strType == "signedType":
        (b1,) = struct.unpack('>l', F.read(4))
    elif strType == "unsignedType":
            (b1,) = struct.unpack('>L', F.read(4))
    return b1

def readFloatB():                               #Ditto, for floats
    
    (b1,) = struct.unpack('>f', F.read(4))
    
    
    return b1

def readString():                               #Reads strings. I'm actually way too proud of this function. 
    strLength = 0                               #I spent an hour banging my head on a wall in order to figure this one out.
    offset = 0
    
    while True:
        val = F.read(1)
        (charNum,) = struct.unpack('=B', val)
        if(charNum > 20):
            offset = F.tell()
            break
    while(charNum > 20 and charNum <= 126):
        strLength += 1
        (charNum,) = struct.unpack('=B', F.read(1)) 
    
    F.seek(offset - 1)
    val = F.read(strLength)
    charDecode = val.decode('utf-8')
    return charDecode

def readByte(strType):                           #Starting to see a pattern here?
    
    if strType == "signedType":
        (b1,) = struct.unpack('>b', F.read(1))
    elif strType == "unsignedType":
            (b1,) = struct.unpack('>B', F.read(1))
    return b1  

def readQuat():
    q1 = readFloatB()
    q2 = readFloatB()
    q3 = readFloatB()
    q4 = readFloatB()
    quat1 = mathutils.Quaternion((q4, q1, q2, q3))
    
    quat1.normalize()
    
    return quat1        

def readTrans():
    f1 = (readFloatB() * 100)
    f2 = (readFloatB() * 100)
    f3 = (readFloatB() * 100)
    Trans = [f1, f2, f3]
    
    return Trans

def getFlagArray(num):
    myBitArray = []
    for i in range(8):
        myBitArray.append(i)
        myBitArray[i] = (num % 2 > .5)
        num /= 2
        
    return myBitArray

#The following 300 or so lines read many different types of data, and store them in lists for later use.

def clearIndex():
    
    global modelPath    
    global modelLoaded
    
    global marker_blocks
    global marker_name
    global marker_instance_blocks
    global marker_instance_region_index
    global marker_instance_permutation_index
    global marker_instance_node_index
    global marker_instance_translation
    global marker_instance_rotation

    global node_blocks
    global node_name
    global node_next_sibling_node_index
    global node_first_child_node_index
    global node_parent_node_index
    global node_translation
    global node_rotation
    global node_distance_from_parent

    global region_blocks
    global region_name
    global region_permutation_blocks
    global region_permutation_name
    global region_permutation_LOD_indices
    global region_permutation_marker_blocks
    global region_permutation_marker_name
    global region_permutation_marker_node_index
    global region_permutation_marker_rotation
    global region_permutation_marker_translation

    global geometry_blocks
    global geometry_part_blocks
    global geometry_part_shader_index
    global geometry_part_data_offset
    global geometry_part_uncompressed_vertex_blocks
    global geometry_part_compressed_vertex_blocks
    global geometry_part_triangle_blocks
    global geometry_part_local_nodes

    global shader_blocks
    global shader_name

    global node_array
    global marker_array

    global node_list_checksum
    global local_nodes
    global u_scale
    global v_scale
    
    modelPath = ""
    modelLoaded = False
    
    marker_blocks = 0
    marker_name = []
    marker_instance_blocks = []
    marker_instance_region_index = []
    marker_instance_permutation_index = []
    marker_instance_node_index = []
    marker_instance_translation = []
    marker_instance_rotation = []

    node_blocks = 0
    node_name = []
    node_next_sibling_node_index = []
    node_first_child_node_index = []
    node_parent_node_index = []
    node_translation = []
    node_rotation = []
    node_distance_from_parent = []

    region_blocks = 0
    region_name = []
    region_permutation_blocks = []
    region_permutation_name = []
    region_permutation_LOD_indices = []
    region_permutation_marker_blocks = []
    region_permutation_marker_name = []
    region_permutation_marker_node_index =[]
    region_permutation_marker_rotation = []
    region_permutation_marker_translation = []

    geometry_blocks = 0
    geometry_part_blocks = []
    geometry_part_shader_index = []
    geometry_part_data_offset = []
    geometry_part_uncompressed_vertex_blocks = []
    geometry_part_compressed_vertex_blocks = []
    geometry_part_triangle_blocks = []
    geometry_part_local_nodes = []

    shader_blocks = 0
    shader_name = []

    node_array = []
    marker_array = []

    node_list_checksum = 0
    local_nodes = False
    u_scale = 1.0
    v_scale = 1.0
    bpy.context.scene.regionList.clear()

def gbxIndex(myFile):
    
    global marker_blocks
    global marker_name
    global marker_instance_blocks
    global marker_instance_region_index
    global marker_instance_permutation_index
    global marker_instance_node_index
    global marker_instance_translation
    global marker_instance_rotation

    global node_blocks
    global node_name
    global node_next_sibling_node_index
    global node_first_child_node_index
    global node_parent_node_index
    global node_translation
    global node_rotation
    global node_distance_from_parent

    global region_blocks
    global region_name
    global region_permutation_blocks
    global region_permutation_name
    global region_permutation_LOD_indices
    global region_permutation_marker_blocks
    global region_permutation_marker_name
    global region_permutation_marker_node_index
    global region_permutation_marker_rotation
    global region_permutation_marker_translation

    global geometry_blocks
    global geometry_part_blocks
    global geometry_part_shader_index
    global geometry_part_data_offset
    global geometry_part_uncompressed_vertex_blocks
    global geometry_part_compressed_vertex_blocks
    global geometry_part_triangle_blocks
    global geometry_part_local_nodes

    global shader_blocks
    global shader_name

    global node_array
    global marker_array

    global node_list_checksum
    global local_nodes
    global u_scale
    global v_scale

    print("--------------------INDEXING BEGIN--------------------")
    global F

    F = open(myFile, 'rb')

    F.seek(66)
    flags = readShortB("unsignedType")
    model_flags = getFlagArray(flags)
    print("Model Flags: ", model_flags)
    if(model_flags[1] == True):
        local_nodes = True
        print("Model uses local nodes")

    F.seek(68)
    node_list_checksum = readLongB("signedType")
    print("Node List Checksum: ", node_list_checksum)

    F.seek(112)
    u_scale = readFloatB()
    F.seek(112)
    if (u_scale == 0.0):
        u_scale = 1.0
    print("Base Map U-Scale: ", u_scale)

    F.seek(116)
    v_scale = readFloatB()
    F.seek(116)
    if (v_scale == 0.0):
        v_scale = 1.0
    print("Base Map V-Scale: ", v_scale)    

    F.seek(238)
    marker_blocks = readShortB("unsignedType")
    print('Marker Blocks: ', marker_blocks)

    F.seek(250)
    node_blocks = readShortB("unsignedType")
    print('Node Blocks: ', node_blocks)

    F.seek(262)
    region_blocks = readShortB("unsignedType")
    print('Region Blocks: ', region_blocks)

    F.seek(274)
    geometry_blocks = readShortB("unsignedType")
    print('Geometry Blocks: ', geometry_blocks)

    F.seek(286)
    shader_blocks = readShortB("unsignedType")
    print('Shader Blocks: ', shader_blocks)

    #----------------------------------------------------------------------------------------------------------------------------

    F.seek(296)

    print('Marker Block Offset: ', F.tell())


    for m in range(marker_blocks):
         offset = F.tell()    
         marker_name.append(m)  #This is one of the major differences between the original Maxscript and the Python version. You absolutely CANNOT throw values into a list that isn't initialized for them in Python. This was a recurring frustration when porting the code over.
         
         marker_name[m] = readString()
         #print(marker_name[m])
         F.seek(offset + 32)
         F.seek(22, 1)
         marker_instance_blocks.append(m)
         marker_instance_blocks[m] = readShortB("unsignedType")
         F.seek(8, 1)
         
    for m in range(marker_blocks):
        temp_region_index = []
        temp_permutation_index = []
        temp_node_index = []
        temp_translation = []
        temp_rotation = []
        for i in range(marker_instance_blocks[m]):
            
            temp_region_index.append(i)
            temp_region_index[i] = readByte("unsignedType")
            temp_permutation_index.append(i)
            temp_permutation_index[i] = readByte("unsignedType")
            temp_node_index.append(i)
            temp_node_index[i] = readByte("unsignedType")
            F.seek(1, 1)
            temp_translation.append(i)
            temp_translation[i] = readTrans()
            
            temp_rotation.append(i)
            temp_rotation[i] = readQuat()
            
       

        marker_instance_region_index.append(m)
        marker_instance_region_index[m] = temp_region_index
        marker_instance_permutation_index.append(m)
        marker_instance_permutation_index[m] = temp_permutation_index
        marker_instance_node_index.append(m)
        marker_instance_node_index[m] = temp_node_index
        marker_instance_translation.append(m)
        marker_instance_translation[m] = temp_translation
        marker_instance_rotation.append(m)
        marker_instance_rotation[m] = temp_rotation

    #-----------------------------------------------------------------------------------------------------------------------------------

    print('Node Block Offset: ', F.tell())

    for n in range(node_blocks):
        offset = (F.tell())
        node_name.append(n)
        node_name[n] = readString()
        #print(node_name[n])
        F.seek(offset + 32)
        node_next_sibling_node_index.append(n)
        node_next_sibling_node_index[n] = readShortB("signedType")
        node_first_child_node_index.append(n)
        node_first_child_node_index[n] = readShortB("signedType")
        node_parent_node_index.append(n)
        node_parent_node_index[n] = readShortB("signedType")
        F.seek(2, 1)
        node_translation.append(n)
        node_translation[n] = readTrans()
        node_rotation.append(n)
        node_rotation[n] = readQuat()
        #print(node_rotation)
        node_distance_from_parent.append(n)
        node_distance_from_parent[n] = readFloatB()
        F.seek(84, 1)

    #----------------------------------------------------------------------------------------------------------------------------------
        
    print("Region Block Offset", F.tell())

    for r in range(region_blocks):
        offset = F.tell()
        region_name.append(r)
        region_name[r] = readString()
        F.seek(offset + 32)
        F.seek(34, 1)
        region_permutation_blocks.append(r)
        region_permutation_blocks[r] = readShortB("unsignedType")
        F.seek(8, 1)
        
    for r in range(region_blocks):
        temp_permutation_name = []
        temp_permutation_LOD_indices = []
        temp_permutation_marker_blocks = []
        for p in range(region_permutation_blocks[r]):
            offset = F.tell()
            temp_permutation_name.append(p)
            temp_permutation_name[p] = readString()
            
            F.seek(offset + 32)
            F.seek(32, 1)
            superlow = readShortB("signedType")
            low = readShortB("signedType")
            medium = readShortB("signedType")
            high = readShortB("signedType")
            superhigh = readShortB("signedType")
            temp_permutation_LOD_indices.append(p)
            temp_permutation_LOD_indices[p] = [superlow, low, medium, high, superhigh]
            F.seek(4, 1)
            temp_permutation_marker_blocks.append(p)
            temp_permutation_marker_blocks[p] = readShortB("unsignedType")
            F.seek(8, 1)
            
        region_permutation_name.append(r)
        region_permutation_name[r] = temp_permutation_name
        region_permutation_LOD_indices.append(r)
        region_permutation_LOD_indices[r] = temp_permutation_LOD_indices
        region_permutation_marker_blocks.append(r)
        region_permutation_marker_blocks[r] = temp_permutation_marker_blocks
        

        temp_permutation_marker_name = []
        temp_permutation_marker_node_index = []
        temp_permutation_marker_rotation = []
        temp_permutation_marker_translation = []
        
        for p in range(region_permutation_blocks[r]):
            temp_marker_name = []
            temp_marker_node_index = []
            temp_marker_rotation = []
            temp_marker_translation = []
            #print("R: ", r," ", "P: ", p)
            for m in range(region_permutation_marker_blocks[r][p]):
            
                offset = F.tell()
                temp_marker_name.append(m)
                temp_marker_name = readString()
                #print(temp_marker_name[m])
                F.seek(offset + 32)
                temp_marker_node_index.append(m)
                temp_marker_node_index[m] = readShortB("signedType")
                F.seek(2, 1)
                temp_marker_rotation.append(m)
                temp_marker_rotation[m] = readQuat()
                temp_marker_translation.append(m)
                temp_marker_translation[m] = readTrans()
                F.seek(16, 1)
            
            
            temp_permutation_marker_name = temp_marker_name
            temp_permutation_marker_node_index = temp_marker_node_index
            temp_permutation_marker_rotation = temp_marker_rotation
            temp_permutation_marker_translation = temp_marker_translation
            
        region_permutation_marker_name = temp_permutation_marker_name
        region_permutation_marker_node_index = temp_permutation_marker_node_index
        region_permutation_marker_rotation = temp_permutation_marker_rotation
        region_permutation_marker_translation = temp_permutation_marker_translation
        
    #----------------------------------------------------------------------------------------------------------------------------------

    print("Geometry Block Offset: ", F.tell())

    for g in range(geometry_blocks):
        F.seek(38, 1)
        geometry_part_blocks.append(g)
        geometry_part_blocks[g] = readShortB("unsignedType")
        F.seek(8, 1)    

    for g in range(geometry_blocks):
        temp_part_shader_index = []
        temp_part_uncompressed_vertex_blocks = []
        temp_part_compressed_vertex_blocks = []
        temp_part_triangle_blocks = []
        
        if(local_nodes == True):
            temp_part_local_nodes = []
        
        for p in range(geometry_part_blocks[g]):
            F.seek(4, 1)
            temp_part_shader_index.append(p)
            temp_part_shader_index[p] = readShortB("signedType")
            F.seek(28, 1)
            temp_part_uncompressed_vertex_blocks.append(p)
            temp_part_uncompressed_vertex_blocks[p] = readShortB("unsignedType")
            F.seek(10, 1)
            temp_part_compressed_vertex_blocks.append(p)
            temp_part_compressed_vertex_blocks[p] = readShortB("unsignedType")
            F.seek(10, 1)
            temp_part_triangle_blocks.append(p)
            temp_part_triangle_blocks[p] = readShortB("unsignedType")
            
            offset = F.tell()
            #print(offset)
            
            if(local_nodes == True):
                F.seek(46, 1)
                number_local_nodes = readShortB("unsignedType")
                the_local_nodes = []
                
                for n in range(number_local_nodes):
                    the_local_nodes.append(readByte("unsignedType"))
                    
                temp_part_local_nodes = the_local_nodes
                
            F.seek(offset + 72)
        
        geometry_part_shader_index.append(g)
        geometry_part_shader_index[g] = temp_part_shader_index
        geometry_part_uncompressed_vertex_blocks.append(g)
        geometry_part_uncompressed_vertex_blocks[g] = temp_part_uncompressed_vertex_blocks
        geometry_part_compressed_vertex_blocks.append(g)
        #print(geometry_part_compressed_vertex_blocks[g])
        geometry_part_compressed_vertex_blocks[g] = temp_part_compressed_vertex_blocks
        geometry_part_triangle_blocks.append(g)
        geometry_part_triangle_blocks[g] = temp_part_triangle_blocks
        if(local_nodes == True):
            geometry_part_local_nodes.append(g)
            geometry_part_local_nodes[g] = temp_part_local_nodes
        
        #print(g)
            
        temp_part_data_offset = []
        for p in range(geometry_part_blocks[g]):
            temp_part_data_offset.append(p)
            temp_part_data_offset[p] = F.tell()
            F.seek(geometry_part_uncompressed_vertex_blocks[g][p] * 68, 1) #This drove me crazy at first, but it's really just a simple 2D array/list
            
            #print(geometry_part_uncompressed_vertex_blocks[g][p])
            F.seek(geometry_part_compressed_vertex_blocks[g][p] * 32, 1)
            F.seek(geometry_part_triangle_blocks[g][p] * 6, 1)
        
        geometry_part_data_offset.append(g)
        geometry_part_data_offset[g] = temp_part_data_offset
        
    #---------------------------------------------------------------------------------------------------------------------

    print("Shader Block Offset: ", F.tell())

    F.seek(shader_blocks * 32, 1)

    for s in range(shader_blocks):
        shader_dir = readString()
        shader_dir = shader_dir.split("\\")[3]
        #print(shader_dir)
        shader_name.append(s)
        shader_name[s] = shader_dir
        
#----------------------------------------------------------------------------------------------------------------------------
def gbxImport():
    
    global import_region_permutation
    import_region_permutation = []
    
    for r in range(region_blocks):
        
        if bpy.context.scene.regionList[r].region_enable == True:
        
            import_region_permutation.append([r, int(bpy.context.scene.regionList[r].perm_enum)])
    
    
    
    if(nodesEnabled == 1 or markersEnabled == 1):
        node_array = []
        marker_array = []
        
        for n in range(node_blocks):
            node_array.append(n)
            bpy.ops.mesh.primitive_uv_sphere_add(size= nodeSize)
            node_array[n] = bpy.context.object
            
            mat = bpy.data.materials.new("Node")
            mat.diffuse_color = nodeColor
            node_array[n].data.materials.append(mat)
            
            node_array[n].name= node_name[n]
            
            
            if(node_parent_node_index[n] != -1):
                
                node_array[n].parent = node_array[node_parent_node_index[n]]        
            
            
            node_array[n].rotation_mode ='QUATERNION'
            node_array[n].rotation_quaternion = (node_rotation[n].w, -node_rotation[n].x, -node_rotation[n].y, -node_rotation[n].z)
            
            node_array[n].location = node_translation[n]
            
            
            
                    
                    
    #---------------------------------------------------------------------------------------------------------------------------------------------                
        if(markersEnabled == 1):
            
            m = 0
            for b in range(marker_blocks):
                
                for i in range(marker_instance_blocks[b]):
                    
                    for p in range(len(import_region_permutation)):
                        
                        if(marker_instance_region_index[b][i] == import_region_permutation[p][0] and marker_instance_permutation_index[b][i] == import_region_permutation[p][1]):
                            
                            marker_array.append(m)
                            print("First loop")
                            bpy.ops.mesh.primitive_uv_sphere_add(size= markerSize)
                            marker_array[m] = bpy.context.object
                            
                            mat = bpy.data.materials.new("Marker")
                            mat.diffuse_color = markerColor
                            marker_array[m].data.materials.append(mat)
                            
                            marker_array[m].name = '#' + marker_name[b]
                            marker_array[m].parent = node_array[marker_instance_node_index[b][i]]
                            marker_array[m].rotation_mode = 'QUATERNION'
                            marker_array[m].rotation_quaternion = (marker_instance_rotation[b][i].w, -marker_instance_rotation[b][i].x, -marker_instance_rotation[b][i].y, -marker_instance_rotation[b][i].z)
                            marker_array[m].location = marker_instance_translation[b][i]
                            m += 1
            
            for r in range(region_blocks):
                for p in range(region_permutation_blocks[r]):
                    for b in range(region_permutation_marker_blocks[r][p]):
                        for i in range(len(import_region_permutation)):
                            if(r == import_region_permutation[i][0] and p == import_region_permutation[i][1]):
                                
                                marker_array.append(m)
                                print("Second loop")
                                bpy.ops.mesh.primitive_uv_sphere_add(size= markerSize)
                                marker_array[m] = bpy.context.object
                                
                                mat = bpy.data.materials.new("Marker")
                                mat.diffuse_color = markerColor
                                marker_array[m].data.materials.append(mat)
                                
                                marker_array[m].name = '#' + region_permutation_marker_name[r][p][b]
                                marker_array[m].parent = node_array[region_permutation_marker_node_index[r][p][b]]
                                marker_array[m].rotation_mode = 'QUATERNION'
                                marker_array[m].rotation_quaternion = (region_permutation_marker_rotation[r][p][b].w, -region_permutation_marker_rotation[r][p][b].x, -region_permutation_marker_rotation[r][p][b].y, -region_permutation_marker_rotation[r][p][b].z)
                                marker_array[m].location = region_permutation_marker_translation[r][p][b]
                                m += 1
                                                
        if(nodesEnabled == False): #Because of how blender handles parenting and transformations, the marker array must be saved to a matrix prior to clearing the node array.
            
            for c in range(len(marker_array)):
                
                bpy.ops.object.select_all(action='DESELECT')
                temp_marker_array_matrix = marker_array[c].matrix_world.copy()
                marker_array[c].parent = None
                marker_array[c].matrix_world = temp_marker_array_matrix
                
            for n in range(node_blocks):    
                
                node_array[n].select = True
                bpy.ops.object.delete()              

    
    if(modelEnabled == True):
                
        import_geometry_indices = []

        for i in range(len(import_region_permutation)):
            
            import_geometry_indices.append(i)
            import_geometry_indices[i] = (region_permutation_LOD_indices[import_region_permutation[i][0]][import_region_permutation[i][1]][LOD_index])

        for geometry_index in range(len(import_geometry_indices)):
            
            g = import_geometry_indices[geometry_index]
            part_meshes = []
            part_vertex_node_index = []
            part_vertex_node_weight = []
            
            for p in range(geometry_part_blocks[g]):
                
                vertex_xyz = []
                vertex_uvw = []
                vertex_node_index = []
                vertex_node_weight = []
                vertex_order = []
                triangles = []
                
                
                for cnt in range(geometry_part_uncompressed_vertex_blocks[g][p]):
                    
                    vertex_xyz.append("FILLER")
                    vertex_uvw.append("FILLER")
                
                vertex_xyz[geometry_part_uncompressed_vertex_blocks[g][p] - 1] = 0
                vertex_uvw[geometry_part_uncompressed_vertex_blocks[g][p] - 1] = 0
                
                F.seek(geometry_part_data_offset[g][p])
                
                for v in range(geometry_part_uncompressed_vertex_blocks[g][p]):
                    vertex_xyz[v] = readTrans()
                    F.seek(36, 1)
                    
                    if(uvwEnabled == 1):
                        u_coord = readFloatB() * u_scale
                        v_coord = 1 - (readFloatB() * v_scale)
                        vertex_uvw[v] = [u_coord, v_coord]    
                    else:
                        F.seek(8, 1)
                        
                    F.seek(12, 1)
                 
                F.seek(geometry_part_compressed_vertex_blocks[g][p] * 32, 1)

                triangle_vertices = (geometry_part_triangle_blocks[g][p] * 3)
                
                for t in range(triangle_vertices):
                    vertex_order.append((readShortB("signedType")) + 0)
            
                vo_count = (len(vertex_order) - 1)
                
                if(vertex_order[vo_count] == -1):
                    vertex_order.remove(-1)
                    
                if(vertex_order[vo_count - 1] == -1):
                    vertex_order.remove(-1)    
                    
                for w in range(len(vertex_order) - 2):
                    triangles.append(w)
                    triangles[w] = [vertex_order[w], vertex_order[w+1], vertex_order[w+2]]
                    
                for r in range(0, len(triangles), 2):
                    a = triangles[r][0]
                    triangles[r][0] = triangles[r][2]
                    triangles[r][2] = a
                    
                for d in range(len(triangles) - 1, 0, -1):

                    if (triangles[d][0] == triangles[d][1]) or (triangles[d][1] == triangles[d][2]) or (triangles[d][0] == triangles[d][2]):
                        del triangles[d]
                    
                NewMesh = bpy.data.meshes.new(shader_name[geometry_part_shader_index[g][p]])
                NewMesh.from_pydata(vertex_xyz, [], triangles)
                NewMesh.polygons.foreach_set("use_smooth", [True] * len(NewMesh.polygons))
                NewMesh.update()
                NewObj = bpy.data.objects.new(shader_name[geometry_part_shader_index[g][p]], NewMesh)
                bpy.context.scene.objects.link(NewObj)                    
                
                if(uvwEnabled == True):
                    # vertex index : vertex value pair
                    vi_uv = {i: uv for i, uv in enumerate(vertex_uvw)}
                    #initialize an empty list
                    per_loop_list = [0.0] * len(NewMesh.loops)
                    
                    for loop in NewMesh.loops:
                        per_loop_list[loop.index] = vi_uv.get(loop.vertex_index)
                        # flattening
                    
                    per_loop_list = [uv for pair in per_loop_list for uv in pair]
                    # creating the uvs
                    NewMesh.uv_textures.new("test")
                    NewMesh.uv_layers[0].data.foreach_set("uv", per_loop_list)
                    #  me_ob.uv_layers[0] assumes you had no uv layers before, only the newly created one.

    #It just works. :ToddHoward:

    #I'd like to thank Adam Papamarcos, known as TheGhost, for making the original Bluestreak plugin that I'm probably butchering horribly.



class RegionItem(bpy.types.PropertyGroup):
        
    region_enable = bpy.props.BoolProperty(name= "", default = True)
    region_name = bpy.props.StringProperty(name= "", default="")
    region_num = bpy.props.IntProperty(name= "", default = 0)
    
    
    def perm_enum_cb(self, context):    #Callback function that determines the options of the perm enum.
        
        #It really seems like this is the only way to do it. If I don't, the enum doesn't seem to get updated.
        
        global region_permutation_name
        
        
        
        perm_enum_items = [] 
        
        for i in range(len(region_permutation_name[self.region_num])):
            
            ident = str(i)
            
            perm_enum_items.append((ident, region_permutation_name[self.region_num][i], "TEST"))
                           
        return perm_enum_items                  
        
        
    
    perm_enum = bpy.props.EnumProperty(name = "", items=perm_enum_cb)
    
    
            
class RegionUIList(bpy.types.UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.prop(item, "region_enable")
        layout.label(item.region_name)
        layout.prop(item, "perm_enum")


class ToolsPanel(bpy.types.Panel):
    bl_label = ".gbxmodel Importer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        
        
        
        row.operator("gbxmodel.load", text="Load")
        
        row.operator("gbxmodel.unload", text="Unload")
        
        
        
        col = layout.column()
        
        col.enabled = modelLoaded
        box = col.box()
        box.label(modelPath)
        
        col.separator()
        col.separator()
        
        col.prop(context.scene, "modelEnabled_bool")
        box = col.box()
        box.enabled = bpy.context.scene.modelEnabled_bool
        box.prop(context.scene, "lodSelect")
        box.prop(context.scene, "uvwEnabled_bool")
        
        boxrow = box.row()
        boxrow.label("    Region")
        boxrow.label("    Permutation")
        box.template_list("RegionUIList", "", context.scene, "regionList", context.scene, "regionIndex")
        
        col.separator()
        col.separator()
        
        col.prop(context.scene, "nodesEnabled_bool")
        box = col.box()
        box.enabled = bpy.context.scene.nodesEnabled_bool
        box.prop(context.scene, "nodeSize_float")
        box.prop(context.scene, "nodeColor")
        
        col.separator()
        col.separator()
        
        col.prop(context.scene, "markersEnabled_bool")
        box = col.box()
        box.enabled = bpy.context.scene.markersEnabled_bool
        box.prop(context.scene, "markerSize_float")
        box.prop(context.scene, "markerColor")
        
        col.separator()
        col.separator()
        
        col.operator("gbxmodel.import", text="Import Selected")
        
        row = layout.row()
        row = layout.row()
        
        row.label("BETA v0.6.0")

               
class LoadButton(bpy.types.Operator):
    bl_idname ="gbxmodel.load"
    bl_label = "Load .gbxmodel"
    filter_glob = bpy.props.StringProperty(default="*.gbxmodel", options={'HIDDEN'})
    filepath = bpy.props.StringProperty(subtype="FILE_PATH")
    filename = bpy.props.StringProperty()
    
    def execute(self, context):
        
        global modelPath
        global modelLoaded
        global region_blocks
        global region_name
        
        clearIndex()
        gbxIndex(self.filepath)
        
        for i in range(region_blocks):
            
            region = bpy.context.scene.regionList.add()
            region.region_name = region_name[i]
            region.region_num = i
            
        modelPath = self.filepath.rsplit("\\", 1)
        modelPath = modelPath[1]
        
        modelLoaded = True 
        
        
        return{'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class UnloadButton(bpy.types.Operator):
    bl_idname = "gbxmodel.unload"
    bl_label = "Unload .gbxmodel"
    
    @classmethod
    def poll(cls, context):
        modelLoaded
        return (modelLoaded != False)
    
    def execute(self,context):
        clearIndex()
        return{'FINISHED'}



#matEnabled = False
#bonesEnabled = False
#bipedBones = False
#allBones = False

class ImportButton(bpy.types.Operator):
    bl_idname = "gbxmodel.import"
    bl_label = "Import with current settings"
    
    @classmethod
    def poll(cls, context):
        modelLoaded
        return (modelLoaded != False)
    
    def execute(self, context):
        
        global modelEnabled
        global uvwEnabled
        global nodesEnabled
        global nodeSize
        global nodeColor
        global markersEnabled
        global markerSize
        global markerColor
        global LOD_index
        
        modelEnabled = True if bpy.context.scene.modelEnabled_bool else False
        uvwEnabled = True if bpy.context.scene.uvwEnabled_bool else False
        
        
        
        nodesEnabled = True if bpy.context.scene.nodesEnabled_bool else False 
        nodeSize = bpy.context.scene.nodeSize_float
        nodeColor = bpy.context.scene.nodeColor
        markersEnabled = True if bpy.context.scene.markersEnabled_bool else False
        markerSize = bpy.context.scene.markerSize_float
        markerColor = bpy.context.scene.markerColor
        lodSelect = int(bpy.context.scene.lodSelect)
        LOD_index = lodSelect
        gbxImport()
        
        
            

        return{'FINISHED'}    



def register():
    
    bpy.utils.register_class(ToolsPanel)
    bpy.utils.register_class(LoadButton)
    bpy.utils.register_class(UnloadButton)
    bpy.utils.register_class(ImportButton)
    bpy.utils.register_class(RegionItem)
    
    bpy.utils.register_class(RegionUIList)
    
    bpy.types.Scene.loadedModel = bpy.props.StringProperty(name ="",description="Test", default="This is a test")
    bpy.types.Scene.modelEnabled_bool = bpy.props.BoolProperty(name="Import Model", description="Import model's geometry", default=True)
    bpy.types.Scene.lodSelect = bpy.props.EnumProperty(name="LOD", description="Level of detail selection", items = 
    [('4', 'Super High', ''),
    ('3', 'High', ''),
    ('2', 'Medium', ''),
    ('1', 'Low', ''),
    ('0', 'Super Low', ''),])
    
    
    
    bpy.types.Scene.regionList = bpy.props.CollectionProperty(type= RegionItem)
    bpy.types.Scene.regionIndex = bpy.props.IntProperty(name= "List Index", default = -1)
    
    bpy.types.Scene.uvwEnabled_bool = bpy.props.BoolProperty(name="Import UVs", description="Import model's UV mapping", default=True)
    bpy.types.Scene.nodesEnabled_bool = bpy.props.BoolProperty(name="Import Nodes", description="Import model's nodes", default=True)
    bpy.types.Scene.nodeSize_float = bpy.props.FloatProperty(name="Size", subtype='UNSIGNED', description="Set size of nodes", default=2.0, min=0.01)
    bpy.types.Scene.nodeColor = bpy.props.FloatVectorProperty(name="Color", subtype='COLOR', description="Set color of nodes", default=(0.0,1.0,0.0))
    bpy.types.Scene.markersEnabled_bool = bpy.props.BoolProperty(name="Import Markers", description="Import model's markers", default=True)
    bpy.types.Scene.markerSize_float = bpy.props.FloatProperty(name="Size", subtype='UNSIGNED', description="Set size of markers", default=1.0, min=0.01)
    bpy.types.Scene.markerColor = bpy.props.FloatVectorProperty(name="Color", subtype='COLOR', description="Set color of markers", default=(0.0,0.0,1.0))
    
def unregister():
    
    bpy.context.scene.regionList.clear()      
    bpy.utils.unregister_class(ToolsPanel)
    bpy.utils.unregister_class(LoadButton)
    bpy.utils.unregister_class(UnloadButton)
    bpy.utils.unregister_class(ImportButton)
    bpy.utils.unregister_class(RegionItem)
    
    bpy.utils.unregister_class(RegionUIList)
    del bpy.types.Scene.loadedModel
    del bpy.types.Scene.modelEnabled_bool
    del bpy.types.Scene.lodSelect
    del bpy.types.Scene.regionList
    del bpy.types.Scene.regionIndex
    del bpy.types.Scene.uvwEnabled_bool
    
    del bpy.types.Scene.nodesEnabled_bool
    del bpy.types.Scene.nodeSize_float
    del bpy.types.Scene.nodeColor
    del bpy.types.Scene.markersEnabled_bool
    del bpy.types.Scene.markerSize_float
    del bpy.types.Scene.markerColor

if __name__ == "__main__" :
    register()      


           
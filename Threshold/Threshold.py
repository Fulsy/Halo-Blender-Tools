
#<!--
#
#                                                    ___
#                                           ___  \   \
#                                           \   \  \  \
#                                            \ \___________------___
#LOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOLOL(/  /_______loljet________/
#                                            /__/   |   /
#                                          n          /  /
#                                                      /  /
#                                                     /___ /
#
#
#-->




#INFORMATION!
bl_info = {
    "name": "HBT WaltzStreet .JMS Exporter",
    "author": "Original WaltzStreet script by Cyboryxmen, Modified by Fulsy",
    "blender": (2, 6, 5),
    "location": "File > Import-Export",
    "description": "Export .JMS files for compilation by Tool.exe",
    "warning": "",
    "category": "Import-Export"}





import time
import os
import bpy
import mathutils
import math
import re
from decimal import *
getcontext().prec=13


#DECLARING ALL GLOBAL FUNCTIONS!
def find_region(obj):
    found="undefined"
    for group in obj.users_group:
        if found=="undefined":
            if re.match("~", group.name,):
                found=group.name
        else:
            throw_exception(6, obj)
    return found

def find_last_parent(obj):
    testparent=obj.parent
    while testparent!=None:
        obj=testparent
        testparent=obj.parent
    return obj

def find_last_node(obj):
    testparent=obj.parent
    while not re.match("frame", testparent.name, re.IGNORECASE) or\
    re.match("bip01", testparent.name, re.IGNORECASE):
        testparent=testparent.parent
    return testparent

def find_child(node):
    while child!="found":
        child=node.child

def find_root_node(node, mainframe, nodeslist):
    testframe=find_last_parent(node)
    if testframe not in nodeslist:
        nodeslist.append(testframe)
    if mainframe=="lol what frame?":
        mainframe=testframe 
    if testframe!=mainframe:
        return "a complete total failure!"
    else:
        return mainframe

def deselect():
    if not bpy.ops.object.select_all.poll():
        bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False, location=(0, 0, 506.061), rotation=(0, 0, 0), layers=(False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.ops.object.delete(use_global=False)


def select():
    if not bpy.ops.object.select_all.poll():
        bpy.ops.object.editmode_toggle()
    bpy.ops.object.select_all(action='SELECT')
    
def select_all_layers():
    x=0
    y=[]
    while x!=20:
        y.append(bpy.context.scene.layers[x])
        bpy.context.scene.layers[x]=True
        x+=1
    return y

def deselect_layers(y):
    x=0
    for bool in y:
        bpy.context.scene.layers[x]=bool
        x+=1

def throw_exception(failmessage, info):
    print("ERROR!")
    print("ERROR!")
    print("ERRPR!")
    print("ERROR!")
    if failmessage==0:
        print("Error message:00")
        
        print("please link all nodes to one object!")
    if failmessage==1:
        print("Error message:01")
        
        print("there were no nodes detected!\
        please make at least one node in the scene!")
    if failmessage==2:
        print("Error message:02")
        
        print("there were no geometry to be exported. please link all\
        geometry to a single node!")
    if failmessage==3:
        print("Error message:03")
        
        print("an open edge was detected when checking object:"\
        + info)
    if failmessage==4:
        print("Error message:04")
        
        print("you forgot to assign a material to geometry object:" + info)
    if failmessage==5:
        print("Error message:05")
        
        print("The file export was uncucessful")
    if failmessage==6:
        print("Error message:06")
        
        print("You linked object {} to more than 1 region".format(obj))
    if failmessage==7:
        print("Error message:07")
        
    if failmessage==8:
        print("Error message:08")
        
    if failmessage==9:
        print("Error message:09")
        
    if failmessage==10:
        print("Error message:10")
        
    if failmessage==11:
        print("Error message:11")
        
    print("")
    raise NameError




#MAKING IMPORT-EXPORT OPERATOR!
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator



class ExportJMS(Operator, ExportHelper):
    bl_idname = "export_jms.export"
    bl_label = "Export JMS"

    filename_ext = ".jms"

    filter_glob = StringProperty(
            default="*.jms",
            options={'HIDDEN'},
            )
            


    def execute(self, context):
        return export_jms(context, self.filepath)

def menu_func_export(self, context):
    self.layout.operator(ExportJMS.bl_idname, text="Halo CE JMS file (.jms)")


def register():
    bpy.utils.register_class(ExportJMS)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportJMS)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()




def export_jms(context, filepath):
    layersSelected=[]
    scene=bpy.context.scene
    blenderscale=bpy.context.scene.unit_settings.scale_length
    objectslist=list(bpy.context.scene.objects)
    versionnumber=8200
    haloscale=1
    counter = 0
    haloestimatedscale=3251
    scale=Decimal(haloscale/blenderscale)
    mainframe="lol what frame?"
    directory=""
    nodeslist=[]
    materialslist=[]
    texturedirectory="<none>"
    markerslist=[]
    geometrylist=[]
    mesheslist=[]
    regionslist=["unnamed"]
    vertslist=[]
    vertnodes=[]
    vertweights=[]
    vertvectors=[]
    vertnormals=[]
    uvlist=[]
    faceslist=[]
    regions=[]
    polymaterials=[]
    status=("okay!")
    getcontext().prec=13
    
    
    #THE SORTING OF STUFF!
    #Picks out all markers, nodes, and mesh objects in the scene, and puts them into appropriate lists.
    print("Script start")
    print("selecting all layers")
    layersSelected=select_all_layers()
    print("sorting out all items...")
    for obj in objectslist:
        if re.match("frame", obj.name, re.IGNORECASE) or\
        re.match("bip01", obj.name, re.IGNORECASE):
            nodeslist.append(obj)
        elif re.match("#", obj.name,):
            markerslist.append(obj)
        else:
            if obj.type=='MESH':
                geometrylist.append(obj)
                
    if len(nodeslist)==0:
        throw_exception(1, "lol")

    for node in nodeslist:  
        if status!="a complete total failure!":
            status=find_root_node(node, mainframe, nodeslist)
            print("checking node:" + node.name + "...")
            mainframe=status
        else:                                                                                                    
            throw_exception(0, "lol")

    try:
        print("current mainframe:" + mainframe.name)
    except:
        throw_exception(0, "lol")
    print("current mainframe:" + mainframe.name)
    del nodeslist[nodeslist.index(mainframe)]
    nodeslist.insert(0, mainframe)

    print("deleting unnnessary items...")
    if mainframe in geometrylist:
        del geometrylist[geometrylist.index(mainframe)]
    elif mainframe in markerslist:
        del markerslist[markerslist.index(mainframe)]
    
    for obj in geometrylist:
        testparent=find_last_parent(obj)
        if testparent!=mainframe:
            del geometrylist[geometrylist.index(obj)]         

    for obj in markerslist:
        testparent=find_last_parent(obj)
        if testparent!=mainframe:
            del markerslist[markerslist.index(obj)]

    if len(geometrylist)==0:
        throw_exception(2, "lol")

    print("gathering materials...")
    for obj in geometrylist:
        if len(obj.material_slots)!=0:
            for slot in obj.material_slots:
                if slot.material not in materialslist:
                    materialslist.append(slot.material)
        else:
            throw_exception(4, obj.name)
    
    print("gathering regions...")
    for group in bpy.data.groups:
        regionslist.append(group.name)
    try:
        regionslist[0]
    except:
        bpy.ops.group.create(name="unnamed")
        regionslist.append(bpy.data.groups["unnamed"])



    #THE REAL FUN BEGINS!
    #Prepare mesh object for exporting.
    print("converting geometry object to mesh...")
    deselect()
    for obj in geometrylist:
        obj.select=True
        bpy.ops.object.duplicate(linked=False)
        mesheslist.append(bpy.context.selected_objects[0])
        deselect()

    print("applying modifiers...")
    for mesh in mesheslist:
        deselect()
        mesh.select=True
        bpy.context.scene.objects.active=mesh
        bpy.ops.object.convert(target='MESH', keep_original=False)

    print("UV unwrapping wrapped objects...")
    for mesh in mesheslist:
        deselect()
        mesh.select=True
        bpy.context.scene.objects.active=mesh
        try:
            mesh.data.uv_layers.active.data
        except:
            bpy.ops.uv.smart_project(angle_limit=66, island_margin=0, user_area_weight=0)

    print("triangulating faces...")
    for mesh in mesheslist:
        deselect()
        mesh.select=True
        bpy.context.scene.objects.active = mesh
        if not bpy.ops.mesh.quads_convert_to_tris.poll():
            bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.quads_convert_to_tris()
        bpy.ops.object.editmode_toggle()

    print("gathering faces and vertices...")
    for mesh in mesheslist:
        region=find_region(mesh)
        if region=="undefined":
            region=regionslist[0]
        node=find_last_node(mesh)
        matrix=mesh.matrix_world
        deselect()
        mesh.select=True
        bpy.context.scene.objects.active = mesh
        uv_layer = mesh.data.uv_layers.active.data
        
        for face in mesh.data.polygons:
            faceslist.append(face)
            material=mesh.data.materials[face.material_index]
            polymaterials.append(materialslist.index(material))
            regions.append(regionslist.index(region))
            for vert_index in face.vertices:
                vertnodes.append([nodeslist.index(node),-1])
                vertweights.append(0)
                vert=mesh.data.vertices[vert_index]
                vertslist.append(vert)
                vector=matrix*vert.co
                vertvectors.append(vector)
                #OMG HALO WANTS THE NORMAL OF THE POLYS NOT THE VERTEX EVEN THOGH IT IS UNDER VERTEX WHY! WHY! THAT DOES NOT MAKE ANY SENSE! PUT IT UNDER POLYS THEN YOU DOLT!
                vertnormals.append(face.normal)
            for loop_index in face.loop_indices:
                uvlist.append(uv_layer[loop_index].uv)
                #print(uv_layer[loop_index].uv)





    print("preparation complete!")
    print("Here are the meshes to be exported:")
    for mesh in mesheslist:
        print(mesh.name)
    print("")
    print("cleaning up...")

    deselect()
    for mesh in mesheslist:
        mesh.select=True
    bpy.ops.object.delete(use_global=False)
    
    deselect_layers(layersSelected)

    print("")
    print("")
    print("")
    print("status:okay!")
    print("")
    print("beginning JMS data export!")
    print("")
    print("")
    print("")

    
    
    f = open(filepath, 'w')
    f.write("{}\n".format(versionnumber))
    f.write("{}\n".format(haloestimatedscale))
    f.write("{}\n".format(len(nodeslist)))
    
    for node in nodeslist:
        print("writing node data:{}...".format(node.name))
        child0=-1
        child1=-1
        matrix=node.matrix_world
        vector=matrix*node.location
        roat=node.rotation_quaternion
        roat1=Decimal(roat[1]).quantize(Decimal('1.000000'))
        roat2=Decimal(roat[2]).quantize(Decimal('1.000000'))
        roat3=Decimal(roat[3]).quantize(Decimal('1.000000'))
        roat0=Decimal(roat[0]).quantize(Decimal('1.000000'))
        vector0=Decimal(vector[0]).quantize(Decimal('1.000000'))
        vector1=Decimal(vector[1]).quantize(Decimal('1.000000'))
        vector2=Decimal(vector[2]).quantize(Decimal('1.000000'))
        f.write("{}\n".format(node.name))
        f.write("{}\n".format(child0))
        f.write("{}\n".format(child1))
        f.write("{}\t{}\t{}\t{}\n".format(roat1, roat2, roat3, roat0))
        f.write("{}\t{}\t{}\n".format(vector0, vector1, vector2))
    f.write("{}\n".format(len(materialslist)))
    
    for material in materialslist:
        print("writing material:{}...".format(material.name))
        f.write("{}\n".format(material.name))
        f.write("{}\n".format(texturedirectory))
    f.write("{}\n".format(len(markerslist)))
    
    for marker in markerslist:
        name=marker.name.replace(' ', '')[+1:]
        print("writing marker data:{}...".format(name))
        node=find_last_node(marker)
        node0=-1
        node1=nodeslist.index(node)
        matrix=marker.matrix_world
        markerweight=2.0
        vector=matrix*marker.location
        roat=marker.rotation_quaternion
        roat1=Decimal(roat[1]).quantize(Decimal('1.000000'))
        roat2=Decimal(roat[2]).quantize(Decimal('1.000000'))
        roat3=Decimal(roat[3]).quantize(Decimal('1.000000'))
        roat0=Decimal(roat[0]).quantize(Decimal('1.000000'))
        vector0=Decimal(vector[0]).quantize(Decimal('1.000000'))
        vector1=Decimal(vector[1]).quantize(Decimal('1.000000'))
        vector2=Decimal(vector[2]).quantize(Decimal('1.000000'))
        f.write("{}\n".format(name))
        f.write("{}\n".format(node0))
        f.write("{}\n".format(node1))
        f.write("{}\t{}\t{}\t{}\n".format(roat1, roat2, roat3, roat0))
        f.write("{}\t{}\t{}\n".format(vector0, vector1, vector2))
        f.write("{}\n".format(markerweight))
    f.write("{}\n".format(len(regionslist)))
    
    for region in regionslist:
        print("writing region data:{}...".format(region))
        f.write("{}\n".format(region))
    f.write("{}\n".format(len(vertslist)))
    print("here comes the big one!")
    
    
    for vert in vertslist:
        
        
        node=vertnodes[vertslist.index(vert)]
        node0=node[0]
        node1=node[1]
        smoothinggroup=0
        vector=vertvectors[vertslist.index(vert)]
        roat=vertnormals[vertslist.index(vert)]
        uv=uvlist[counter]
        counter += 1
        #print(vertslist.index(vert))
        
        vector0=Decimal(vector[0]).quantize(Decimal('1.000000'))
        vector1=Decimal(vector[1]).quantize(Decimal('1.000000'))
        vector2=Decimal(vector[2]).quantize(Decimal('1.000000'))
        
        vector0=vector0*scale
        vector1=vector1*scale
        vector2=vector2*scale
        
        roat0=Decimal(roat[0]).quantize(Decimal('1.000000'))
        roat1=Decimal(roat[1]).quantize(Decimal('1.000000'))
        roat2=Decimal(roat[2]).quantize(Decimal('1.000000'))
        
        vertweight=vertweights[vertslist.index(vert)]
        
        uv0=Decimal(uv[0]).quantize(Decimal('1.000000'))
        uv1=Decimal(uv[1]).quantize(Decimal('1.000000'))
        
        f.write("{}\n".format(node0))
        f.write("{}\t{}\t{}\n".format(vector0, vector1, vector2))
        f.write("{}\t{}\t{}\n".format(roat0, roat1, roat2))
        f.write("{}\n".format(node1))
        f.write("{}\n".format(vertweight))
        f.write("{}\n".format(uv0))
        f.write("{}\n".format(uv1))
        f.write("{}\n".format(smoothinggroup))
    f.write("{}\n".format(len(faceslist)))
    x=0
    
    for face in faceslist:
        region=regions[faceslist.index(face)]
        material=polymaterials[faceslist.index(face)]
        f.write("{}\n".format(region))
        f.write("{}\n".format(material))
        f.write("{}\t{}\t{}\n".format(x, x+1, x+2))
        x+=3
    f.close
    
    print("")
    print("")
    print("")
    print("Export complete!")
    print("")
    print("")
    print("")


    return {'FINISHED'}

#memo
#   support for bones not yet implemented
#   export regions not yet implemented
#   experiment on sealed world rules
#   test if scale is correct

##########################################
# Copyright AI Robot Media 2017
# Bug fixes and Blender 2.8 support by CodingEric@Github
# Rename it to io_export_xaml.py before installation if encountering bugs
##########################################

bl_info = {
    "name": "XAML format (.xaml)",
    "author": "AI Robot Media, CodingEric",
    "version": (1, 0, 1),
    "blender": (2, 80, 0),
    "location": "File > Export > XAML",
    "description": "Export scene to XAML",
    "warning": "",
    "wiki_url": "http://airobotmedia.com",
    "category": "Import-Export"}

import bpy
import bmesh
from mathutils import Matrix
from io import StringIO
from math import *

class XamlWriter :
    def __init__(self):
        self.outfile = StringIO()
    
    def toString(self):
        return self.outfile.getvalue()

    def writeString(self, str):
        self.outfile.write(str)
        return 

    def writeLine(self, str):
        self.outfile.write(str + "\n")
        return 

def compactFloat(number):
    str = "%.6f" % number

    if len(str) == 0 : return str

    backStr = str[-5:]
    frontStr = str[:-5]
    
    str = frontStr + backStr.rstrip("0")

    return str

##########################################
#  Xaml Exporter
##########################################

class XamlExporter :
    def __init__(self):
        self.writer = XamlWriter()

    def writeCamera(self, cameraObj):
        self.writer.writeString("Camera")

    def writeLamp(self, lampObj):
        self.writer.writeString("Lamp")

    def writeMesh(self, meshObj):
        #transform into xaml coordinate system (Y-UP)
        matrix = Matrix.Rotation(radians(-90), 4, 'X')
        
        # get mesh data from obj
        mesh = meshObj.data

        # copy mesh so it does not transform original
        mesh = mesh.copy()

        #apply tranform matrix to whole mesh
        mesh.transform(matrix)

        # Vertices are correct
        self.writer.writeString("Positions=" + '"')
        for vertice in mesh.vertices:
            self.writer.writeString("%s,%s,%s " % (compactFloat(round(vertice.co.x, 6)), compactFloat(round(vertice.co.y, 6)), compactFloat(round(vertice.co.z, 6))))
        self.writer.writeLine('"')

        # Triangle Indices
        self.writer.writeString("TriangleIndices=" + '"')
        for polygon in mesh.polygons:
            if len(polygon.vertices) == 3:
                self.writer.writeString("%d,%d,%d " % (polygon.vertices[0], polygon.vertices[1], polygon.vertices[2],))
            elif len(polygon.vertices) == 4:
                self.writer.writeString("%d,%d,%d " % (polygon.vertices[0], polygon.vertices[1], polygon.vertices[2],))
                self.writer.writeString("%d,%d,%d " % (polygon.vertices[0], polygon.vertices[2], polygon.vertices[3],))
        self.writer.writeLine('"')

        # Normals
        self.writer.writeString("Normals=" + '"')
        for polygon in mesh.polygons:
            if polygon.use_smooth:
                self.writer.writeString("n use smooth (lookup)")
            else:
                if len(polygon.vertices) == 3:
                    self.writer.writeString("%s,%s,%s " % (compactFloat(round(polygon.normal[0],6)), compactFloat(round(polygon.normal[1],6)), compactFloat(round(polygon.normal[2],6)),))
                elif len(polygon.vertices) == 4:
                    self.writer.writeString("%s,%s,%s " % (compactFloat(round(polygon.normal[0],6)), compactFloat(round(polygon.normal[1],6)), compactFloat(round(polygon.normal[2],6)),))
                    self.writer.writeString("%s,%s,%s " % (compactFloat(round(polygon.normal[0],6)), compactFloat(round(polygon.normal[1],6)), compactFloat(round(polygon.normal[2],6)),))
        self.writer.writeLine('"')

        #self.writer.writeString("\n")
        #for loop in mesh.loops:
        #    self.writer.writeString("l %f" % (loop.vertex_index))

    def writeScene(self, file):
        for item in bpy.context.scene.objects:
            if item.type == 'MESH':
                self.writeMesh(item)
            elif item.type == 'LAMP':
                self.writeLamp(item)
            elif item.type == 'CAMERA':
                self.writeCamera(item)

        file.write(self.writer.toString())

##########################################
# Main
##########################################

def export(filename, context):

    exporter = XamlExporter()
    file = open(filename, 'w')
    try:
        exporter.writeScene(file)
    finally:
        file.flush()
        file.close()

    return True

##########################################
#  The Export Xaml Class
##########################################

from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty

class ExportXaml(bpy.types.Operator, ExportHelper):
    """Export scene to XAML"""
    bl_idname = "export.xaml"
    bl_label = "Export to XAML"
    filename_ext = ".xaml"

    #Draw
    #Poll

    def execute(self, context):
        filepath = self.filepath
        filepath = bpy.path.ensure_ext(filepath, self.filename_ext)
        exported = export(filepath, context)
        return {'FINISHED'}

##########################################
# REGISTER
##########################################

def menu_func(self, context):
    self.layout.operator(ExportXaml.bl_idname, text="XAML (.xaml)")

def register():
    bpy.utils.register_class(ExportXaml)
    bpy.types.TOPBAR_MT_file_export.append(menu_func)

def unregister():
    bpy.utils.unregister_class(ExportXaml)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func)

if __name__ == "__main__":
    register()

import codecs
import json
import pathlib
import sys
import os
from bl_ui.space_sequencer import selected_sequences_len
import bpy
import collections
from . tag_reader.readers.reader_factory import ReaderFactory
from . Texture import Texture
from . ImportCoating import ImportCoating

class ImportSettings:
    lod = -1
    mipmap = -1
    norm_signed = True
    def __init__(self):
        self.lod = -1
        self.mipmap = -1
        self.norm_signed = True
        
class ImportVisor(bpy.types.Operator):
    bl_idname = "infinite.infinitevisor"
    bl_label = "Import Halo Infinite MaterialVisorSwatch"
    bl_description = "Import .visormaterialswatch files as usable shaders"
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    use_modules: bpy.props.BoolProperty(default=False,name="use modules",options={"HIDDEN"})
    selected_only: bpy.props.BoolProperty(default=False, name= "Selected Objects Only", description= 'Only imports coatings to objects selected.')

    def grabvisornames(self, context):
        parse_mwvs_name = ReaderFactory.create_reader(self.filepath)
        if type(parse_mwvs_name) == type(None):
            return [('', '', '')]
        else:
            parse_mwvs_name.load()
            coatingnames = []
            for entry in range(parse_mwvs_name.tag_parse.rootTagInst.childs[0]['pattern_variants'].childrenCount):
                temp_palette = parse_mwvs_name.tag_parse.rootTagInst.childs[0]['pattern_variants'].childs[entry]
                parse_mwvs_name.default_styles = entry
                parse_mwvs_name.toJsonNames()
                coatingnames.append((parse_mwvs_name.naming,parse_mwvs_name.palette,parse_mwvs_name.naming))
            return coatingnames
    def grabvisorcolor(self, context):
        parse_mwvs_name = ReaderFactory.create_reader(self.filepath)
        if type(parse_mwvs_name) == type(None):
            return [('', '', '')]
        else:
            parse_mwvs_name.load()
            coatingnames = []
            for entry in range(parse_mwvs_name.tag_parse.rootTagInst.childs[0]['color_variants'].childrenCount):
                temp_palette = parse_mwvs_name.tag_parse.rootTagInst.childs[0]['color_variants'].childs[entry]
                parse_mwvs_name.default_styles = entry
                parse_mwvs_name.toJsonColors()
                coatingnames.append((parse_mwvs_name.naming,parse_mwvs_name.naming,parse_mwvs_name.naming))
            return coatingnames

    coatingname: bpy.props.EnumProperty(items=grabvisornames, name = "Visor Pattern", description = "Visor Pattern To Import",)
    visorcolor: bpy.props.EnumProperty(items=grabvisorcolor, name = "Visor Color", description = "Visor Color To Import",)
    def execute(self, context):
        # Invoke nodes
        obj = ImportCoating(self)
        obj = ImportCoating.betteruvscaling(self)
        obj = ImportCoating.roughnessmath(self)
        obj = ImportCoating.HIMS(self)
        # Parse MaterialVisorSwatch
        parse_mwvs = ReaderFactory.create_reader(self.filepath)
        parse_mwvs.load()
        parse_mwvs.toJson(self.root_folder,self.coatingname)

        
        return {"FINISHED"}
    def invoke(self,context,event):
        self.addon_prefs = context.preferences.addons[__package__].preferences
        self.root_folder = self.addon_prefs.root_folder
        if not self.use_modules:
            context.window_manager.fileselect_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.execute(context)
            return {"FINISHED"}

##def menu_func(self,context):
##    self.layout.operator_context = 'INVOKE_DEFAULT'
##    self.layout.operator(ImportVisor.bl_idname,text="Halo Infinite Visor")

def register():
    print("loaded")
    bpy.utils.register_class(ImportVisor)
    bpy.types.TOPBAR_MT_file_import.append(menu_func)
    
def unregister():
    print("unloaded")
    bpy.utils.unregister_class(ImportVisor)

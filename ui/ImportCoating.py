import bpy
import bpy_extras
from bpy.props import BoolProperty, FloatProperty, StringProperty, EnumProperty
from ..tools import scene

class ImportCoating(bpy.types.Operator,bpy_extras.io_utils.ImportHelper):
    bl_idname = "infinite.infinitecoating"
    bl_label = "Halo Infinite Coating"
    bl_description = "Import .materialstyles files as usable shaders"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    filter_glob: StringProperty(default = "*.json",options = {'HIDDEN'})

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    materialuserpath: bpy.props.StringProperty(name = "Material Path", description = "Path To Use For .material",default = "M:\\objects\\")    
    selected_only: bpy.props.BoolProperty(default=False, name= "Selected Objects Only", description= 'Only imports coatings to objects selected')
    weighted_norms: bpy.props.BoolProperty(name="Weighted Normals/Clean Up",description="Merge by distance on all objects, and add Weighted Normals Modifier, also getting rid of invalid models",default=True)
    clean_up: bpy.props.BoolProperty(name="Purge Orphans",description="After each material, purge all orphans. Useful for long imports",default=True)
    use_crosscore: bpy.props.BoolProperty(default=False, name= "Cross Core", description= 'Removes style requirement to enable "cross core" coatings')
    use_damage: bpy.props.BoolProperty(default=False, name= "Zone 7 (Damage)", description= 'Enables Zone 7, used mostly for Damage/Dirt')
    move_UVs: bpy.props.BoolProperty(name="Move UVs",description="Moves UVs up by 1. If you are using a clean import, this is required",default=True)
    move_UV_by: bpy.props.IntProperty(name="Move Level",description="How far to move UVs",default=1)

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(icon = 'MATERIAL', text = "Settings")
        box.prop(self, "materialuserpath")

        box = layout.box()
        row = box.row()
        box.label(icon = 'MESH_CUBE', text = "Meshes")
        box.prop(self, "selected_only")
        box.prop(self, "weighted_norms")
        box.prop(self, "move_UVs")
        box.prop(self, "move_UV_by")
        
        box = layout.box()
        row = box.row()
        box.label(icon = 'ORPHAN_DATA', text = "Extras")
        box.prop(self, "use_crosscore")
        box.prop(self, "clean_up")
        box.prop(self, "use_damage")


    def execute(self, context):
        datasource = bpy.data.objects


        if self.selected_only: 
            datasource = bpy.context.selected_objects

        if self.weighted_norms: 
            for obj in datasource:
                if obj.type == 'MESH':
                    scene.weighted_norm(context,obj)
            scene.mergebydistance(context,obj)

        if self.move_UVs: 
            for obj in datasource:
                if obj.type == 'MESH':
                    scene.moveUVs(context,datasource,self.move_UV_by, obj)

        return {"FINISHED"}

    def invoke(self,context,event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
     

def draw_operator(self, context):
    self.layout.operator(ImportCoating.bl_idname)    

def register():
    bpy.utils.register_class(ImportCoating)
    bpy.types.TOPBAR_MT_file_import.append(draw_operator)
    
def unregister():
    bpy.utils.unregister_class(ImportCoating)
    bpy.types.TOPBAR_MT_file_import.remove(draw_operator)

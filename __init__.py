bl_info = {
    "name" : "Olympus",
    "blender" : (3,4,1),
    "version" : (0,7,0),
    "category" : "Import/Export",
    "description" : "Imports Models, Textures, BSPs and Coatings from Halo Infinite",
    "author" : "Surasia, Coreforge, Plastered_Crab, Urium86"
}
modulesNames = ["Header", "DataTable", "StringTable", "ContentTable", "renderModel", "ImportCoating"]

import sys
import bpy

class HaloInfiniteAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    print(__name__)

    root_folder: bpy.props.StringProperty(
        subtype="FILE_PATH",
        name="Asset Root",
        description="Path to use for additional data. Uses relative path from imported file if none is specified and import dependencies is active",
        default=""
    )

    shader_file: bpy.props.StringProperty(
        name="Shader library",
        description="Path to the blend file containing the shader",
        default=""
    )

    shader_name: bpy.props.StringProperty(
        name="Shader name",
        description="Name of the shader within the library",
        default=""
    )

    oodle_lib_path: bpy.props.StringProperty(
        subtype="FILE_PATH",
        name="Oodle Path",
        description="",
        default=""
    )

    module_deploy_path: bpy.props.StringProperty(
        subtype="DIR_PATH",
        name="Deploy Path",
        description="",
        default=""
    )

    ####################################
    # Global data
    # Mostly used for module support
    ####################################

    modules_resources = []
    modules_list_updated = False    # tells the panel to regenerate the tree view (doing so every draw would be stupid)

    def draw(self,context):
        layout = self.layout
        layout.label(text="Importer Preferences")
        layout.prop(self,"root_folder")


if 'DEBUG_MODE' in sys.argv:
    import renderModel
else:
    from . import renderModel
    from . import TextureOp
    from . import ImportCoating
    from . import ModulePanel
    from . import bsp

def register():
    bpy.utils.register_class(HaloInfiniteAddonPreferences)
    TextureOp.register()
    ImportCoating.register()
    renderModel.register()
    ModulePanel.register()
    bsp.register()
 
def unregister():
    bpy.utils.unregister_class(HaloInfiniteAddonPreferences)
    TextureOp.unregister()
    ImportCoating.unregister()
    renderModel.unregister()
    ModulePanel.unregister()
    bsp.unregister()
 
if __name__ == "__main__":
    register()

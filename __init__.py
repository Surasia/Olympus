import bpy
import sys
from .ui import ImportCoating

bl_info = {
    "name": "Olympus",
    "author": "Surasia",
    "version": (0, 0, 1),
    "blender": (3, 6, 0),
    "description": "Asset importer for Halo Infinite",
    "warning": "",
    "wiki_url": "https://github.com/Surasia/Olympus",
    "support": "COMMUNITY",
    "category": "Import-Export",
}


modulesNames = ["db", "tag_reader", "tools", "ui"]

class HaloInfiniteAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    root_folder: bpy.props.StringProperty(
        subtype="FILE_PATH",
        name="Asset Root",
        description="Path to use for additional data. Uses relative path from imported file if none is specified and import dependencies is active",
        default=""
    )
    def draw(self,context):
        layout = self.layout
        layout.prop(self,"root_folder")

def register():
    bpy.utils.register_class(HaloInfiniteAddonPreferences)
    ImportCoating.register()

def unregister():
    bpy.utils.unregister_class(HaloInfiniteAddonPreferences)
    ImportCoating.unregister()
    
if __name__ == "__main__":
    register()

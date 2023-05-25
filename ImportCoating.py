import codecs
import json
import pathlib
from pathlib import Path, PureWindowsPath
import sys
import os
from bl_ui.space_sequencer import selected_sequences_len
import bpy
import bpy_extras
from bpy.props import BoolProperty, FloatProperty, StringProperty, EnumProperty
import collections
from . Texture import Texture
from . Nodes import Nodes



class ImportSettings:
    def __init__(self):
        self.lod = -1
        self.mipmap = -1
        self.norm_signed = False
    
class Utilities:
    def moveUVs(context,datasource,move_UV_by, obj):
        for uv_layer in obj.data.uv_layers:
            for loop in obj.data.loops:
                uv_layer.data[loop.index].uv[1] += move_UV_by
    def weighted_norm(context,obj):
        obj.data.use_auto_smooth = True
        weighted_normal = obj.modifiers.new(name="Weighted Normal", type='WEIGHTED_NORMAL')
        weighted_normal.mode = 'FACE_AREA_WITH_ANGLE'
    def mergebydistance(context,obj):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles(threshold=0.0001)
        bpy.ops.object.mode_set(mode='OBJECT')

class GrabStrings:

    def grabvisornames(self, context):
        addon_prefs = context.preferences.addons[__package__].preferences
        root_folder = addon_prefs.root_folder
        with open("E:\OlympusDev\-1260457915_mwvs.json","r") as fff:
            visorstyle = json.load(fff)
        if type(fff) == type(None):
            return [('', '', '')]
        else:
            with open(os.path.dirname(__file__)+'/visorcolorIDs.json', 'r') as m:
                m = m.read()
                altnames = []
                colorIDs = json.loads(m)
                for altname in colorIDs:
                    name = altname['name']['value']
                    colorID = str(altname['colorID'])
                    visorID = str(altname['visorID'])
                    altnames.append((colorID, name, visorID))
            return altnames
            
class ImportCoating(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    bl_idname = "infinite.infinitecoating"
    bl_label = "Halo Infinite Coating"
    bl_description = "Import .materialstyles files as usable shaders"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    
    filename_ext = ".json"
    filter_glob: StringProperty(default = "*.json",options = {'HIDDEN'})

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    visor_selection: bpy.props.EnumProperty(items=GrabStrings.grabvisornames, name = "Visor",  description = "Visor To Import",)
    materialuserpath: bpy.props.StringProperty(name = "Material Path", description = "Path To Use For .material",default = "G:\\materials\\")    
    use_modules: bpy.props.BoolProperty(default=False,name="use modules",options={"HIDDEN"})
    mipmap: bpy.props.IntProperty(name="Mipmap level",description="Mipmap level of the textures to import",default=0,options={"HIDDEN"})
    norm_signed: bpy.props.BoolProperty(name="Signed Texture Range",description="import texures with a signed format as signed",default=False,options={"HIDDEN"})
    selected_only: bpy.props.BoolProperty(default=False, name= "Selected Objects Only", description= 'Only imports coatings to objects selected')
    import_visor: bpy.props.BoolProperty(name="Import Visor",description="Imports visor for multiplayer spartans",default=False)
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
        box.prop(self, "visor_selection")
        box.prop(self, "materialuserpath")

        box = layout.box()
        row = box.row()
        box.label(icon = 'TEXTURE', text = "Textures")
        box.prop(self, "mipmap")
        box.prop(self, "norm_signed")

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
        box.prop(self, "import_visor")
        box.prop(self, "use_crosscore")
        box.prop(self, "clean_up")
        box.prop(self, "use_damage")        
    # Textures have to be imported inside an operator, as otherwise data gets discarded..

    def readTexture(self, context, texturepath):
        number = texturepath
        texturepath = str(hex(number & (2**32 - 1))[2:])
        settings = ImportSettings()
        settings.mipmap = self.mipmap
        settings.norm_signed = self.norm_signed
        addon_prefs = context.preferences.addons[__package__].preferences
        self.root_folder = addon_prefs.root_folder.replace('\\', '/')
        self.textureroot = self.root_folder + 'bitm'
        self.texturepath = (str(self.textureroot + '/' + texturepath))
        texturename = texturepath.split('/')[-1] + '.png'

        # Check if texture already exists
        texture = bpy.data.images.get(texturename)
        if texture:
            img = texture
            return img

        # If texture doesn't exist, create a new one
        tex = Texture()
        textureData = tex.readTextureImage(self.texturepath, settings, self.use_modules)
        texture = bpy.data.textures.new(texturename, type="IMAGE")
        img = bpy.data.images.new(texturename, textureData[0], textureData[1])
        if textureData[2] is not None:
            img.pixels = textureData[2]
        tex.image = img
        img.pack()
        return img




    def execute(self, context):
        datasource = bpy.data.objects
        if self.selected_only: # Only use selected objects
            datasource = bpy.context.selected_objects
        if self.weighted_norms: # Apply Weighted Normal Modifier
            for obj in datasource:
                if obj.type == 'MESH':
                    Utilities.weighted_norm(context,obj)
            Utilities.mergebydistance(context,obj)
            if "invalid" in obj.name or "custom_shadow_cast" in obj.name:
                        bpy.data.objects.remove(context,obj, do_unlink=True)
        if self.move_UVs: # Move UVs
            for obj in datasource:
                    if obj.type == 'MESH':
                        Utilities.moveUVs(context,datasource,self.move_UV_by, obj)
        
        # Addon Initialize
        coating = open(self.filepath,'r')
        coating = json.load(coating)
        Nodes.betteruvscaling()
        Nodes.roughnessmath()
        Nodes.HIMS()
        # Style Parsing
        addon_prefs = context.preferences.addons[__package__].preferences
        self.root_folder = addon_prefs.root_folder.replace('\\', '/')
        grimeSwatch = coating["grimeSwatch"]
        grimeAmount = coating["grimeAmount"]
        scratchAmount = coating["scratchAmount"]
        for ob in datasource: 
            if ob.type == "MESH": 
                for mat_slot in ob.material_slots: 
                    if mat_slot.material.node_tree:
                        materialname = str(mat_slot.material.name)
                        if '.' in materialname: 
                            materialname = materialname.split('.',1)[0] 
                        for path in pathlib.Path(self.materialuserpath).rglob(materialname + '*_mat .json'): 
                            materialpath = str(path).replace(self.root_folder, '')
                            parse_mat = open(materialpath,'r')
                            parse_mat = json.load(parse_mat)
                            currentmaterial = parse_mat
                            if type(currentmaterial["style info"][0]) == type(None): # If material has no style, skip!
                                continue
                            else:
                                materialregion = currentmaterial.get("style info")[0]["region name"]["Value"]
                                materialstylename = currentmaterial.get("style info")[0]["material style"]["Value"]["Ref_id_int"]
                                materialstyleselection = coating['RootStyle']
                                normalmap = ""
                                mask0 = 7443
                                mask1 = 7443
                                asgtexture = ""
                                BaseScaleX = 0
                                BaseScaleY = 0
                                MaterialTransformX = 0
                                MaterialTransformY = 0
                                if self.use_crosscore: 
                                    materialstylename = materialstyleselection
                                if int(materialstylename) == int(materialstyleselection):
                                    matparams = currentmaterial['material parameters']
                                    for materialparameters in matparams: 
                                        if materialparameters['parameter name']['Value'] == 523899303: 
                                            BaseScaleX = materialparameters['real']['Value']
                                            BaseScaleY = materialparameters['vector']['Value']['X']
                                            MaterialTransformX = materialparameters['vector']['Value']['Y']
                                            MaterialTransformY = materialparameters['vector']['Value']['Z']
                                        elif materialparameters['parameter name']['Value'] == 2142563353:
                                            normalmap = materialparameters['bitmap']['Value']['Ref_id_int']
                                        elif materialparameters['parameter name']['Value'] == -447337164:
                                            asgtexture = materialparameters['bitmap']['Value']['Ref_id_int']
                                            print(asgtexture)
                                        elif materialparameters['parameter name']['Value'] == -1869712910:
                                            mask0 = materialparameters['bitmap']['Value']['Ref_id_int']
                                            mask1 = materialparameters['bitmap']['Value']['Ref_id_int']
                                        elif materialparameters['parameter name']['Value'] == -1677269129:
                                            mask1 = materialparameters['bitmap']['Value']['Ref_id_int']
                                    try:
                                        layers = coating["regionLayers"][str(materialregion)]["layers"]
                                    except:
                                        continue
                                    materialshader = coating["regionLayers"][str(materialregion)]["material"]
                                    
                                    node_tree0 = mat_slot.material.node_tree
                                    for node in node_tree0.nodes:
                                        node_tree0.nodes.remove(node)
                                    
                                    material_output_0 = node_tree0.nodes.new('ShaderNodeOutputMaterial')
                                    material_output_0.target = 'ALL'
                                    material_output_0.location = (675, 291)
                                    material_output_0.is_active_output = True

                                    # Apply ASG
                                    asg_texture = node_tree0.nodes.new('ShaderNodeTexImage')
                                    asg_texture.location = (-911, -136)
                                    texturepath = asgtexture
                                    asg_texture.image = self.readTexture(context,texturepath)
                                    asg_texture.image.colorspace_settings.name = 'Non-Color'
                                    asg_texture.label = 'ASG'
                                    asg_texture.interpolation = 'Cubic'

                                    # Mask0 Texture
                                    mask0_texture = node_tree0.nodes.new('ShaderNodeTexImage')
                                    mask0_texture.location = (-911, -422)
                                    texturepath = mask0
                                    mask0_texture.image = self.readTexture(context,texturepath)
                                    mask0_texture.image.colorspace_settings.name = 'Non-Color'
                                    mask0_texture.label = 'Mask 0'

                                    # Mask1 Texture
                                    mask1_texture = node_tree0.nodes.new('ShaderNodeTexImage')
                                    mask1_texture.location = (-911, -708)
                                    texturepath = mask1
                                    mask1_texture.image = self.readTexture(context,texturepath)
                                    mask1_texture.image.colorspace_settings.name = 'Non-Color'
                                    mask1_texture.label = 'Mask 1'

                                    # Normal Map
                                    normal_texture = node_tree0.nodes.new('ShaderNodeTexImage')
                                    normal_texture.location = (-911, -994)
                                    texturepath = normalmap
                                    normal_texture.image = self.readTexture(context,texturepath)
                                    normal_texture.image.colorspace_settings.name = 'Non-Color'
                                    normal_texture.label = 'Normal Map'
                                    width, height = normal_texture.image.size
                                    
                                    # HIMS initialize
                                    infiniteshader = node_tree0.nodes.new('ShaderNodeGroup')
                                    infiniteshader.node_tree = bpy.data.node_groups.get('HIMS 2.8 by Average Goat Enthusiast/ChromaCore')
                                    infiniteshader.location = (177, 267)
                                    infiniteshader.width = 400
                                    
                                    # Plug textures into reroutes
                                    reroute_002_0 = node_tree0.nodes.new('NodeReroute')
                                    reroute_002_0.location = (-592, -456)
                                    reroute_004_0 = node_tree0.nodes.new('NodeReroute')
                                    reroute_004_0.location = (-563, -743)
                                    reroute_006_0 = node_tree0.nodes.new('NodeReroute')
                                    reroute_006_0.location = (-534, -1029)
                                    reroute_0 = node_tree0.nodes.new('NodeReroute')
                                    reroute_0.location = (-616, -171)
                                    reroute_003_0 = node_tree0.nodes.new('NodeReroute')
                                    reroute_003_0.location = (-592, -72)
                                    reroute_008_0 = node_tree0.nodes.new('NodeReroute')
                                    reroute_008_0.location = (-534, -112)
                                    reroute_005_0 = node_tree0.nodes.new('NodeReroute')
                                    reroute_005_0.location = (-563, -92)
                                    reroute_001_0 = node_tree0.nodes.new('NodeReroute')
                                    reroute_001_0.location = (-616, -48)
                                try:
                                    if width != 1:
                                        node_tree0.links.new(reroute_008_0.outputs[0], infiniteshader.inputs[3])
                                    else:
                                        infiniteshader.inputs[3].default_value = (0.5, 0.5, 1.0, 1.0)
                                except:
                                    continue
                                # Reroute to Shader
                                node_tree0.links.new(reroute_001_0.outputs[0], infiniteshader.inputs[0])
                                node_tree0.links.new(reroute_003_0.outputs[0], infiniteshader.inputs[1])
                                node_tree0.links.new(reroute_005_0.outputs[0], infiniteshader.inputs[2])
                                node_tree0.links.new(reroute_0.outputs[0], reroute_001_0.inputs[0])
                                node_tree0.links.new(reroute_002_0.outputs[0], reroute_003_0.inputs[0])
                                node_tree0.links.new(reroute_004_0.outputs[0], reroute_005_0.inputs[0])
                                node_tree0.links.new(reroute_006_0.outputs[0], reroute_008_0.inputs[0])
                                node_tree0.links.new(asg_texture.outputs[0], reroute_0.inputs[0])
                                node_tree0.links.new(mask0_texture.outputs[0], reroute_002_0.inputs[0])
                                node_tree0.links.new(mask1_texture.outputs[0], reroute_004_0.inputs[0])
                                node_tree0.links.new(normal_texture.outputs[0], reroute_006_0.inputs[0])

                                # Set AO amount, grime amount, etc.
                                infiniteshader.inputs[4].default_value = 1
                                infiniteshader.inputs[5].default_value = grimeAmount
                                infiniteshader.inputs[6].default_value = 1
                                infiniteshader.inputs[8].default_value = 1
                                infiniteshader.inputs[7].default_value = 2
                                infiniteshader.inputs[9].default_value = 1
                                infiniteshader.inputs[10].default_value = 0

                                # Initialize swatch import
                                node_tree0.links.new(infiniteshader.outputs[0], material_output_0.inputs[0])
                                isGrimeDone = False
                                self.swwww = 0

                                for swatch in layers:
                                    swatchnum = str(swatch.get("swatch"))
                                    try:
                                        if swatchnum == '0':
                                            swatchnum = coating["regionLayers"][str(materialregion)]["layers"][0]
                                    except:
                                        continue
                                    for item in coating["swatches"]:
                                        EmissiveAmount = item.get("emissiveAmount")
                                        BotColor = item.get("colorVariant").get("gradient_bottom_color")
                                        MidColor = item.get("colorVariant").get("gradient_mid_color")
                                        TopColor = item.get("colorVariant").get("gradient_top_color")
                                        ScratchColor = item.get("scratchColor")
                                        ScratchMetallic = item.get("scratchMetallic")
                                        ScratchRoughness = item.get("scratchRoughness")
                                        Metallic = item.get("metallic")
                                        Roughness = item.get("roughness")
                                        RoughnessBlack = item.get("roughnessBlack")
                                        RoughnessWhite = item.get("roughnessWhite")
                                        NormalPath = item.get("normalPath")
                                        NormalScale = item.get("normalTextureTransform")
                                        ColorGradientScale = item.get("color_and_roughness_texture_transform")
                                        ColorGradientMap = item.get("colorGradientMap")
                                        swatchID = str(item.get("swatchId"))
                                        swatchRef = str(item.get("swatchref"))
                                        # if self.import_visor:
                                            # if materialregion == '1420626520':
                                                # if not swatchID == grimeSwatch:
                                                    # mappednames = GrabStrings.grabvisornames(self,context)
                                                    # for visor in range(len(mappednames)):
                                                        # visorID = mappednames[visor][2]
                                                        # colorID = mappednames[visor][0]
                                                        # if colorID == self.visor_selection:
                                                            # with open("E:\OlympusDev\-1260457915_mwvs.json","r") as hmmm:
                                                                # parse_mvsw = json.load(hmm)
                                                            # root = parse_mvsw['pattern_variants']
                                                            # EmissiveAmount = root['emissiveAmount']
                                                            # BotColor = parse_mvsw.bot
                                                            # MidColor = parse_mvsw.mid
                                                            # TopColor = parse_mvsw.top
                                                            # ScratchColor = root['scratchColor']
                                                            # ScratchMetallic = root['scratchMetallic']
                                                            # ScratchRoughness = root['scratchRoughness']
                                                            # Metallic = root['metallic']    
                                                            # Roughness = root['roughness']
                                                            # RoughnessBlack = root['roughnessBlack']
                                                            # RoughnessWhite = root['roughnessWhite']
                                                            # NormalPath = root['normalPath']
                                                            # NormalScale = root['normalTextureTransform']
                                                            # ColorGradientScale  = root['colorAndRoughnessTextureTransform']
                                                            # ColorGradientMap = root['colorGradientMap']
                                                            # swatchID = swref[item].get('swatchId')
                                                            # swatchref = str(root['swatchref'])
                                        def createSwatch(isGrime):
                                            node_tree1 = bpy.data.node_groups.new(swatchRef+'_swatch', 'ShaderNodeTree')

                                            # Swatch Inputs
                                            node_tree1.inputs.new('NodeSocketFloat', 'Base-Scale_X')
                                            node_tree1.inputs.new('NodeSocketFloat', 'Base-Scale_Y')
                                            node_tree1.inputs.new('NodeSocketFloat', 'Gradient-Scale_X')
                                            node_tree1.inputs.new('NodeSocketFloat', 'Gradient-Scale_Y')
                                            node_tree1.inputs.new('NodeSocketFloat', 'Normal-Scale_X')
                                            node_tree1.inputs.new('NodeSocketFloat', 'Normal-Scale_Y')
                                            node_tree1.inputs.new('NodeSocketFloat', 'Material Transform X')
                                            node_tree1.inputs.new('NodeSocketFloat', 'Material Transform Y')
                                            node_tree1.inputs.new('NodeSocketFloat', 'Roughness')
                                            node_tree1.inputs.new('NodeSocketFloat', 'Roughness Black')
                                            node_tree1.inputs.new('NodeSocketFloat', 'Roughness White')

                                            # Swatch Outputs
                                            node_tree1.outputs.new('NodeSocketFloat', 'Gradient Out')
                                            node_tree1.outputs.new('NodeSocketFloat', 'Rough Out')
                                            node_tree1.outputs.new('NodeSocketColor', 'Norm Out')

                                            group_002_0 = node_tree0.nodes.new('ShaderNodeGroup')
                                            group_002_0.node_tree = bpy.data.node_groups.get(swatchRef+'_swatch')
                                            group_002_0.color = (MidColor["R_value"], MidColor["G_value"], MidColor["B_value"])
                                            group_002_0.hide = True
                                            locationX = -150
                                            locationY = -628 + -352 * (self.swwww - 1)
                                            if self.swwww == 0:
                                                locationY = -297
                                            if isGrime:
                                                locationY = -2739
                                            group_002_0.location = (locationX, locationY)
                                            group_002_0.name = swatchRef+'_swatch'
                                            group_002_0.use_custom_color = True
                                            group_002_0.width = 250

                                            group_002_0.inputs[0].default_value = BaseScaleX
                                            group_002_0.inputs[1].default_value = BaseScaleY
                                            group_002_0.inputs[2].default_value = ColorGradientScale["X"]
                                            group_002_0.inputs[3].default_value = ColorGradientScale["Y"]
                                            group_002_0.inputs[4].default_value = NormalScale["X"]
                                            group_002_0.inputs[5].default_value = NormalScale["Y"]
                                            group_002_0.inputs[6].default_value = MaterialTransformX
                                            group_002_0.inputs[7].default_value = MaterialTransformY
                                            group_002_0.inputs[8].default_value = Roughness
                                            group_002_0.inputs[9].default_value = RoughnessBlack
                                            group_002_0.inputs[10].default_value = RoughnessWhite
                                            group_002_0.outputs[0].default_value = 1.0
                                            group_002_0.outputs[1].default_value = 0.0
                                            group_002_0.outputs[2].default_value = (0.5, 0.5, 1.0, 1.0)
                                            group_input_1 = node_tree1.nodes.new('NodeGroupInput')
                                            group_input_1.location = (-1000, -0.0)

                                            group_output_1 = node_tree1.nodes.new('NodeGroupOutput')
                                            group_output_1.location = (1000, 0.0)

                                            swatch_normal = node_tree1.nodes.new('ShaderNodeTexImage')
                                            swatch_normal.location = (0.0, 0.0)
                                            texturepath = NormalPath
                                            swatch_normal.image = self.readTexture(context,texturepath)
                                            swatch_normal.image.colorspace_settings.name = 'Non-Color'
                                            swatch_normal.label = 'Swatch Normal'
                                            width, height = swatch_normal.image.size

                                            swatch_gradient = node_tree1.nodes.new('ShaderNodeTexImage')
                                            swatch_gradient.location = (0.0, 300.0)
                                            texturepath = ColorGradientMap
                                            swatch_gradient.image = self.readTexture(context,texturepath)
                                            swatch_gradient.image.colorspace_settings.name = 'Non-Color'
                                            swatch_gradient.label = 'Swatch Gradient'



                                            # Better UV Scaling for Gradient
                                            group_002_1 = node_tree1.nodes.new('ShaderNodeGroup')
                                            group_002_1.node_tree = bpy.data.node_groups.get('BetterUVScaling')
                                            group_002_1.location = (-375, -9)
                                            group_002_1.name = 'Better UV Scaling'
                                            group_002_1.width = 200

                                            group_002_1.inputs[0].name = 'Base_Scale_X'
                                            group_002_1.inputs[1].name = 'Base_Scale_Y'
                                            group_002_1.inputs[2].name = 'Detail_Scale_X'
                                            group_002_1.inputs[3].name = 'Detail_Scale_Y'
                                            group_002_1.inputs[4].name = 'Alternative Transform X'
                                            group_002_1.inputs[5].name = 'Alternative Transform Y'
                                            group_002_1.outputs[0].name = 'Finalized Scale'

                                            node_tree1.links.new(group_input_1.outputs[0], group_002_1.inputs[0])
                                            node_tree1.links.new(group_input_1.outputs[1], group_002_1.inputs[1])
                                            node_tree1.links.new(group_input_1.outputs[2], group_002_1.inputs[2])
                                            node_tree1.links.new(group_input_1.outputs[3], group_002_1.inputs[3])
                                            node_tree1.links.new(group_input_1.outputs[6], group_002_1.inputs[4])
                                            node_tree1.links.new(group_input_1.outputs[7], group_002_1.inputs[5])
                                            node_tree1.links.new(group_002_1.outputs[0], swatch_gradient.inputs[0])

                                            # Better UV Scaling for Normal
                                            group_002_2 = node_tree1.nodes.new('ShaderNodeGroup')
                                            group_002_2.node_tree = bpy.data.node_groups.get('BetterUVScaling')
                                            group_002_2.location = (-375, -300)
                                            group_002_2.name = 'Better UV Scaling'
                                            group_002_2.width = 200

                                            group_002_2.inputs[0].name = 'Base_Scale_X'
                                            group_002_2.inputs[1].name = 'Base_Scale_Y'
                                            group_002_2.inputs[2].name = 'Detail_Scale_X'
                                            group_002_2.inputs[3].name = 'Detail_Scale_Y'
                                            group_002_2.inputs[4].name = 'Alternative Transform X'
                                            group_002_2.inputs[5].name = 'Alternative Transform Y'
                                            group_002_2.outputs[0].name = 'Finalized Scale'

                                            node_tree1.links.new(group_input_1.outputs[0], group_002_2.inputs[0])
                                            node_tree1.links.new(group_input_1.outputs[1], group_002_2.inputs[1])
                                            node_tree1.links.new(group_input_1.outputs[4], group_002_2.inputs[2])
                                            node_tree1.links.new(group_input_1.outputs[5], group_002_2.inputs[3])
                                            node_tree1.links.new(group_input_1.outputs[6], group_002_2.inputs[4])
                                            node_tree1.links.new(group_input_1.outputs[7], group_002_2.inputs[5])
                                            node_tree1.links.new(group_002_2.outputs[0], swatch_normal.inputs[0])

                                            # Separate Gradient and link to Output

                                            separate_rgb_1 = node_tree1.nodes.new('ShaderNodeSeparateColor')
                                            separate_rgb_1.mode = 'RGB'
                                            separate_rgb_1.location = (418, 294)

                                            node_tree1.links.new(swatch_gradient.outputs[0], separate_rgb_1.inputs[0])
                                            node_tree1.links.new(separate_rgb_1.outputs[0], group_output_1.inputs[0])
                                            

                                            # Roughness Math Instance

                                            group_1 = node_tree1.nodes.new('ShaderNodeGroup')
                                            group_1.node_tree = bpy.data.node_groups.get('Roughness Math')
                                            group_1.location = (772, -157)
                                            group_1.name = 'Group'
                                            group_1.width = 140.0
                                            
                                            group_1.inputs[0].name = 'Base'
                                            group_1.inputs[1].name = 'Exponent'
                                            group_1.inputs[2].name = 'Roughness Black'
                                            group_1.inputs[3].name = 'Roughness White'
                                            group_1.outputs[0].name = 'Color'

                                            # Roughness Math Links

                                            node_tree1.links.new(separate_rgb_1.outputs[2], group_1.inputs[0])
                                            node_tree1.links.new(group_input_1.outputs[8], group_1.inputs[1])
                                            node_tree1.links.new(group_input_1.outputs[9], group_1.inputs[2])
                                            node_tree1.links.new(group_input_1.outputs[10], group_1.inputs[3])
                                            node_tree1.links.new(group_1.outputs[0], group_output_1.inputs[1])
                                            if not isGrime:
                                                inputnum = 10+16*int(self.swwww)
                                                inputnum1 = 11+16*int(self.swwww)
                                                inputnum2 = 12+16*int(self.swwww)
                                                inputnuminit = 13+16*int(self.swwww)
                                                if self.swwww == 0:
                                                    inputnum = 11
                                                    inputnum1 = 12
                                                    inputnum2 = 13
                                                inputnum3 = 14+16*int(self.swwww)
                                                inputnum4 = 15+16*int(self.swwww)
                                                inputnum5 = 16+16*int(self.swwww)
                                                inputnum6 = 17+16*int(self.swwww)
                                                inputnum7 = 18+16*int(self.swwww)
                                                inputnum8 = 19+16*int(self.swwww)
                                                inputnum9 = 20+16*int(self.swwww)
                                                inputnum10 = 21+16*int(self.swwww)
                                                inputnum11 = 22+16*int(self.swwww)
                                                inputnum12 = 23+16*int(self.swwww)
                                                inputnum13 = 24+16*int(self.swwww)
                                                inputnum14 = 25+16*int(self.swwww)
                                                
                                                node_tree0.links.new(group_002_0.outputs[2], infiniteshader.inputs[inputnum2])
                                                node_tree0.links.new(group_002_0.outputs[0], infiniteshader.inputs[inputnum])
                                                node_tree0.links.new(group_002_0.outputs[1], infiniteshader.inputs[inputnum1])
                                                infiniteshader.inputs[inputnum3].default_value = scratchAmount
                                                infiniteshader.inputs[inputnum5].default_value = ScratchRoughness
                                                infiniteshader.inputs[inputnum4].default_value = ScratchMetallic
                                                infiniteshader.inputs[inputnum6].default_value = Metallic
                                                infiniteshader.inputs[inputnum7].default_value = 0
                                                infiniteshader.inputs[inputnum8].default_value = 0                                                            
                                                infiniteshader.inputs[inputnum9].default_value = EmissiveAmount
                                                infiniteshader.inputs[inputnum10].default_value = (TopColor["R_value"],TopColor["G_value"],TopColor["B_value"],1.0)
                                                infiniteshader.inputs[inputnum11].default_value = (MidColor["R_value"],MidColor["G_value"],MidColor["B_value"],1.0)
                                                infiniteshader.inputs[inputnum12].default_value = (BotColor["R_value"],BotColor["G_value"],BotColor["B_value"],1.0)
                                                infiniteshader.inputs[inputnum13].default_value = (ScratchColor["R_value"],ScratchColor["G_value"],ScratchColor["B_value"],1.0)
                                                infiniteshader.inputs[inputnum14].default_value = (ScratchColor["R_value"],ScratchColor["G_value"],ScratchColor["B_value"],1.0)
                                                if width == 1 or height == 1:
                                                    group_output_1.inputs[2].default_value = (0.5, 0.5, 1.0, 1.0)
                                                else:
                                                    node_tree1.links.new(swatch_normal.outputs[0], group_output_1.inputs[2])
                                                if self.swwww > 0:
                                                    infiniteshader.inputs[inputnuminit].default_value = 1
                                                if self.swwww == 6:
                                                    infiniteshader.inputs[inputnuminit].default_value = 0
                                                infiniteshader.inputs[109].default_value = int(self.use_damage)
                                                if materialshader == 1:
                                                    infiniteshader.inputs[61].default_value = int(self.use_damage)
                                                if ColorGradientMap == '7443':
                                                    try:
                                                        infiniteshader.inputs[inputnuminit].default_value = 0
                                                    except:
                                                        print('')
                                                
                                            if isGrime:
                                                node_tree0.links.new(group_002_0.outputs[0], infiniteshader.inputs[122])
                                                node_tree0.links.new(group_002_0.outputs[1], infiniteshader.inputs[123])
                                                node_tree0.links.new(group_002_0.outputs[2], infiniteshader.inputs[124])
                                                infiniteshader.inputs[125].default_value = Metallic
                                                infiniteshader.inputs[126].default_value = 0
                                                infiniteshader.inputs[127].default_value = 0
                                                infiniteshader.inputs[128].default_value = EmissiveAmount
                                                infiniteshader.inputs[129].default_value = (TopColor["R_value"],TopColor["G_value"],TopColor["B_value"],1.0)
                                                infiniteshader.inputs[130].default_value = (MidColor["R_value"],MidColor["G_value"],MidColor["B_value"],1.0)
                                                infiniteshader.inputs[131].default_value = (BotColor["R_value"],BotColor["G_value"],BotColor["B_value"],1.0)
                                                infiniteshader.inputs[132].default_value = (BotColor["R_value"],BotColor["G_value"],BotColor["B_value"],1.0)
                                                if width == 1 or height == 1:
                                                    group_output_1.inputs[2].default_value = (0.5, 0.5, 1.0, 1.0)
                                                else:
                                                    node_tree1.links.new(swatch_normal.outputs[0], group_output_1.inputs[2])
                                        if swatchnum == swatchID:
                                            isGrime = False
                                            createSwatch(isGrime)
                                            self.swwww = self.swwww + 1

                                        if swatchID == str(grimeSwatch):
                                            if not isGrimeDone:
                                                isGrime = True
                                                createSwatch(isGrime)
                                                isGrimeDone = True

                                    if self.clean_up:
                                        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

                                    if materialshader == 1:
                                        infiniteshader.inputs[77].default_value = 0
                                        infiniteshader.inputs[93].default_value = 0
                                        infiniteshader.inputs[109].default_value = 0

                    
            
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        print('')
        print('''
                            .,:clooxkO00KK0OOxol:^.              
                          ^:lllccc;,,,^,,,;;cldOKXKOdc^           
                       .;ol;^^^^..             .,cx0XX0x:.        
                     .:oc...,^.                    ^lOXXKkc.      
                    ^ol. .,^                         .l0XXKk,     
                   ;d; .,,.                            ^xKXXKl.   
                  :o^ .;^                               .lKXXKd.  
                 ;d^ .,^                                  cKXKKd. 
                .o;  ^;                                   .oKXXKl 
                co. .;.                                    .kXXX0;
                o:  ^;.                                     cKXXXo
                d,  ^,                                      ^OXKXk
                o^  ^^                                      .xXKXO
                o,  ^,                                      .dXKXO
                c:  .;.                   .^^.              .xXKXO
                ^:. .;^         ...  .,:dxkOKOd;.           ^OXKXd
                 ;,  .;.     ...ckOxoxO0KXK00KXXOdc;.       :KXX0:
                 .;^  ^:,....,::o0XXKOKXXXOokXXXKKXKkc^.   .xXKXd.
                  .,^,:l:..  .;:,^;;^.;lxO:.:0X0xOX00KKkl,^oKXXk. 
                     ..                 ...  :KkoOX00KKXXK0KXXk^  
                                              cl^;cx0XXXXXXXKx.   
                                               .    ^lkKXXXOc.    
                                                     .oKXOl.      
                                                   ,oOOd;.        
                                               .^:ool;.           
                                              .;:;.
            ''')
        print('                 Thanks for Using Olympus! Support: https://discord.gg/haloarchive')
        print('')
        
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

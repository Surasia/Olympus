from . base_template import BaseTemplate
from .. tag_instance import TagInstance


class Mwsw(BaseTemplate):

    def __init__(self, filename):
        super().__init__(filename, 'mwsw')
        self.default_color_variant = ""
        self.json_str_base = '{"emissiveAmount": 0.0,\
                              "scratchRoughness": 0.0,\
                              "scratchBrightness": 0.0,\
                              "ior": 0.0,\
                              "colorVariant": {\
                                  "botColor": [],\
                                  "topColor": [],\
                                  "midColor": []\
                              },\
                              "normalPath": "",\
                              "normalTextureTransform": [],\
                              "colorAndRoughnessTextureTransform": [],\
                              "scratchAlbedoTint": 0,\
                              "scratchColor": [],\
                              "metallic": 0.0,\
                              "scratchMetallic": 0.0,\
                              "roughnessBlack": 0.0,\
                              "colorVariantId": "",\
                              "scratchIor": 0.0,\
                              "roughnessWhite": 0.0,\
                              "roughness": 0.0,\
                              "groupName": "",\
                              "emissiveIntensity": 0.0,\
                              "colorGradientMap": "",\
                              "swatchId": ""\
                              }'

    def toJson(self):
        print('is it loading?')
        super().toJson()
        root = self.tag_parse.rootTagInst.childs[0]
        color_variant = None
        json_color_variants = root['color_variants'].toJson()
        color_v_index = -1
        for i, color in enumerate(root['color_variants'].childs):
            if color['name'].value == self.default_color_variant:
                color_variant = color
                color_v_index = i
                break
        if color_variant is None:
            color_variant = root['color_variants'].childs[0]
            color_v_index = 0
        try:
            self.handle = root['global tag ID'].value
        except:
            self.handle = '00000000'
        self.json_base["default_color_variant_index"] = color_v_index
        self.json_base["scratchRoughness"] = root['scratch_roughness'].value
        self.json_base["scratchBrightness"] = root['scratch_brightness'].value
        self.json_base["ior"] = root['ior'].value
        self.json_base["colorVariant"]["botColor"] = [color_variant['gradient_bottom_color'].r_value, color_variant['gradient_bottom_color'].g_value, color_variant['gradient_bottom_color'].b_value]
        self.json_base["colorVariant"]["topColor"] = [color_variant['gradient_top_color'].r_value, color_variant['gradient_top_color'].g_value, color_variant['gradient_top_color'].b_value]
        self.json_base["colorVariant"]["midColor"] = [color_variant['gradient_mid_color'].r_value, color_variant['gradient_mid_color'].g_value, color_variant['gradient_mid_color'].b_value]
        if not root['normal_detail_map'].ref_id_sub == 'ffffffff':
            self.json_base["normalPath"] = root['normal_detail_map'].ref_id_sub
        self.json_base["normalTextureTransform"] = [root['normalTextureTransform'].x,root['normalTextureTransform'].y]
        self.json_base["colorAndRoughnessTextureTransform"] = [root['colorAndRoughnessTextureTransform'].x,root['colorAndRoughnessTextureTransform'].y]
        self.json_base["scratchAlbedoTint"] = root['scratch_albedo_tint_spec'].value
        self.json_base["scratchColor"] = [root['scratch_color'].r_value,root['scratch_color'].g_value,root['scratch_color'].b_value]
        self.json_base["metallic"] = root['metallic'].value
        self.json_base["scratchMetallic"] = root['scratch_metallic'].value
        self.json_base["roughnessBlack"] = root['roughness_black'].value
        self.json_base["colorVariantId"] = color_variant['name'].value
        self.json_base["scratchIor"] = root['scratch_ior'].value
        self.json_base["roughnessWhite"] = root['roughness_white'].value
        if not root['colorGradientMap'].ref_id_sub == 'ffffffff':
            self.json_base["colorGradientMap"] = root['color_gradient_map'].ref_id_sub
        self.json_base["swatchref"] = self.handle
        self.json_base["swatchId"] = self.handle

    def onInstanceLoad(self, instance: TagInstance):
        super(Mwsw, self).onInstanceLoad(instance)



from .. tag_instance import TagInstance
from . base_template import BaseTemplate

class Material(BaseTemplate):

    def __init__(self, filepath):
        super().__init__(filepath, 'mat ')

    def load(self):
        super().load()
                     
    def toJson(self):
        super().toJson()
        if not type(self.tag_parse.rootTagInst) == type(None):
            root = self.tag_parse.rootTagInst.childs[0]
            matparams = []
            for entry in root['material parameters'].childs:
                lay_d = {}
                lay_d['ParameterName'] = entry['parameter name'].value
                if entry['parameter name'].value == '599E311A':
                    lay_d['ParameterName'] = 'cubemap'
                if entry['parameter name'].value == 'A7113A1F':
                    lay_d['ParameterName'] = 'texel_density'
                if entry['parameter name'].value == '19ECB47F':
                    lay_d['ParameterName'] = 'normal_map'
                if entry['parameter name'].value == 'F2718E90':
                    lay_d['ParameterName'] = 'mask_0'
                if entry['parameter name'].value == '77E7069C':
                    lay_d['ParameterName'] = 'mask_1'
                if entry['parameter name'].value == '342D56E5':
                    lay_d['ParameterName'] = 'asg_control'
                lay_d['BaseScaleX'] = entry['real'].value
                lay_d['BaseScaleY'] = entry['vector'].x
                lay_d['MaterialTransformX'] = entry['vector'].y
                lay_d['MaterialTransformY'] = entry['vector'].z
                lay_d['Bitmap'] = entry['bitmap'].ref_id_sub
                matparams.append(lay_d)
                self.json_base["MaterialParameters"] = matparams
                
            styleinfo = []
            for entry in root['style info'].childs:
                lay_a = {}
                lay_a['materialstyle'] = entry['material style'].ref_id_sub
                lay_a['region'] = entry['region name'].value
                styleinfo.append(lay_a)
                self.json_base["StyleInfo"] = styleinfo

            self.json_base["materialshader"] = root['material shader'].ref_id_sub
            if "skin" in root['material shader'].ref_id_sub:
                skinarray = []
                for textures in root['postprocess definition'].childs[0]['textures'].childs:
                    skin = {}
                    if 'color' in textures['bitmap reference'].path:
                        skin["color"] = textures['bitmap reference'].path
                    if 'normal' in textures['bitmap reference'].path and 'pore' not in textures['bitmap reference'].path:
                        skin["normal"] = textures['bitmap reference'].path
                    if 'pore' in textures['bitmap reference'].path:
                        skin["pore"] = textures['bitmap reference'].path
                    if 'aorotr' in textures['bitmap reference'].path:
                        skin["aorotr"] = textures['bitmap reference'].path
                    if 'aorstr' in textures['bitmap reference'].path:
                        skin["aorotr"] = textures['bitmap reference'].path
                    if 'sismpm' in textures['bitmap reference'].path:
                        skin["sismpm"] = textures['bitmap reference'].path
                    skinarray.append(skin)
                    self.json_base["skin"] = skinarray


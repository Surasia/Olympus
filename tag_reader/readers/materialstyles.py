
from . base_template import BaseTemplate
from . materialpalette import MaterialPalette
from . reader_factory import ReaderFactory
from .. var_names import Mmr3Hash_str, getStrInMmr3Hash
from ... import ImportCoating


class MaterialStyles(BaseTemplate):

    def __init__(self, filename):
        super().__init__(filename, 'mwsy')
        self.default_style = 0
        self.default_styles = 0
        self.name = ""
        self.done = False
        self.r_name = ""

    def toJsonNames(self):
        super().toJson()
        roots = self.tag_parse.rootTagInst.childs[0]
        style_selection = roots['style'].childs[self.default_styles]
        self.naming = style_selection['name'].value
        self.palette = style_selection['palette'].path.split('\\')[-1]

    def toJson(self, coatingname, root_folder):
        self.root_folder = root_folder
        self.done = False
        super().toJson()
        root = self.tag_parse.rootTagInst.childs[0]
        regions_names = []
        for entry in root['regions'].childs:
            regions_names.append(entry['name'].value)
        style_select = root['style'].childs[self.default_style]
        if style_select['name'].value == coatingname:
            self.json_base["grimeSwatch"] = style_select['grime_type'].value
            self.json_base["name"] = style_select['palette'].path.split('\\')[-1] + '_' + style_select['name'].value 
            self.json_base["emissiveAmount"] = style_select['emissive_amount'].value
            self.json_base["grimeAmount"] = style_select['grime_amount'].value
            self.json_base["scratchAmount"] = style_select['scratch_amount'].value
            parse_mwpl = ReaderFactory.create_reader(self.root_folder+style_select['palette'].path+".materialpalette") 
            parse_mwpl.load()
            parse_mwpl.toJson(self.root_folder)
            self.json_base["swatches"] = parse_mwpl.json_base['swatches']
            regionLayers = {}
            for entry in style_select['regions'].childs:
                layers = []
                for lay in entry['layers'].childs:
                    lay_d = {}
                    lay_d['colorBlend'] = bool(lay['Color_Blend'].selected_index)
                    lay_d['swatch'] = lay['name'].value
                    lay_d['ignoreTexelDensity'] = bool(lay['Ignore_Texel_Density_Scalar'].selected_index)
                    lay_d['normalBlend'] = bool(lay['Normal_Blend'].selected_index)
                    """
                    if lay_d['swatch'] == "00000000":
                        lay_d['swatch'] = ""
                    """
                    layers.append(lay_d)
                material = root['coatingMaterialSets'].childs[entry['Coating Material Set'].value]['coatingMaterialSet'].path
                material = material.split('\\')[-1]
                self.r_name = entry['name'].str_value
                regionLayers[self.r_name] = {"layers": layers,
                                            "material": material,
                                            "bodyPart": self.r_name,
                                            }

            self.json_base["regionLayers"] = regionLayers
            self.done = True
            
        #print(root)

    def onInstanceLoad(self, instance):
        super(MaterialStyles, self).onInstanceLoad(instance)


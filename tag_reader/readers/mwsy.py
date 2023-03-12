
from . base_template import BaseTemplate
from . mwpl import Mwpl
from . reader_factory import ReaderFactory
from .. var_names import Mmr3Hash_str, getStrInMmr3Hash, map_alt_name_id
from ... import ImportCoating


class Mwsy(BaseTemplate):

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
        self.naming = style_selection['name'].int_value
        self.naminghex = style_selection['palette'].ref_id_sub
        self.palette = style_selection['name'].value
        if map_alt_name_id.keys().__contains__(self.naming):
            self.palette = map_alt_name_id[self.naming]

    def toJson(self, coatingname, root_folder):
        self.root_folder = root_folder
        self.done = False
        super().toJson()
        root = self.tag_parse.rootTagInst.childs[0]
        regions_names = []
        for entry in root['regions'].childs:
            regions_names.append(entry['name'].value)
        style_select = root['style'].childs[self.default_style]
        if style_select['palette'].ref_id_sub == coatingname:
            print('W')
            self.json_base["grimeSwatch"] = style_select['grime_type'].value
            self.json_base["name"] = style_select['palette'].ref_id_center
            self.json_base["emissiveAmount"] = style_select['emissive_amount'].value
            self.json_base["grimeAmount"] = style_select['grime_amount'].value
            self.json_base["scratchAmount"] = style_select['scratch_amount'].value
            parse_mwpl = ReaderFactory.create_reader(self.root_folder+ 'mwpl/'+style_select['palette'].ref_id_sub)
            parse_mwpl.load()
            parse_mwpl.toJson(self.root_folder)
            print('palette loaded')
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
                    layers.append(lay_d)
                material = root['coatingMaterialSets'].childs[entry['Coating Material Set'].value]['coatingMaterialSet'].ref_id_sub
                self.r_name = entry['name'].str_value
                regionLayers[self.r_name] = {"layers": layers,
                                            "material": material,
                                            "bodyPart": self.r_name,
                                            }

            self.json_base["regionLayers"] = regionLayers
            self.done = True


    def onInstanceLoad(self, instance):
        super(Mwsy, self).onInstanceLoad(instance)


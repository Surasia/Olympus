from . base_template import BaseTemplate
from . reader_factory import ReaderFactory
from . swatch import Swatch
from ... import ImportCoating

class MaterialPalette(BaseTemplate):

    def __init__(self, filename):
        super().__init__(filename, 'mwpl')
        self.json_str_base = '{"swatches":[]}'

    def load(self):
        super().load()
        for i, key in enumerate(self.tag_parse.rootTagInst.childs[0]['swatches'].childs):
            key['swatch'].path = self.tag_parse.full_header.tag_reference_fixup_table.entries[i].str_path

    def getrootfolder(self):
        self.root_folder: rootfolder
    def toJson(self, root_folder):
        super().toJson()
        i = 0
        swatches = []
        for key in self.tag_parse.rootTagInst.childs[0]['swatches'].childs:
            parse_mwsw = ReaderFactory.create_reader(root_folder + key['swatch'].path+'.materialswatch')
            parse_mwsw.load()
            parse_mwsw.default_color_variant = key['color'].value
            parse_mwsw.toJson()
            parse_mwsw.json_base['swatchId'] = key['name'].value
            parse_mwsw.json_base['swatchref'] = parse_mwsw.handle
            parse_mwsw.json_base['emissiveAmount'] = key['emissiveAmount'].value
            parse_mwsw.json_base['emissiveIntensity'] = key['emissiveIntensity'].value
            parse_mwsw.json_base['roughness'] = key['roughnessOverride'].selected_index
            swatches.append(parse_mwsw.json_base)
        self.json_base['swatches'] = swatches
        empty_i = self.tag_parse.rootTagInst.childs[0]['Empty Swatch Index'].value
        assert self.tag_parse.rootTagInst.childs[0]['swatches'].childs[empty_i]['name'].value == '00000000'


    def onInstanceLoad(self, instance):
        super(MaterialPalette, self).onInstanceLoad(instance)

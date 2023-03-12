from . base_template import BaseTemplate
from . reader_factory import ReaderFactory
from . mwsw import Mwsw
from ... import ImportCoating
from .. var_names import Mmr3Hash_str, getMmr3HashFrom, map_alt_name_id,getMmr3HashFromInt
import json
import sys
import os

class Mwvs(BaseTemplate):

    def __init__(self, filename):
        super().__init__(filename, 'mwvs')

    def load(self):
        super().load()
    
    def toJson(self, root_folder, coatingname, colorname, index):
        root = self.tag_parse.rootTagInst.childs[0]
        super().toJson()
        self.json_base["botColor"] = {}
        self.json_base["topColor"] = {}
        self.json_base["midColor"] = {}
        for key in root['pattern_variants'].childs:
            path = key['visorPattern'].ref_id_sub
            name = key['name'].value
            if coatingname == name:
                print('hey')
                parse_mwsw = ReaderFactory.create_reader(root_folder + 'mwsw/' + path)
                parse_mwsw.load()
                parse_mwsw.toJson()
                self.json_base['pattern_variant'] = parse_mwsw.json_base
                with open(os.path.dirname(__file__)+'/visorcolorIDs.json', 'r') as m:
                    m = m.read()
                    colorIDs = json.loads(m)
                    ID = getMmr3HashFromInt(colorIDs['visors'][index]['colorID'])
                    Roughness = float(colorIDs['visors'][index]['Roughness'])
                    Emmissive = float(colorIDs['visors'][index]['Emmisive'])
                    self.json_base["pattern_variant"]["roughness"] = Roughness
                    self.json_base["pattern_variant"]["emissiveAmount"] = Emmissive
                    for keys in range(len(root["color_variants"].childs)):
                        name = root["color_variants"].childs[keys]['name'].value
                        rootc = root["color_variants"].childs[keys]
                        if name == ID:
                            self.bot = ((rootc['gradient_bottom_color'].r_value)), ((rootc['gradient_bottom_color'].g_value)), ((rootc['gradient_bottom_color'].b_value))
                            self.top = ((rootc['gradient_top_color'].r_value)), ((rootc['gradient_top_color'].g_value)), ((rootc['gradient_top_color'].b_value))
                            self.mid = ((rootc['gradient_mid_color'].r_value)),((rootc['gradient_mid_color'].g_value)), ((rootc['gradient_mid_color'].b_value))
                            continue


    def onInstanceLoad(self, instance):
        super(Mwvs, self).onInstanceLoad(instance)

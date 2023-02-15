from . base_template import BaseTemplate
from . reader_factory import ReaderFactory
from . swatch import Swatch
from ... import ImportCoating
import json
import os

class MpVisorSwatch(BaseTemplate):

    def __init__(self, filename):
        super().__init__(filename, 'mwvs')
        self.json_str_base = '{"pattern_variants":[]}'

    def load(self):
        super().load()

        
    def toJsonNames(self):
        super().toJson()
        roots = self.tag_parse.rootTagInst.childs[0]
        style_selection = roots['pattern_variants'].childs[self.default_styles]
        self.naming = style_selection['name'].value
        self.palette = style_selection['visorPattern'].path.split('\\')[-1]
    def toJsonColors(self):
        super().toJson()
        roots = self.tag_parse.rootTagInst.childs[0]
        style_selection = roots['color_variants'].childs[self.default_styles]
        self.naming = style_selection['name'].value
        path = os.path.realpath(os.path.dirname(__file__))
        pardir = os.path.abspath(os.path.join(path, os.pardir))

        
    def toJson(self, root_folder,coatingname):
        root = self.tag_parse.rootTagInst.childs[0]
        super().toJson()
        for key in root['pattern_variants'].childs:
            path = key['visorPattern'].path
            name = key['name'].value
            if coatingname == name:
                parse_mwsw = ReaderFactory.create_reader(root_folder + path + '.materialswatch')
                parse_mwsw.load()
                parse_mwsw.toJson()


                    


    def onInstanceLoad(self, instance):
        super(MpVisorSwatch, self).onInstanceLoad(instance)

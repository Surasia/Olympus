import os
import pathlib

from ... commons.tag_group_extension_map import map_ext
from . base_template import BaseTemplate


class Generic(BaseTemplate):
    def __init__(self, filename):
        self._loaded = True
        file_ext = os.path.splitext(filename)[1].replace('.','')
        tag_group = ''
        for key in map_ext.keys():
            if map_ext[key] == file_ext:
                tag_group = str(key)
                break

        if tag_group != '':
            super().__init__(filename, tag_group)

    def toJson(self, from_first_child=False):
        return super().toJson(True)

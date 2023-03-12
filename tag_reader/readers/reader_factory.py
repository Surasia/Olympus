import os
import pkgutil
import importlib

from ... commons.share_mem import parse_dict
from ... commons.tag_group_extension_map import map_ext
from . interfaces import IBaseTemplate
from . import generic
from pathlib import Path



class ReaderFactory:
    class_map = {
        'bitm': ('bitmap', 'Bitmap'),
        'bipd': ('biped', 'Biped'),
        'ocad': ('i343.ObjectCustomization.AttachmentConfiguration', 'AttachmentConfiguration'),
        'mat ': ('mat', 'Mat'),
        'mwpl': ('mwpl', 'Mwpl'),
        'mwsy': ('mwsy', 'Mwsy'),
        'hlmt': ('model', 'Model'),
        'unic': ('multilingual_unicode_string_list', 'MultilingualUnicodeStringList'),
        'mode': ('render_model', 'RenderModel'),
        'uslg': ('stringlist', 'StringList'),
        'mwsw': ('mwsw', 'Mwsw'),
        'shbc': ('shader_bytecode', 'ShaderBytecode'),
        'jmad': ('c_model_animation_graph', 'ModelAnimationGraph'),
        'mwvs': ('mwvs', 'Mwvs')
    }
    path_import = 'Olympus.tag_reader.readers'
    pluginname = 'swatch'


    def iter_namespace(ns_pkg):
        # Specifying the second argument (prefix) to iter_modules makes the
        # returned name an absolute name instead of a relative one. This allows
        # import_module to work without having to do additional modification to
        # the name.
        return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

    @staticmethod
    def create_reader(relative_path: str) -> IBaseTemplate:
        file_ext = os.path.basename(os.path.dirname(relative_path))
        tag_group = ''
        for key in map_ext.keys():
            if key == file_ext:
                tag_group = str(key)
                break
        path_import = 'Olympus.tag_reader.readers'
        pluginname = 'swatch'
        relative_path = relative_path.replace('\\', '/')
        #relative_path = relative_path.replace('/', '\\')
        if parse_dict.keys().__contains__(relative_path):
            return parse_dict[relative_path]
        if ReaderFactory.class_map.keys().__contains__(tag_group):
            pluginname = ReaderFactory.class_map[tag_group][0]
            plugin = importlib.import_module('{path}.{name}'.format(path=path_import, name=pluginname))
            temp_parse = eval(f'plugin.{ReaderFactory.class_map[tag_group][1]}("{relative_path}")')

        else:
            return

        parse_dict[relative_path] = temp_parse
        return temp_parse

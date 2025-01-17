import os

from ... commons.common_utils import resolvePathFile
from ... events import Event
from ... import ImportCoating
from . interfaces import IBaseTemplate

from .. tag_parse_control import TagParseControl
import json


class BaseTemplate(IBaseTemplate):

    def __init__(self, p_in_game_path, tagLayoutExt):
        self.tigger_event_on_parent = True
        self.EventOnInstanceLoad = Event()
        self.json_str_base = "{}"
        self.json_base = None
        self.in_game_path = p_in_game_path
        self.full_filepath = self.in_game_path
        self.tagLayoutExt = tagLayoutExt
        self.tag_parse = TagParseControl(self.full_filepath, self.tagLayoutExt)
        self.tag_parse.AddSubscribersForOnInstanceLoad(self.onInstanceLoad)
        self._loaded = False
        self.loading = False
        self.first_child = None
        self.load_recursive = False

    def load(self, force = False):
        self.loading = True
        if not self._loaded:
            self.tag_parse.readFile()
        else:
            if force:
                self.tag_parse.reset()
                self.tag_parse.readFile()

        self._loaded = True
        self.loading = False

        if self.tag_parse.rootTagInst is not None :
            if len(self.tag_parse.rootTagInst.childs) != 0:
                self.first_child = self.tag_parse.rootTagInst.childs[0]
            else:
                    print(f'len(self.tag_parse.rootTagInst.childs) == 0 in {self.full_filepath}')

    def getTagGroup(self):
        super(BaseTemplate, self).getTagGroup()
        return self.tagLayoutExt
        
    def readParameterByName(self, str_name):
        return self.tag_parse.readTagDefinitionByNamePathSelfAddress(str_name)

    def is_loaded(self):
        return self._loaded

    def toJson(self, from_first_child=False):
        if not from_first_child:
            self.json_base = json.loads(self.json_str_base)
        else:
            if self.first_child is None:
                return self.json_str_base

            self.json_str_base =json.dumps( self.tag_parse.rootTagInst.toJson())
            self.json_base = json.loads(self.json_str_base)
        return self.json_base

    def onInstanceLoad(self, instance):
        if self.load_recursive and instance.tagDef.T == 'TagRef':
            if instance.ref_id_int != -1 and instance.path == '':
                debug = True
            if instance.path != '' and instance.path is not None:
                path_full = instance.getInGamePath()
                if path_full == '' or not os.path.exists(path_full):
                    path_full = resolvePathFile(instance.path, instance.tagGroupRev).replace('','')
                    if path_full!= '' and not (path_full.__contains__('{') and path_full.__contains__('}')):
                        #print(f'No mapped but exist {path_full} ')
                        pass
                if path_full != '':
                    #print(path_full)
                    instance.parse = ReaderFactory.create_reader(path_full)
                    if not instance.parse.is_loaded() and not instance.parse.loading:
                        instance.parse.load_recursive = self.load_recursive
                        instance.parse.load()
                else:
                    debug = True
                    #print(f'Error missing file {instance.path }')
        if self.tigger_event_on_parent:
            self.EventOnInstanceLoad(instance)
        pass

    def AddSubForOnInstanceLoad(self, objMethod):
        self.EventOnInstanceLoad += objMethod

    def RemoveSubOnInstanceLoad(self, objMethod):
        self.EventOnInstanceLoad -= objMethod

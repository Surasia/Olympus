import json
import os
import sys
from classes import rucy


def getfromJSON():
    with open("D:/OlympusDev/tags/rucy/3F88B537.json",'r') as f:
        fs = json.load(f)
        Rucy = rucy.root.from_dict(fs)
        Swatch = rucy.Info.from_dict(Rucy.info) # type: ignore
        print(Swatch)

getfromJSON()
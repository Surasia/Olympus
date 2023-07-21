from dataclasses import dataclass, field
from .cmsw import CMSW
from typing import Any, Dict, List
import json

def gettag(data: Dict[str, Any]):
    value = data.get('Value', {})
    ref_id_str = value.get('Ref_id_str', '')
    TagGroupRev = value.get('TagGroupRev', '')
    try:
        with open(f"D:/OlympusDev/tags/{TagGroupRev}/{ref_id_str}.json",'r') as f:
            if TagGroupRev == "cmsw":
                return CMSW.from_dict(json.load(f))
            else:
                return json.load(f)
    except:
        return "{}"

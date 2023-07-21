from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin,config
import json
from typing import Any, Dict, List
import sqlite3
import os


@dataclass
class ValueField(DataClassJsonMixin):
    Value: Any
    AddressStart: int
    Offset: int
    InstOffset: int

def getvalue(v: Dict[str, Any]):
    return v.get('Value', {})

def value_field_to_bool(v: Dict[str, Any]):
    return v.get('Selected', 'disabled') == 'enabled'

def scratch_flag_to_bool(v: Dict[str, Any]):
    return v.get('Selected', 'Use Default Colors From Swatch') == 'Override Colors'

def color_variant(v: Dict[str, Any]):
    value_dict = v.get('Value', {})
    return [value_dict.get('R_value', 0), value_dict.get('G_value', 0), value_dict.get('B_value', 0)]

def vector(v: Dict[str, Any]):
    value_dict = v.get('Value', {})
    return [value_dict.get('X', 0), value_dict.get('Y', 0)]

def tagref(data: Dict[str, Any]):
    value = data.get('Value', {})
    ref_id_str = value.get('Ref_id_str', '')
    TagGroupRev = value.get('TagGroupRev', '')
    try:
        with open(f"D:/OlympusDev/tags/{TagGroupRev}/{ref_id_str}.json",'r') as f:
            if TagGroupRev == 'cmsw':
                swatch = cmsw.CMSW.from_dict(json.load(f))
                return swatch
            else:
                return json.load(f)
    except:
        return "{}"
    

def getrefid(data: Dict[str, Any]):
    value = data.get('Value', {})
    ref_id_str = value.get('Ref_id_str', '')
    TagGroupRev = value.get('TagGroupRev', '')
    return {TagGroupRev, ref_id_str}

def mmr3(mm3):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    db_path = os.path.join(script_dir, '..', '..', 'db', 'database.db')

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM StringMmh3LTU WHERE mmh3_id=?', (mm3,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result[1] if result else None

def getmmh3(v: Dict[str, Any]):
    return mmr3(v.get('Value', {}))

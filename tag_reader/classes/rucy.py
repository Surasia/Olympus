from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin,config
import json
from typing import Any, Dict, List
from .common import value_field_to_bool, scratch_flag_to_bool, color_variant, tagref, getvalue, getmmh3


"""

DATACLASSES FOR RUCY

"""

@dataclass
class Swatch(DataClassJsonMixin):
    elementID: int = field(metadata=config(decoder=getvalue))
    Description: str = field(metadata=config(decoder=getmmh3))
    Swatch: str = field(metadata=config(decoder=tagref))
    gradientColorFlag: bool = field(metadata=config(decoder=scratch_flag_to_bool))
    gradientTopColor: List[float] = field(metadata=config(decoder=color_variant))
    gradientMidColor: List[float] = field(metadata=config(decoder=color_variant))
    gradientBottomColor: List[float] = field(metadata=config(decoder=color_variant))
    roughnessOffset: float = field(metadata=config(decoder=getvalue))
    scratchColorFlag: bool = field(metadata=config(decoder=scratch_flag_to_bool))
    scratchColor: List[float] = field(metadata=config(decoder=color_variant))
    scratchRoughnessOffset: float = field(metadata=config(decoder=getvalue))
    useEmmissive: bool = field(metadata=config(field_name="Use Emissive?", decoder=value_field_to_bool))
    emissiveIntensity: float = field(metadata=config(decoder=getvalue))
    emissiveAmount: float = field(metadata=config(decoder=getvalue))
    useAlpha: bool = field(metadata=config(field_name="Use Alpha?", decoder=value_field_to_bool))
    useSubSurf: bool = field(metadata=config(field_name="Use Subsurface Scattering?", decoder=value_field_to_bool))    

@dataclass
class Intention(DataClassJsonMixin):
    name: str = field(metadata=config(decoder=getmmh3))
    info: Swatch

@dataclass
class Info(DataClassJsonMixin):
    globalDamageSwatch: Swatch
    heroDamageSwatch: Swatch
    globalEmissiveSwatch: Swatch
    emissiveAmount: float = field(metadata=config(decoder=getvalue))
    emissiveIntensity: float = field(metadata=config(decoder=getvalue))
    scratchAmount: float = field(metadata=config(decoder=getvalue))
    grimeSwatch: Swatch
    grimeAmount: float = field(metadata=config(decoder=getvalue))

@dataclass
class region(DataClassJsonMixin):
    name: str = field(metadata=config(decoder=getvalue))
    coatingMaterialOverride: str = field(metadata=config(decoder=getvalue))
    intentions: List[Intention]

@dataclass
class root(DataClassJsonMixin):
    info: Info
    regions: List[region]


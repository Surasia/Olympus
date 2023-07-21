from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin,config
from typing import List
from .common import vector, tagref, color_variant, getvalue, getrefid


"""

DATACLASSES FOR CMSW

"""

@dataclass
class CMSW(DataClassJsonMixin):
    colorAndRoughnessTextureTransform: List[float] = field(metadata=config(decoder=vector))
    colorGradientMap: str = field(metadata=config(decoder=getrefid))
    gradientTopColor: List[float] = field(metadata=config(decoder=color_variant))
    gradientMidColor: List[float] = field(metadata=config(decoder=color_variant))
    gradientBottomColor: List[float] = field(metadata=config(decoder=color_variant))
    roughnessWhite: float = field(metadata=config(decoder=getvalue))
    roughnessBlack: float = field(metadata=config(decoder=getvalue))
    normalDetailMap: str = field(metadata=config(decoder=getrefid))
    metallic: float = field(metadata=config(decoder=getvalue))
    scratchColor: List[float] = field(metadata=config(decoder=color_variant))
    scratchRoughness: float = field(metadata=config(decoder=getvalue))
    sssIntensity: float = field(metadata=config(decoder=getvalue))
    emissiveIntensity: float = field(metadata=config(decoder=getvalue))
    emissiveAmount: float = field(metadata=config(decoder=getvalue))

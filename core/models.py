from dataclasses import dataclass, field
from typing import Optional
from core.enums import DisabilityType, DisabilityLevel

@dataclass(frozen=True)
class UserInfo:
    """대상자 정보 모델"""
    name:str
    birth:str
    disability_type:DisabilityType
    disability_level = DisabilityLevel
    address : str
    id:Optional[int] = None

@dataclass
class WelfareService:
    """복지 서비스 정보 모델"""
    service_id : str
    service_name : str
    service_url : str
    summary : str
    department : str
    id : Optional[int] = None
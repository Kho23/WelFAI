from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UserInfo:
    """대상자 정보 모델"""
    name: str
    birth: str
    disability_type: str
    disability_level: str
    address: str
    id: Optional[int] = None

from dataclasses import dataclass
from typing import Optional


@dataclass
class WelfareService:
    """복지 서비스 정보 모델"""
    name: str
    service_url: str
    summary: str
    department: str
    target: str
    id: Optional[int] = None

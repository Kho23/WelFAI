from enum import Enum

class DisabilityType(Enum):
    PHYSICAL = "지체장애"
    VISUAL = "시각장애"
    HEARING = "청각장애"
    BRAIN = "뇌병변장애"
    INTELLECTUAL = "지적장애"
    AUTISM = "자폐성장애"
    ALL = "모든장애"

class DisabilityLevel(Enum):
    SEVERE = "심한 장애"
    MILD = "심하지 않은 장애"
    ALL = "모든정도"
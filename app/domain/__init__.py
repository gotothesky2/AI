"""
도메인 모델 패키지
데이터베이스 엔티티 클래스들을 포함합니다.
"""

from .User import User
from .Hmt import Hmt
from .Cst import Cst
from .entity.BaseEntity import BaseEntity
from .AiReport import AiReport
from .mock import *
from .report import *
from .University import University
from .UniversityMajor import UniversityMajor
from .Major import Major
from .Field import Field
from .OAuth import OAuth

__all__ = [
    "User",
    "Hmt",
    "Cst",
    "BaseEntity",
    "AiReport",
    "Mock",
    "MockScore",
    "Report",
    "ReportScore",
    "University",
    "UniversityMajor",
    "Major",
    "Field",
    "OAuth"
]



"""
도메인 모델 패키지
데이터베이스 엔티티 클래스들을 포함합니다.
"""

from .entity.BaseEntity import BaseEntity,Base
from .User import User
from .Hmt import Hmt
from .Cst import Cst
from .AiReport import AiReport
from .mockModule.Mock import Mock
from .mockModule.MockScore import MockScore
from .reportModule.Report import Report
from .reportModule.ReportScore import ReportScore
from .University import University
from .UniversityMajor import UniversityMajor
from .Major import Major
from .Field import Field
from .OAuth import OAuth
from .MajorBookmark import MajorBookmark

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
    "OAuth",
    "MajorBookmark"
]



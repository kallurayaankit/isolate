
"""Data model for isolate."""

from dataclasses import dataclass, field, asdict
from enum import Enum


class Verdict(str, Enum):
    ISOLATED = "isolated"
    ORDER_DEPENDENT = "order_dependent"
    POLLUTER = "polluter"
    BROKEN = "broken"


@dataclass
class Audit:
    test_id: str
    verdict: str = Verdict.ISOLATED.value
    reason: str = ""

    def to_dict(self):
        return asdict(self)


@dataclass
class Report:
    suite_count: int = 0
    isolated: int = 0
    order_dependent: int = 0
    polluter: int = 0
    broken: int = 0
    audits: list = field(default_factory=list)

    def to_dict(self):
        return {
            "suite_count": self.suite_count,
            "isolated": self.isolated,
            "order_dependent": self.order_dependent,
            "polluter": self.polluter,
            "broken": self.broken,
            "audits": [a.to_dict() for a in self.audits],
        }

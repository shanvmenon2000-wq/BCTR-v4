from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any


class ClosureType(str, Enum):
    TERMINAL = "terminal"
    FIXED_POINT = "fixed_point"
    CYCLE = "cycle"
    REGENERATIVE = "regenerative"
    UNKNOWN = "unknown"


class IState(str, Enum):
    I0 = "i0"
    I1 = "i1"
    I2 = "i2"
    I3 = "i3"
    I4 = "i4"


MATRIX_FIELDS = [
    "definition",
    "entry_anchor",
    "invariant",
    "transformer",
    "canceler",
    "repetition",
    "measure",
    "minimal_form",
    "opposite",
    "hidden_ladder",
    "intuition_break",
    "debt_source",
    "first_tail",
    "reconstructable",
    "returnable",
    "teaches",
    "compresses",
    "infrastructure",
]


@dataclass
class MatrixAnswer:
    field: str
    score: float
    evidence: str = ""

    def validate(self) -> None:
        if self.field not in MATRIX_FIELDS:
            raise ValueError(f"Unknown matrix field: {self.field}")
        if self.score not in (0, 0.5, 1):
            raise ValueError(f"Matrix score must be 0, 0.5, or 1 for {self.field}")


@dataclass
class BCTRObject:
    object_id: str
    label: str
    matrix: Dict[str, float]
    closure_type: ClosureType = ClosureType.UNKNOWN
    tails: List[str] = field(default_factory=list)
    tail_weights: Dict[str, float] = field(default_factory=dict)
    evidence: Dict[str, str] = field(default_factory=dict)
    status: str = "seed_estimate"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BCTRObject":
        return cls(
            object_id=data["object_id"],
            label=data["label"],
            matrix=data.get("matrix", {}),
            closure_type=ClosureType(data.get("closure_type", "unknown")),
            tails=data.get("tails", []),
            tail_weights=data.get("tail_weights", {}),
            evidence=data.get("evidence", {}),
            status=data.get("status", "seed_estimate"),
        )


@dataclass
class LearnerObjectState:
    agent_id: str
    object_id: str
    required_crossings: int
    paid_crossings: int
    unpaid_crossing_weights: List[float] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LearnerObjectState":
        return cls(
            agent_id=data["agent_id"],
            object_id=data["object_id"],
            required_crossings=int(data.get("required_crossings", 0)),
            paid_crossings=int(data.get("paid_crossings", 0)),
            unpaid_crossing_weights=[float(x) for x in data.get("unpaid_crossing_weights", [])],
        )


@dataclass
class Packet:
    packet_id: str
    label: str
    crossings_paid: List[str] = field(default_factory=list)
    crossing_weights: List[float] = field(default_factory=list)
    debt_type: str = "mixed"
    status: str = "draft"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Packet":
        return cls(
            packet_id=data["packet_id"],
            label=data.get("label", data["packet_id"]),
            crossings_paid=data.get("crossings_paid", []),
            crossing_weights=[float(x) for x in data.get("crossing_weights", [])],
            debt_type=data.get("debt_type", "mixed"),
            status=data.get("status", "draft"),
        )


@dataclass
class Rung:
    rung_id: str
    from_object: str
    to_object: str
    i4_anchor_values: List[float] = field(default_factory=list)
    new_i0_object_weights: List[float] = field(default_factory=list)
    selected_packet_capacities: List[float] = field(default_factory=list)
    has_return_test: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Rung":
        return cls(
            rung_id=data["rung_id"],
            from_object=data["from_object"],
            to_object=data["to_object"],
            i4_anchor_values=[float(x) for x in data.get("i4_anchor_values", [])],
            new_i0_object_weights=[float(x) for x in data.get("new_i0_object_weights", [])],
            selected_packet_capacities=[float(x) for x in data.get("selected_packet_capacities", [])],
            has_return_test=bool(data.get("has_return_test", False)),
        )

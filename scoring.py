from typing import Dict, Any, List
from .models import BCTRObject, LearnerObjectState, Packet, Rung, ClosureType, IState, MATRIX_FIELDS


CLOSURE_MULTIPLIERS = {
    ClosureType.TERMINAL: 1,
    ClosureType.FIXED_POINT: 2,
    ClosureType.CYCLE: 3,
    ClosureType.REGENERATIVE: 5,
    ClosureType.UNKNOWN: 1,
}


def closure_multiplier(closure_type: ClosureType) -> int:
    return CLOSURE_MULTIPLIERS.get(closure_type, 1)


def matrix_score(matrix: Dict[str, float]) -> float:
    """
    Sum the 18 matrix fields.

    Field scores:
    0   = absent / unclear / not usable
    0.5 = partial / unstable / observer-dependent
    1   = clear enough to route
    """
    total = 0.0
    for field in MATRIX_FIELDS:
        value = matrix.get(field, 0)
        if value not in (0, 0.5, 1):
            raise ValueError(f"Invalid score for {field}: {value}. Use 0, 0.5, or 1.")
        total += value
    return total


def object_weight(obj: BCTRObject) -> float:
    """
    Object Weight = Matrix Score × Closure Multiplier.
    """
    return matrix_score(obj.matrix) * closure_multiplier(obj.closure_type)


def derivative_pressure(obj: BCTRObject, weighted: bool = False) -> float:
    """
    Object-level derivative pressure.

    Simple mode:
        DP = tail count

    Weighted mode:
        DP = sum tail weights when provided.
        Missing tail weights default to 1.
    """
    if not weighted:
        return float(len(obj.tails))
    return sum(float(obj.tail_weights.get(tail, 1)) for tail in obj.tails)


def ownership_percent(state: LearnerObjectState) -> float:
    if state.required_crossings <= 0:
        return 0.0
    return max(0.0, min(1.0, state.paid_crossings / state.required_crossings))


def i_state_from_percent(percent: float, return_evidence: bool = False) -> IState:
    """
    i4 requires 80-100% ownership and return evidence.
    Without return evidence, cap at i3.
    """
    p = max(0.0, min(1.0, percent))
    if p < 0.20:
        return IState.I0
    if p < 0.40:
        return IState.I1
    if p < 0.60:
        return IState.I2
    if p < 0.80:
        return IState.I3
    return IState.I4 if return_evidence else IState.I3


def ownership_value(state: LearnerObjectState, obj: BCTRObject, return_evidence: bool = False) -> float:
    """
    Ownership Value = Ownership Percent × Object Weight.

    Note: i-state is a label; Ownership Value is the weighted numeric score.
    """
    return ownership_percent(state) * object_weight(obj)


def integral_burden(state: LearnerObjectState) -> float:
    """
    Integral Burden = sum weights of unpaid crossings.
    """
    return sum(state.unpaid_crossing_weights)


def packet_capacity(packet: Packet) -> float:
    """
    Packet Capacity = weighted crossings paid by packet.

    If no crossing weights are given, each crossing counts as 1.
    """
    if packet.crossing_weights:
        return sum(packet.crossing_weights)
    return float(len(packet.crossings_paid))


def rung_viability(rung: Rung, minimum_anchor_threshold: float = 1.0) -> Dict[str, Any]:
    """
    A rung is viable if:
    1. anchor value meets threshold
    2. packet capacity covers derivative pressure
    3. at least one i4 anchor exists
    4. return test exists
    """
    anchor_value = sum(rung.i4_anchor_values)
    dp = sum(rung.new_i0_object_weights)
    cap = sum(rung.selected_packet_capacities)

    checks = {
        "has_i4_anchor": len(rung.i4_anchor_values) > 0,
        "anchor_value_ok": anchor_value >= minimum_anchor_threshold,
        "capacity_covers_pressure": cap >= dp,
        "has_return_test": rung.has_return_test,
    }

    viable = all(checks.values())

    if not checks["has_i4_anchor"]:
        recommendation = "Add an entry or continuity bridge. No owned anchor survives."
    elif not checks["anchor_value_ok"]:
        recommendation = "Strengthen anchor before introducing new pressure."
    elif not checks["capacity_covers_pressure"]:
        recommendation = "Split rung or add bridge packet capacity."
    elif not checks["has_return_test"]:
        recommendation = "Add return test before marking rung viable."
    else:
        recommendation = "Rung is viable as a seed estimate."

    return {
        "rung_id": rung.rung_id,
        "anchor_value": anchor_value,
        "derivative_pressure": dp,
        "packet_capacity": cap,
        "checks": checks,
        "viable": viable,
        "recommendation": recommendation,
    }


def score_object(obj: BCTRObject) -> Dict[str, Any]:
    ms = matrix_score(obj.matrix)
    cm = closure_multiplier(obj.closure_type)
    w = object_weight(obj)
    dp = derivative_pressure(obj, weighted=False)
    wdp = derivative_pressure(obj, weighted=True)
    return {
        "object_id": obj.object_id,
        "label": obj.label,
        "matrix_score": ms,
        "closure_type": obj.closure_type.value,
        "closure_multiplier": cm,
        "object_weight": w,
        "tail_count": len(obj.tails),
        "derivative_pressure": dp,
        "weighted_derivative_pressure": wdp,
        "status": obj.status,
    }


def score_learner_state(state: LearnerObjectState, obj: BCTRObject, return_evidence: bool = False) -> Dict[str, Any]:
    own = ownership_percent(state)
    return {
        "agent_id": state.agent_id,
        "object_id": state.object_id,
        "ownership_percent": own,
        "i_state": i_state_from_percent(own, return_evidence=return_evidence).value,
        "ownership_value": ownership_value(state, obj, return_evidence=return_evidence),
        "integral_burden": integral_burden(state),
        "return_evidence": return_evidence,
    }


def score_packet(packet: Packet) -> Dict[str, Any]:
    return {
        "packet_id": packet.packet_id,
        "label": packet.label,
        "debt_type": packet.debt_type,
        "crossings_paid": packet.crossings_paid,
        "packet_capacity": packet_capacity(packet),
        "status": packet.status,
    }


def score_rung(rung: Rung) -> Dict[str, Any]:
    return rung_viability(rung)

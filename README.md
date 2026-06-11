# BCTR v4 Scoring Engine

A tiny operational engine for turning the BCTR 18-question Stability Matrix into numbers.

Canon pipeline:

```text
O -> M(O) -> T(O) -> D(O,A) -> P(D) -> X(O,A)
```

Scoring pipeline:

```text
M(O) -> Matrix Score
Matrix Score × Closure Multiplier -> Object Weight
T(O) -> Derivative Pressure
Unpaid crossings -> Integral Burden
P(D) -> Packet Capacity
X(O,A) -> Ownership Percent and i-State
```

## What this engine does

Given an object record, it calculates:

- `matrix_score`
- `closure_multiplier`
- `object_weight`
- `tail_count`
- `derivative_pressure`
- `ownership_percent`
- `i_state`
- `ownership_value`
- `integral_burden`
- `packet_capacity`
- `rung_viability`

## Quick Start

```bash
python -m bctr_engine.cli examples/euler_route.json
```

Or:

```bash
python run_demo.py
```

## Design Boundary

These scores are routing estimates, not truth claims.  
A score without evidence is not BCTR.  
Always store score + evidence + packet + return result.

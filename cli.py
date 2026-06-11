import json
import sys
from pathlib import Path

from .models import BCTRObject, LearnerObjectState, Packet, Rung
from .scoring import score_object, score_learner_state, score_packet, score_rung


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m bctr_engine.cli <route.json>")
        sys.exit(1)

    path = Path(sys.argv[1])
    data = json.loads(path.read_text())

    results = {"objects": [], "learner_states": [], "packets": [], "rungs": []}

    objects = {}
    for raw in data.get("objects", []):
        obj = BCTRObject.from_dict(raw)
        objects[obj.object_id] = obj
        results["objects"].append(score_object(obj))

    for raw in data.get("learner_states", []):
        state = LearnerObjectState.from_dict(raw)
        obj = objects.get(state.object_id)
        if obj is None:
            raise ValueError(f"Learner state references missing object: {state.object_id}")
        results["learner_states"].append(
            score_learner_state(state, obj, return_evidence=raw.get("return_evidence", False))
        )

    for raw in data.get("packets", []):
        packet = Packet.from_dict(raw)
        results["packets"].append(score_packet(packet))

    for raw in data.get("rungs", []):
        rung = Rung.from_dict(raw)
        results["rungs"].append(score_rung(rung))

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

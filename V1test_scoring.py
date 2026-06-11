from bctr_engine.models import BCTRObject, ClosureType, LearnerObjectState
from bctr_engine.scoring import matrix_score, object_weight, ownership_percent, i_state_from_percent


def test_matrix_score():
    obj = BCTRObject("O", "test", {"definition": 1}, ClosureType.TERMINAL)
    assert matrix_score(obj.matrix) == 1


def test_object_weight():
    obj = BCTRObject("O", "test", {"definition": 1}, ClosureType.REGENERATIVE)
    assert object_weight(obj) == 5


def test_ownership():
    state = LearnerObjectState("A", "O", 10, 5)
    assert ownership_percent(state) == 0.5
    assert i_state_from_percent(0.5).value == "i2"
from scoring import object_weight


def test_terminal_weight():
    assert object_weight(10, "terminal") == 10


def test_fixed_point_weight():
    assert object_weight(14, "fixed_point") == 28


def test_cycle_weight():
    assert object_weight(13, "cycle") == 39


def test_regenerative_weight():
    assert object_weight(15.5, "regenerative") == 77.5


def test_unknown_weight():
    assert object_weight(10, "unknown") == 10

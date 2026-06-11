"""
BCTR v4 Object Scoring Engine
Reference implementation

Input:
- matrix score
- closure type

Output:
- object weight
"""

CLOSURE_MULTIPLIERS = {
    "terminal": 1,
    "fixed_point": 2,
    "cycle": 3,
    "regenerative": 5,
    "unknown": 1
}


def object_weight(matrix_score, closure_type):
    multiplier = CLOSURE_MULTIPLIERS.get(
        closure_type,
        1
    )

    return matrix_score * multiplier


def score_object(label, matrix_score, closure_type):
    weight = object_weight(
        matrix_score,
        closure_type
    )

    return {
        "label": label,
        "matrix_score": matrix_score,
        "closure_type": closure_type,
        "closure_multiplier": CLOSURE_MULTIPLIERS[closure_type],
        "object_weight": weight
    }


if __name__ == "__main__":

    pi = score_object(
        "pi",
        15.5,
        "regenerative"
    )

    euler = score_object(
        "e^(i*pi)+1=0",
        17,
        "regenerative"
    )

    print(pi)
    print(euler)

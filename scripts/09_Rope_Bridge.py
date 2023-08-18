import numpy as np

test_data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""".strip().split(
    "\n"
)

test_result = 13


# set up movement space
grid = np.full((6, 5), ".")


def parse_instructions(lines):
    directions = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}
    moves = []
    for line in lines:
        move = [directions[line[0]], int(line[-1])]
        moves.append(move)
    return moves


assert parse_instructions(["R 4"]) == [[(0, 1), 4]]
assert parse_instructions(test_data) == [
    [(0, 1), 4],
    [(-1, 0), 4],
    [(0, -1), 3],
    [(1, 0), 1],
    [(0, 1), 4],
    [(1, 0), 1],
    [(0, -1), 5],
    [(0, 1), 2],
]

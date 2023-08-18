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


def parse_instructions(lines):
    """Parse instructions for head from given list"""
    directions = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}
    moves = []
    for line in lines:
        move = [directions[line[0]], int(line[-1])]
        moves.append(move)
    return moves


assert parse_instructions(["R 4"]) == [[(1, 0), 4]]
assert parse_instructions(test_data) == [
    [(1, 0), 4],
    [(0, -1), 4],
    [(-1, 0), 3],
    [(0, 1), 1],
    [(1, 0), 4],
    [(0, 1), 1],
    [(-1, 0), 5],
    [(1, 0), 2],
]


def make_move(mover, move, position, grid):
    """Move the given mover (H/T) on the grid
    from current position to new one"""
    grid[position] = "."
    new_position = tuple(x + y for x, y in zip(position, move))
    grid[new_position] = mover
    return grid


test_grid = np.full((6, 5), ".")
test_grid[(2, 2)] = "H"
expected_grid = np.full((6, 5), ".")
expected_grid[(2, 3)] = "H"

assert np.array_equal(make_move("H", (0, 1), (2, 2), test_grid), expected_grid)


def calculate_tail_move(position_head, position_tail):
    """Given the current positions,
    calculate the corresponding move for the tail"""

    # if in same column
    if position_head[0] == position_tail[0]:
        # check if head is up/down from tail
        if position_head[1] > position_tail[1]:
            move = (0, 1)
        else:
            move = (0, -1)
    # if in same row
    elif position_head[1] == position_tail[1]:
        # check if head is left/right from tail
        if position_head[0] > position_tail[0]:
            move = (1, 0)
        else:
            move = (-1, 0)
    else:
        # check which diagonal
        if position_head[0] > position_tail[0] and position_head[1] > position_tail[1]:
            move = (1, 1)
        elif (
            position_head[0] > position_tail[0] and position_head[1] < position_tail[1]
        ):
            move = (1, -1)
        elif (
            position_head[0] < position_tail[0] and position_head[1] < position_tail[1]
        ):
            move = (-1, -1)
        else:
            move = (-1, 1)

    return move


assert calculate_tail_move((3, 1), (1, 1)) == (1, 0)
assert calculate_tail_move((1, 3), (1, 1)) == (0, 1)
assert calculate_tail_move((1, 2), (3, 1)) == (-1, 1)
assert calculate_tail_move((2, 3), (3, 1)) == (-1, 1)

# set up movement space
grid = np.full((6, 5), ".")

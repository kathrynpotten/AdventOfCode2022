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
    directions = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}
    moves = []
    for line in lines:
        move = (directions[line[0]], int(line[-1]))
        moves.append(move)
    return moves


assert parse_instructions(["R 4"]) == [((0, 1), 4)]
assert parse_instructions(test_data) == [
    ((0, 1), 4),
    ((-1, 0), 4),
    ((0, -1), 3),
    ((1, 0), 1),
    ((0, 1), 4),
    ((1, 0), 1),
    ((0, -1), 5),
    ((0, 1), 2),
]


def make_move(move, position):
    """Move the given mover (H/T) on the grid
    from current position to new one"""

    return tuple(x + y for x, y in zip(position, move))


assert make_move((0, 1), (2, 2)) == (2, 3)


def calculate_tail_move(position_head, position_tail):
    """Given the current positions,
    calculate the corresponding move for the tail"""

    difference = tuple(int(h - t) for h, t in zip(position_head, position_tail))
    if any(abs(x) > 1 for x in difference):
        move = tuple(int(x / abs(x)) if abs(x) != 0 else x for x in difference)
        # check new move gets us close enough
        new_move = ()
        while new_move != (0, 0):
            new_pos = tuple(x + y for x, y in zip(position_tail, move))
            new_move = calculate_tail_move(position_head, new_pos)
            if new_move == (0, 0):
                return move
    else:
        return (0, 0)


assert calculate_tail_move((3, 1), (1, 1)) == (1, 0)
assert calculate_tail_move((1, 3), (1, 1)) == (0, 1)
assert calculate_tail_move((1, 2), (3, 1)) == (-1, 1)
assert calculate_tail_move((2, 3), (3, 1)) == (-1, 1)


def number_of_unique_tail_positions(lines):
    # initialise start
    head = (0, 0)
    tail = (0, 0)

    # initialise set to keep track of tail positions
    tail_positions = set()
    tail_positions.add(tail)

    head_moves = parse_instructions(lines)

    for move in head_moves:
        direction, distance = move
        for _ in range(distance):
            head = make_move(direction, head)
            tail_move = calculate_tail_move(head, tail)
            tail = make_move(tail_move, tail)
            tail_positions.add(tail)
            print(head, tail)

    # print out final grid
    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0
    for coord in tail_positions:
        x, y = coord
        if x > max_x:
            max_x = x
        elif x < min_x:
            min_x = x
        if y > max_y:
            max_y = y
        elif y < min_y:
            min_y = y

    grid = np.full((max_x + 1 - min_x, max_y + 1 - min_y + 1), ".")
    for coord in tail_positions:
        x, y = coord
        x, y = x - min_x, y - min_y
        grid[x, y] = "#"
    grid[-min_x, -min_y] = "s"
    print("\n".join("".join(row) for row in grid))

    return len(tail_positions)


# assert number_of_unique_tail_positions(test_data) == test_result

with open("../input_data/09_Rope_Bridge.txt", "r", encoding="utf-8") as file:
    input = file.read().strip().split("\n")

test_1 = input[0:10]
number_of_unique_tail_positions(test_1)
# correct up to the first 10 instructions

# answer_1 = number_of_unique_tail_positions(input)
# print(answer_1)

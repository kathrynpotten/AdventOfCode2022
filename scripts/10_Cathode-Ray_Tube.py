import numpy as np
import math

test_data = """noop
addx 3
addx -5""".split(
    "\n"
)

with open("../input_data/10_Cathode-Ray_Tube_test.txt", "r", encoding="utf-8") as file:
    longer_test_data = file.read().strip().split("\n")


def parse_instructions(lines):
    instructions = []
    for line in lines:
        if line == "noop":
            cycle = 1
            add = 0
        elif line.split()[0] == "addx":
            cycle = 2
            add = int(line.split()[1])
        instructions.append((cycle, add))

    return instructions


assert parse_instructions(test_data) == [(1, 0), (2, 3), (2, -5)]


def execute_program(instructions):
    X = 1
    cycle = 1
    for instruction in instructions:
        cycles, add = instruction
        cycle += cycles
        X += add

    return X


assert execute_program([(1, 0), (2, 3), (2, -5)]) == -1


def calculate_strengths(instructions, check_cycles):
    sum_of_strengths = 0
    X = 1
    current_cycle = 1
    for instruction in instructions:
        num_of_cycles, add = instruction
        for i in range(num_of_cycles):
            current_cycle += 1
            if current_cycle in check_cycles and i != num_of_cycles - 1:
                sum_of_strengths += X * current_cycle
        X += add
        if current_cycle in check_cycles:
            sum_of_strengths += X * current_cycle
        if current_cycle >= max(check_cycles):
            break

    return sum_of_strengths


longer_instructions = parse_instructions(longer_test_data)
assert calculate_strengths(longer_instructions, [20]) == 420
assert calculate_strengths(longer_instructions, [60]) == 1140
assert calculate_strengths(longer_instructions, [100]) == 1800
assert calculate_strengths(longer_instructions, [20, 60, 100, 140, 180, 220]) == 13140


with open("../input_data/10_Cathode-Ray_Tube.txt", "r", encoding="utf-8") as file:
    input = file.read().strip().split("\n")

answer_instructions = parse_instructions(input)
answer_1 = calculate_strengths(answer_instructions, [20, 60, 100, 140, 180, 220])
print(answer_1)


""" Part 2 """


def sprite_position(X, cycle):
    row = math.floor((cycle - 1) / 40)
    return [(row, X - 1), (row, X), (row, X + 1)]


def CRT_draw(screen, sprite_position, current_pixel):
    if current_pixel in sprite_position:
        image = "#"
    else:
        image = "."
    screen[current_pixel] = image

    return screen


def current_pixel(cycle):
    row = math.floor((cycle - 1) / 40)
    col = (cycle - 40 * row) - 1
    return (row, col)


def produce_image(instructions):
    X = 1
    current_cycle = 1
    screen = np.full((6, 40), "")
    for instruction in instructions:
        sprite = sprite_position(X, current_cycle)
        num_of_cycles, add = instruction
        for _ in range(num_of_cycles):
            pixel = current_pixel(current_cycle)
            screen = CRT_draw(screen, sprite, pixel)
            current_cycle += 1
        X += add

    return "\n".join("".join(row) for row in screen)


longer_instructions_sample = longer_instructions[:11]
# print(produce_image(longer_instructions_sample))

# print(produce_image(longer_instructions))

print(produce_image(answer_instructions))

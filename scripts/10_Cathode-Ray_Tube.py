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


def signal_strength(X, cycle):
    return X * cycle


def calculate_strengths(instructions, check_cycles):
    sum_of_strengths = 0
    X = 1
    current_cycle = 1
    for instruction in instructions:
        num_of_cycles, add = instruction
        for _ in range(num_of_cycles):
            current_cycle += 1
            # need to add to X if necessary here...
            if current_cycle in check_cycles:
                sum_of_strengths += X * current_cycle

        X += add
        print(current_cycle, X)
        if current_cycle >= max(check_cycles):
            break

    return sum_of_strengths


longer_instructions = parse_instructions(longer_test_data)
# assert calculate_strengths(longer_instructions, [20]) == 420
# assert calculate_strengths(longer_instructions, [60]) == 1140
assert calculate_strengths(longer_instructions, [100]) == 1800
# assert calculate_strengths(longer_instructions, [20, 60, 100, 140, 180, 220]) == 13140

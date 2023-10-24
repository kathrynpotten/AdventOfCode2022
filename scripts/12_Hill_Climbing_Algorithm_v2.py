import numpy as np


test_data = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""".split(
    "\n"
)

test_result_visual = """v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^"""

test_result = 31


class Path:
    def __init__(self):
        self.steps_taken = 0

    def __repr__(self):
        return "\n".join("".join(row) for row in self.grid)

    def elevation_convert(self):
        init_grid = np.copy(self.grid)
        converted_grid = np.char.replace(init_grid, "S", "a")
        self.converted_grid = np.char.replace(converted_grid, "E", "z").astype("U25")
        for index, elem in np.ndenumerate(self.converted_grid):
            self.converted_grid[index] = ord(elem) - 96
        return self.converted_grid.astype(int)

    def parse_heightmap(self, input):
        locations = [list(loc) for loc in input]
        self.grid = np.array(locations, dtype="U25")
        self.converted_grid = self.elevation_convert()
        self.start_loc = self.starting_loc()
        self.best_signal_loc = self.best_signal_location()
        self.current_loc = self.best_signal_loc
        return self.converted_grid

    def starting_loc(self):
        row, col = int(np.where(self.grid == "S")[0][0]), int(
            np.where(self.grid == "S")[1][0]
        )
        self.start_loc = (row, col)
        return self.start_loc

    def best_signal_location(self):
        row, col = int(np.where(self.grid == "E")[0][0]), int(
            np.where(self.grid == "E")[1][0]
        )
        self.best_signal_loc = (row, col)
        return self.best_signal_loc

    def take_step(self):
        row, col = self.current_loc
        possible_moves = []
        min_elevation = self.converted_grid[row, col] - 1

        def check_on_grid(row, col):
            max_row, max_col = np.shape(self.grid)
            if 0 <= row < max_row and 0 <= col < max_col:
                return True
            else:
                return False

        if (
            check_on_grid(row - 1, col)
            and self.converted_grid[row - 1, col] >= min_elevation
        ):
            step_size = self.converted_grid[row - 1, col] - min_elevation
            possible_moves.append([(-1, 0), "v", step_size])
        if (
            check_on_grid(row, col - 1)
            and self.converted_grid[row, col - 1] >= min_elevation
        ):
            step_size = self.converted_grid[row, col - 1] - min_elevation
            possible_moves.append([(0, -1), ">", step_size])
        if (
            check_on_grid(row, col + 1)
            and self.converted_grid[row, col + 1] >= min_elevation
        ):
            step_size = self.converted_grid[row, col + 1] - min_elevation
            possible_moves.append([(0, 1), "<", step_size])
        if (
            check_on_grid(row + 1, col)
            and self.converted_grid[row + 1, col] >= min_elevation
        ):
            step_size = self.converted_grid[row + 1, col] - min_elevation
            possible_moves.append([(1, 0), "^", step_size])

        possible_moves.sort(key=lambda move: move[-1])
        best_move = possible_moves[0]

        self.converted_grid[self.current_loc] = 30
        self.current_loc = tuple(x + y for x, y in zip(self.current_loc, best_move[0]))

        self.grid[self.current_loc] = best_move[1]

    def climb_to_best_signal_loc(self):
        while self.current_loc != self.start_loc:
            self.take_step()
            self.steps_taken += 1

        for index, elem in np.ndenumerate(self.grid):
            if elem not in ["E", "v", "^", ">", "<"]:
                self.grid[index] = "."

        return self.steps_taken


test_path = Path()
test_path.parse_heightmap(test_data)
print(test_path.converted_grid)

steps_taken = test_path.climb_to_best_signal_loc()

assert steps_taken == test_result

with open(
    "../input_data/12_Hill_Climbing_Algorithm.txt", "r", encoding="utf-8"
) as file:
    input = file.read().strip().split("\n")


answer_path = Path()
answer_path.parse_heightmap(input)

answer_1 = answer_path.climb_to_best_signal_loc()
print(answer_1)

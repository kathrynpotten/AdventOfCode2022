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
        self.converted_grid = np.copy(self.grid)
        for index, elem in np.ndenumerate(self.grid):
            self.converted_grid[index] = ord(elem) - 96
        return self.converted_grid.astype(int)

    def parse_heightmap(self, input):
        locations = [list(loc) for loc in input]
        init_grid = np.array(locations, dtype="U25")
        self.grid = np.pad(init_grid, ((1, 1), (1, 1)), constant_values="~")
        self.converted_grid = self.elevation_convert()
        self.current_loc = self.starting_loc()
        return self.converted_grid

    def starting_loc(self):
        row, col = int(np.where(self.grid == "S")[0][0]), int(
            np.where(self.grid == "S")[1][0]
        )
        self.current_loc = (row, col)
        return self.current_loc

    def best_signal_location(self):
        row, col = int(np.where(self.grid == "E")[0][0]), int(
            np.where(self.grid == "E")[1][0]
        )
        self.best_signal_loc = (row, col)
        return self.best_signal_loc

    def initial_move(self, down=True, right=False, left=False, up=False):
        if down:
            self.grid[self.current_loc] = "v"
            self.current_loc = tuple(x + y for x, y in zip(self.current_loc, (1, 0)))
        elif right:
            self.grid[self.current_loc] = ">"
            self.current_loc = tuple(x + y for x, y in zip(self.current_loc, (0, 1)))
        elif left:
            self.grid[self.current_loc] = "<"
            self.current_loc = tuple(x + y for x, y in zip(self.current_loc, (0, -1)))
        elif up:
            self.grid[self.current_loc] = "^"
            self.current_loc = tuple(x + y for x, y in zip(self.current_loc, (-1, 0)))

    def take_step(self):
        row, col = self.current_loc
        possible_moves = []
        max_elevation = self.converted_grid[row, col] + 1

        if self.converted_grid[row + 1, col] <= max_elevation:
            step_size = self.converted_grid[row + 1, col] - max_elevation
            possible_moves.append([(1, 0), "v", step_size])

        if self.converted_grid[row, col + 1] <= max_elevation:
            step_size = self.converted_grid[row, col + 1] - max_elevation
            possible_moves.append([(0, 1), ">", step_size])

        if self.converted_grid[row, col - 1] <= max_elevation:
            step_size = self.converted_grid[row, col - 1] - max_elevation
            possible_moves.append([(0, -1), "<", step_size])

        if self.converted_grid[row - 1, col] <= max_elevation:
            step_size = self.converted_grid[row - 1, col] - max_elevation
            possible_moves.append([(-1, 0), "^", step_size])

        possible_moves.sort(key=lambda move: move[-1])
        best_move = possible_moves[-1]

        self.grid[self.current_loc] = best_move[1]
        self.converted_grid[self.current_loc] = 30
        self.current_loc = tuple(x + y for x, y in zip(self.current_loc, best_move[0]))

        self.grid[self.current_loc] = "S"

    def climb_to_best_signal_loc(self):
        self.best_signal_loc = self.best_signal_location()
        while self.current_loc != self.best_signal_loc:
            self.take_step()
            self.steps_taken += 1

        self.grid[self.current_loc] = "E"
        for index, elem in np.ndenumerate(self.grid):
            if elem not in ["E", "v", "^", ">", "<"]:
                self.grid[index] = "."

        return self.steps_taken


test_path = Path()
test_path.parse_heightmap(test_data)
print(test_path)
# print(test_path.converted_grid)

print("\n")
test_path.initial_move()
print(test_path)
print("\n")
for _ in range(10):
    test_path.take_step()
    print(test_path)
    print("\n")

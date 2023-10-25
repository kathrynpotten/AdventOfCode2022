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
    def __init__(self, input):
        self.steps_taken = 0
        locations = [list(loc) for loc in input]
        self.grid = np.array(locations, dtype="U25")
        self.m, self.n = np.shape(self.grid)
        self.distance_grid = np.full((self.m, self.n), -1)
        self.next_loc = set()

    def __repr__(self):
        return "\n".join("".join(row) for row in self.grid)

    def elevation_convert(self):
        init_grid = np.copy(self.grid)
        converted_grid = np.char.replace(init_grid, "S", "a")
        self.converted_grid = np.char.replace(converted_grid, "E", "z").astype("U25")
        for index, elem in np.ndenumerate(self.converted_grid):
            self.converted_grid[index] = ord(elem) - 96
        return self.converted_grid.astype(int)

    def parse_heightmap(self):
        self.converted_grid = self.elevation_convert()
        self.start_loc = self.starting_loc()
        self.best_signal_loc = self.best_signal_location()
        self.distance_grid[self.best_signal_loc] = 0
        self.next_loc.add(self.best_signal_loc)

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
        for coords in self.current_loc:
            row, col = coords
            possible_moves = []
            min_elevation = self.converted_grid[row, col] - 1
            self.converted_grid[row, col] = -5

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
                possible_moves.append((-1, 0))
            if (
                check_on_grid(row, col - 1)
                and self.converted_grid[row, col - 1] >= min_elevation
            ):
                possible_moves.append((0, -1))
            if (
                check_on_grid(row, col + 1)
                and self.converted_grid[row, col + 1] >= min_elevation
            ):
                possible_moves.append((0, 1))
            if (
                check_on_grid(row + 1, col)
                and self.converted_grid[row + 1, col] >= min_elevation
            ):
                possible_moves.append((1, 0))

            for move in possible_moves:
                row, col = tuple(x + y for x, y in zip(coords, move))
                if self.distance_grid[row, col] == -1:
                    self.distance_grid[row, col] = self.steps_taken
                    self.next_loc.add(tuple(x + y for x, y in zip(coords, move)))

    def calculate_path_distance(self):
        while np.any(self.distance_grid == -1):
            if not self.next_loc:
                break
            self.current_loc = self.next_loc
            self.next_loc = set()
            self.steps_taken += 1
            self.take_step()

        return self.distance_grid

    def total_distance_from_start(self):
        return self.distance_grid[self.start_loc]

    def minimum_to_best_signal(self, from_height="a"):
        elev_grid = np.char.replace(self.grid, "S", "a")
        x, y = np.where(elev_grid == from_height)
        start_locs = list(zip(x, y))
        distances = [self.distance_grid[loc] for loc in start_locs]
        poss_distances = [dist for dist in distances if dist != -1]
        return min(poss_distances)


test_path = Path(test_data)
test_path.parse_heightmap()

test_path.calculate_path_distance()
steps_taken = test_path.total_distance_from_start()
minimum_from_a = test_path.minimum_to_best_signal()

assert steps_taken == test_result
assert minimum_from_a == 29


with open(
    "../input_data/12_Hill_Climbing_Algorithm.txt", "r", encoding="utf-8"
) as file:
    input = file.read().strip().split("\n")


answer_path = Path(input)
answer_path.parse_heightmap()

answer_path.calculate_path_distance()
answer_1 = answer_path.total_distance_from_start()
answer_2 = answer_path.minimum_to_best_signal()

print(answer_1, answer_2)

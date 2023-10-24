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
        pass

    def __repr__(self):
        return "\n".join()

    def elevation_convert(self):
        for index, elem in np.ndenumerate(self.grid):
            if elem == "S" or elem == "E":
                continue
            self.grid[index] = ord(elem) - 96
        return self.grid.astype(int)

    def parse_heightmap(self, input):
        locations = [list(loc) for loc in input]
        self.grid = np.array(locations, dtype="U25")
        self.converted_grid = elevation_convert(self.grid)
        return self.grid


def parse_input(input):
    new_input = []
    for line in input:
        line_list = [loc for loc in line]
        new_input.append(line_list)
    start_grid = np.array(new_input, dtype="U25")
    return start_grid


grid = parse_input(test_data)
print(parse_input(test_data))


def elevation_convert(grid):
    for index, elem in np.ndenumerate(grid):
        grid[index] = ord(elem) - 96
    return grid.astype(int)


print(elevation_convert(grid))

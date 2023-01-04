##### Day 14 #####
# https://adventofcode.com/2022/day/14

# ------------------------------------------------
# imports
# ------------------------------------------------
import matplotlib.pyplot as plt

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
with open("input.csv", "r") as file:
    lines = file.readlines()

walls = [x.replace("\n", "").split(" -> ") for x in lines]
# ------------------------------------------------
# Solution
# ------------------------------------------------
def plot_map(wall_points, sand_points):
    wall_xy_to_plot = list(zip(*wall_points))
    sand_xy_to_plot = list(zip(*sand_points))
    plt.gca().invert_yaxis()
    plt.scatter(*wall_xy_to_plot)
    plt.scatter(*sand_xy_to_plot)
    plt.show()


def get_wall_points(p1, p2):
    wall_points = set()
    if p1[1] == p2[1]:
        wall_points = wall_points.union(
            set([(x, p1[1]) for x in range(min(p1[0], p2[0]), max(p1[0], p2[0]))])
        )
    if p1[0] == p2[0]:
        wall_points = wall_points.union(
            set([(p1[0], y) for y in range(min(p1[1], p2[1]), max(p1[1], p2[1]))])
        )
    wall_points = wall_points.union(set([p1, p2]))
    return wall_points


def add_floor(wall_points):
    floor = max(wall_points, key=lambda item: item[1])[1] + 2
    for point in wall_points.copy():
        wall_points.add((point[0], floor))
        wall_points.add((point[0] - 1, floor))
        wall_points.add((point[0] + 1, floor))
    return wall_points, floor


def get_next_possible_positions(cur_col, curr_row):
    return [
        (cur_col, curr_row + 1),
        (cur_col - 1, curr_row + 1),
        (cur_col + 1, curr_row + 1),
    ]


def simulate(walls, floor=None):
    wall_points = set()
    for wall in walls:
        for i in range(len(wall) - 1):
            wall_points = wall_points.union(
                get_wall_points(eval(wall[i]), eval(wall[i + 1]))
            )
    if floor:
        wall_points, floor = add_floor(wall_points)
    all_cols = set([x for x, _ in wall_points])
    all_rows = set([y for _, y in wall_points])
    all_points = wall_points.copy()

    sand_points = set()
    out_of_bound = False
    while not out_of_bound:
        if (500, 0) in sand_points:
            return wall_points, sand_points
        cur_col, cur_row = (500, 0)
        # check the if one of the lower points is available
        resting_position = False
        while not resting_position:
            resting_position = True
            lower_possible_positions = get_next_possible_positions(cur_col, cur_row)
            for point in lower_possible_positions:
                if floor:
                    all_points.add((point[0], floor))
                # if any is empty move down to it
                if not point in all_points:
                    cur_col, cur_row = point
                    resting_position = False
                    break
            if cur_row > max(all_rows) + 1:
                resting_position = True
                out_of_bound = True
        if not out_of_bound:
            all_cols.add(cur_col)
            all_rows.add(cur_row)
            sand_points.add((cur_col, cur_row))
            all_points.add((cur_col, cur_row))
            if floor:
                all_points.add((cur_col, floor))
                all_points.add((cur_col - 1, floor))
                all_points.add((cur_col + 1, floor))
    return wall_points, sand_points


# ---------------- part 1 ----------------
wall_points, sand_points = simulate(walls)
# %load_ext line_profiler
# %lprun -f simulate simulate(walls)

print(len(sand_points))
# plot_map(wall_points, sand_points)
# ---------------- part 2 ----------------
wall_points, sand_points = simulate(walls, True)
print(len(sand_points))
# plot_map(wall_points, sand_points)

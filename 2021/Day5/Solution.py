##### Day 5 #####
# https://adventofcode.com/2021/day/5

# ------------------------------------------------
# imports
# ------------------------------------------------
import pandas as pd

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------

lines_points = pd.read_csv(
    "input.csv", sep=" -> |,", names=["x1", "y1", "x2", "y2"], engine="python"
)
grid_size = lines_points.max().max() + 1

# ------------------------------------------------
# Solution
# ------------------------------------------------
# ---------------- part 1 ----------------
# y = m*x + b
# m = slope = (y1-y2)/(x1-x2)
# b = y-intercept = (x1*y2 - x2*y1)/(x1-x2)
def draw_hv_line(row, grid):
    x1 = min(row["x1"], row["x2"])
    x2 = max(row["x1"], row["x2"])
    y1 = min(row["y1"], row["y2"])
    y2 = max(row["y1"], row["y2"])
    if x1 == x2:
        grid.iloc[x1, y1 : (y2 + 1)] += 1
    if y1 == y2:
        grid.iloc[x1 : (x2 + 1), y1] += 1
    return grid


grid = pd.DataFrame(0, columns=range(grid_size), index=range(grid_size))
for i in range(lines_points.shape[0]):
    grid = draw_hv_line(lines_points.iloc[i, :], grid)

print((grid > 1).sum().sum())
## 4421
# ---------------- part 2 ----------------
def get_range(x1, x2):
    if x1 > x2:
        return reversed(range(x2, x1 + 1))
    return range(x1, x2 + 1)


def draw_diag_line(row, grid):
    x1 = row["x1"]
    x2 = row["x2"]
    y1 = row["y1"]
    y2 = row["y2"]
    if (x1 != x2) & (y1 != y2):
        for x, y in zip(get_range(x1, x2), get_range(y1, y2)):
            grid.iloc[x, y] += 1
    return grid


for i in range(lines_points.shape[0]):
    grid = draw_diag_line(lines_points.iloc[i, :], grid)

print((grid > 1).sum().sum())
## 18674
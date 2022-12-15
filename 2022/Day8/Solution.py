##### Day 8 #####
# https://adventofcode.com/2022/day/8

# ------------------------------------------------
# imports
# ------------------------------------------------
import numpy as np

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------

data = np.loadtxt("input.csv", dtype=str)

tree_map = np.array([[int(x) for x in list(row)] for row in data])

# ------------------------------------------------
# Solution
# ------------------------------------------------
def scenic_score_one_dir(dir_trees, point):
    high_trees_loc = np.where(dir_trees >= point)[0]
    if len(high_trees_loc) == 0:
        return len(dir_trees)
    else:
        return high_trees_loc[0] + 1


# ---------------- part 1 ----------------
trees_on_edges = tree_map.shape[0] * 2 + tree_map.shape[1] * 2 - 4
count = 0
for row in range(1, tree_map.shape[0] - 1):
    for col in range(1, tree_map.shape[1] - 1):
        point = tree_map[row, col]
        up = tree_map[0:row, col]
        down = tree_map[(row + 1) :, col]
        left = tree_map[row, 0:col]
        right = tree_map[row, (col + 1) :]
        if (
            np.all(point > up)
            + np.all(point > down)
            + np.all(point > left)
            + np.all(point > right)
        ) > 0:
            count += 1
print(trees_on_edges + count)

# ---------------- part 2 ----------------
max_scenic_score = 0
for row in range(1, tree_map.shape[0] - 1):
    for col in range(1, tree_map.shape[1] - 1):
        point = tree_map[row, col]
        up = np.flip(tree_map[0:row, col])
        down = tree_map[(row + 1) :, col]
        left = np.flip(tree_map[row, 0:col])
        right = tree_map[row, (col + 1) :]
        point_scenic_score = (
            scenic_score_one_dir(up, point)
            * scenic_score_one_dir(down, point)
            * scenic_score_one_dir(left, point)
            * scenic_score_one_dir(right, point)
        )
        # print(f"row: {row}, col: {col}, point: {point}, score: {point_scenic_score}")
        max_scenic_score = max(max_scenic_score, point_scenic_score)
print(max_scenic_score)

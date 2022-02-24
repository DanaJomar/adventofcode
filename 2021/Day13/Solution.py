##### Day 13 #####
# https://adventofcode.com/2021/day/13

# ------------------------------------------------
# imports
# ------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
folds = []
x_coords = ()
y_coords = ()
with open("input.csv", "r") as file:
    for line in file:
        line = line.replace("\n", "")
        if line.startswith("fold"):
            folds.append(line.split("fold along ")[1].split("="))
        elif line != "":
            coords_str = line.split(",")
            x_coords += (int(coords_str[0]),)
            y_coords += (int(coords_str[1]),)
coords = (x_coords, y_coords)

# ------------------------------------------------
# Solution
# ------------------------------------------------
# ---------------- part 1 ----------------
max_coord = (max(coords[0]) + 1, max(coords[1]) + 1)
grid = np.zeros(tuple(max_coord))
grid[coords] = 1
for fold in folds:
    axis = fold[0]
    loc = int(fold[1])
    if axis == "y":
        grid = grid[:, :loc] + np.flip(grid[:, (loc + 1) :], 1)
    if axis == "x":
        grid = grid[:loc, :] + np.flip(grid[(loc + 1) :, :], 0)
    print("Folded along: " + axis + " = " + str(loc))
    print("\tNumber of dots: " + str(len(grid[grid > 0])))
# ---------------- part 2 ----------------
grid[grid > 0] = 1
plt.imshow(np.transpose(grid), cmap="hot", interpolation="nearest")
plt.show()
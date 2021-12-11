##### Day 11 #####
# https://adventofcode.com/2021/day/11

# ------------------------------------------------
# imports
# ------------------------------------------------
import numpy as np
import pandas as pd

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------

with open("input.csv", "r") as file:
    lines = file.readlines()
data = pd.DataFrame([list(x.replace("\n", "")) for x in lines]).astype(int).values
# ------------------------------------------------
# Solution
# ------------------------------------------------
# ---------------- part 1 ----------------
def take_step(data):
    flashes = 0
    data = data + 1
    flashed_this_round = []
    flashes_idx = np.where(data > 9)
    while len(flashes_idx[0]):
        # pad with zeros to avoid errors at edge values
        # data = np.pad(data, 1)
        flashes += len(flashes_idx[0])
        # update neighbourhood
        for x, y in zip(flashes_idx[0], flashes_idx[1]):
            if x < (nrows - 1):
                data[(x + 1, y)] += 1
            if x > 0:
                data[(x - 1, y)] += 1
            if y < (ncols - 1):
                data[(x, y + 1)] += 1
            if y > 0:
                data[(x, y - 1)] += 1
            if (x < (nrows - 1)) & (y < (ncols - 1)):
                data[(x + 1, y + 1)] += 1
            if (x > 0) & (y > 0):
                data[(x - 1, y - 1)] += 1
            if (x < (nrows - 1)) & (y > 0):
                data[(x + 1, y - 1)] += 1
            if (x > 0) & (y < (ncols - 1)):
                data[(x - 1, y + 1)] += 1
        # add indices to those which needs to be reset
        flashed_this_round += [flashes_idx]
        data[flashes_idx] = 0
        # update flashes_idx
        flashes_idx = np.where(data > 9)
        # remove padding
        # data = data[1 : (nrows + 1), 1 : (ncols + 1)]
    # reset flashed octopuses
    for idx in flashed_this_round:
        data[idx] = 0
    return flashes, data


flashes = 0
nrows, ncols = data.shape
for i in range(100):
    f, data = take_step(data)
    flashes += f
#     print(data)
#     print("-------------------")
print(flashes)
## 1675

# ---------------- part 2 ----------------
data = pd.DataFrame([list(x.replace("\n", "")) for x in lines]).astype(int).values
found = False
i = 0
while not found:
    i += 1
    _, data = take_step(data)
    if all((data == 0).flatten()):
        found = True
print(i)
## 515
##### Day 1 #####
# https://adventofcode.com/2021/day/1

# ------------------------------------------------
# imports
# ------------------------------------------------
import numpy as np

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
with open("input.txt") as f:
    lines = f.readlines()
depths = np.array([int(x.replace("\n", "")) for x in lines])

# ------------------------------------------------
# Solution
# ------------------------------------------------
# ---------------- part 1 ----------------
def get_number_of_increases(data_array):
    return (np.roll(data_array, 1)[1:] - data_array[1:] < 0).sum()


# number of increases in depth readings
get_number_of_increases(depths)
## 1688

# ---------------- part 2 ----------------
def rolling_sum(data_array, window_size):
    # https://stackoverflow.com/a/38507725/4905565
    return np.convolve(data_array, np.ones(window_size, dtype=int), "valid")


get_number_of_increases(rolling_sum(depths, 3))
## 1728
##### Day 1 #####
# https://adventofcode.com/2022/day/1

# ------------------------------------------------
# imports
# ------------------------------------------------
import numpy as np

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
with open("input.csv", "r") as file:
    lines = file.read()

cal_list = np.array([x.split("\n") for x in lines.split("\n\n")], dtype=object)

cal_sums = np.array([np.array(x, dtype=int).sum() for x in cal_list])
# ------------------------------------------------
# Solution
# ------------------------------------------------
# ---------------- part 1 ----------------
print(max(cal_sums))
# ---------------- part 2 ----------------
cal_sums.sort()
print(sum(cal_sums[-3:]))

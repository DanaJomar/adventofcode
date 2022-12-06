##### Day 5 #####
# https://adventofcode.com/2022/day/5

# ------------------------------------------------
# imports
# ------------------------------------------------
import re
import numpy as np

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------

with open("input.csv", "r") as file:
    moving_detailes = []
    crate_stacks_raw = []
    moving_info = False
    for line in file:
        if moving_info:
            move = re.findall(r"\d+", line)
            moving_detailes.append(move)
        elif line == "\n":
            moving_info = True
        else:
            crate_stacks_raw.append(list(line.replace("\n", "")))

crate_stacks = np.array(crate_stacks_raw)
crate_locs = np.where(np.char.isnumeric(crate_stacks[-1]))[0]
crate_stacks = crate_stacks[:-1, crate_locs]
crate_stacks = {
    str(i + 1): [x for x in crate_stacks[:, i] if x != " "]
    for i in range(len(crate_locs))
}
# ------------------------------------------------
# Solution
# ------------------------------------------------
# ---------------- part 1 ----------------
crate_stacks_copy = {k: list(v) for k, v in crate_stacks.items()}
for cnt, from_loc, to_loc in moving_detailes:
    for i in range(int(cnt)):
        crate = crate_stacks_copy[from_loc].pop(0)
        crate_stacks_copy[to_loc].insert(0, crate)
"".join([x[0] for x in crate_stacks_copy.values()])
# ---------------- part 2 ----------------
crate_stacks_copy = {k: list(v) for k, v in crate_stacks.items()}
for cnt, from_loc, to_loc in moving_detailes:
    for i in range(int(cnt)):
        crate = crate_stacks_copy[from_loc].pop(0)
        crate_stacks_copy[to_loc].insert(i, crate)
"".join([x[0] for x in crate_stacks_copy.values()])

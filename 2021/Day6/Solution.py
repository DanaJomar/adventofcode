##### Day 6 #####
# https://adventofcode.com/2021/day/6

# ------------------------------------------------
# imports
# ------------------------------------------------
import pandas as pd

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------

init_state = pd.read_csv("input.csv", header=None).transpose()
init_state.columns = ["days"]
init_state = init_state.groupby("days").size().to_dict()
# ------------------------------------------------
# Solution
# ------------------------------------------------
# ---------------- part 1 ----------------
def update_state(state):
    new_state = {(x - 1): y for x, y in state.items() if x > -1}
    # new_state = remove_negative_keys(new_state)
    new_fish_generators = new_state.get(-1, 0)
    if new_fish_generators > 0:
        new_state[8] = new_state.get(8, 0) + new_fish_generators
        new_state[6] = new_state.get(6, 0) + new_fish_generators
        new_state[-1] = new_state.get(-1, 0) - new_fish_generators
    return new_state


state = init_state
for day in range(80):
    state = update_state(state)
sum(state.values())
## 360268

# ---------------- part 2 ----------------
state = init_state
for day in range(256):
    state = update_state(state)
    # print("Ater " + str(day + 1) + " day(s): " + ",".join([str(x) for x in state]))
sum(state.values())
## 1632146183902
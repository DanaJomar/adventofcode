##### Day 2 #####
# https://adventofcode.com/2021/day/2

# ------------------------------------------------
# imports
# ------------------------------------------------
import pandas as pd

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
commands_df = pd.read_csv("input.csv", delim_whitespace=True, names=["dir", "steps"])

# ------------------------------------------------
# Solution
# ------------------------------------------------
# ---------------- part 1 ----------------
taken_steps = commands_df.groupby("dir")["steps"].sum()
position_h = taken_steps["forward"]
position_v = taken_steps["down"] - taken_steps["up"]
position_h * position_v
## 1762050
# ---------------- part 2 ----------------
def forward(steps, current_pos):
    # increase horizonal position, and increase depth based on current aim
    return (
        current_pos[0] + steps,
        current_pos[1] + (steps * current_pos[2]),
        current_pos[2],
    )


def down(steps, current_pos):
    # increase the aim
    return (current_pos[0], current_pos[1], current_pos[2] + steps)


def up(steps, current_pos):
    # decrease the aim
    return down(-steps, current_pos)


caller = {"forward": forward, "up": up, "down": down}
# (position_h, position_v, aim)
current_pos = (0, 0, 0)
for i in commands_df.index:
    current_pos = caller[commands_df.loc[i, "dir"]](
        commands_df.loc[i, "steps"], current_pos
    )
    print(current_pos)

current_pos[0] * current_pos[1]

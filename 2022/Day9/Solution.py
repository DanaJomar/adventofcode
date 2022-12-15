##### Day 9 #####
# https://adventofcode.com/2022/day/9

# ------------------------------------------------
# imports
# ------------------------------------------------
import numpy as np

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
data = np.loadtxt("input.csv", dtype=str)

# ------------------------------------------------
# Solution
# ------------------------------------------------
def move_head(state, move, previous_tail_locs, tail):
    dirs = {"R": (0, 1), "L": (0, -1), "U": (1, 0), "D": (-1, 0)}
    for _ in range(int(move[1])):
        state[0] = tuple(map(lambda i, j: i + j, state[0], dirs[move[0]]))
        for knot in range(1, tail + 1):
            state, previous_tail_locs = move_knot(state, knot, previous_tail_locs, tail)
        # print(state)
    return state, previous_tail_locs


def move_knot(state, knot, previous_tail_locs, tail):
    row_dist = state[knot - 1][0] - state[knot][0]
    col_dist = state[knot - 1][1] - state[knot][1]
    if abs(col_dist) * abs(row_dist) > 1:
        col_move_dir = col_dist / abs(col_dist)
        row_move_dir = row_dist / abs(row_dist)
        state[knot] = (state[knot][0], state[knot][1] + col_move_dir)
        state[knot] = (state[knot][0] + row_move_dir, state[knot][1])
    elif abs(col_dist) > 1:
        col_move_dir = col_dist / abs(col_dist)
        state[knot] = (state[knot][0], state[knot][1] + col_move_dir)
    elif abs(row_dist) > 1:
        row_move_dir = row_dist / abs(row_dist)
        state[knot] = (state[knot][0] + row_move_dir, state[knot][1])
    if knot == tail:
        previous_tail_locs.add(state[knot])
    return state, previous_tail_locs


def simulate_movement(knot_cnt):
    state = {i: (0, 0) for i in range(knot_cnt)}
    previous_tail_locs = set()
    for move in data:
        state, previous_tail_locs = move_head(
            state, move, previous_tail_locs, knot_cnt - 1
        )
    return len(previous_tail_locs)


# ---------------- part 1 ----------------
print(simulate_movement(2))


# ---------------- part 2 ----------------
print(simulate_movement(10))

##### Day 10 #####
# https://adventofcode.com/2022/day/10

# ------------------------------------------------
# imports
# ------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
with open("input.csv", "r") as file:
    lines = file.readlines()

# ------------------------------------------------
# Solution
# ------------------------------------------------
def check_total_strength(stregnth_so_far, cycle, X, chosen_cycles):
    if cycle in chosen_cycles:
        stregnth_so_far = stregnth_so_far + cycle * X
    return stregnth_so_far


def draw_pixel(current_cycle, sprite_position, map_dict):
    h_loc = current_cycle // 40
    v_loc = current_cycle % 40
    current_row = map_dict.get(h_loc, [])
    if v_loc in sprite_position:
        map_dict[h_loc] = current_row + ["#"]
    else:
        map_dict[h_loc] = current_row + ["."]
    return map_dict


def run_cycle(cycle, map_dict, X):
    map_dict = draw_pixel(cycle, range(X, X + 3), map_dict)
    cycle += 1
    return cycle, map_dict


# ---------------- part 1 ----------------
X = 1
cycle = 0
total_signal_strength = 0
chosen_cycles = [20, 60, 100, 140, 180, 220]
for line in lines:
    command = line.replace("\n", "").split(" ")
    if command[0] == "noop":
        cycle += 1
        total_signal_strength = check_total_strength(
            total_signal_strength, cycle, X, chosen_cycles
        )
    if command[0] == "addx":
        cycle += 1
        total_signal_strength = check_total_strength(
            total_signal_strength, cycle, X, chosen_cycles
        )
        cycle += 1
        total_signal_strength = check_total_strength(
            total_signal_strength, cycle, X, chosen_cycles
        )
        X += int(command[1])

print(total_signal_strength)
# ---------------- part 2 ----------------
X = 0
cycle = 0
map_dict = {}
# map_dict = draw_pixel(cycle, range(X, X + 3), map_dict)
for line in lines:
    command = line.replace("\n", "").split(" ")
    if command[0] == "noop":
        cycle, map_dict = run_cycle(cycle, map_dict, X)
    if command[0] == "addx":
        cycle, map_dict = run_cycle(cycle, map_dict, X)
        cycle, map_dict = run_cycle(cycle, map_dict, X)
        X += int(command[1])


plt.imshow(pd.DataFrame(map_dict).transpose() == "#")

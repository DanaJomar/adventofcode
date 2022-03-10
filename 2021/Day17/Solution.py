##### Day 17 #####
# https://adventofcode.com/2021/day/17

# ------------------------------------------------
# imports
# ------------------------------------------------
import numpy as np
from math import sqrt
import pandas as pd

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------

input = "target area: x=29..73, y=-248..-194"
sample_input = "target area: x=20..30, y=-10..-5"

target_area = [x[3:].split("..") for x in input[12:].split(",")]
target_area = [range(int(x[0]), int(x[1]) + 1) for x in target_area]
# ------------------------------------------------
# Solution
# ------------------------------------------------
def step(velocity, current_pos):
    x = current_pos[0] + velocity[0]
    y = current_pos[1] + velocity[1]
    x_velocity = velocity[0] - np.sign(velocity[0])
    y_velocity = velocity[1] - 1
    return [x_velocity, y_velocity], [x, y]


def in_target_area(target_area, position):
    x = position[0]
    y = position[1]
    return (x in target_area[0]) & (y in target_area[1])


def passed_target_area(target_area, position):
    x = position[0]
    y = position[1]
    if target_area[0].stop > 0:
        passed_x = x >= target_area[0].stop
    elif target_area[0].start < 0:
        passed_x = x < target_area[0].start
    if target_area[1].stop > 0:
        passed_y = y >= target_area[1].stop
    elif target_area[1].start < 0:
        passed_y = y < target_area[1].start
    return passed_x | passed_y


def sum_first_n(n):
    return int(n * (n + 1) / 2)


def get_n_from_sum(x):
    a = 1
    b = 1
    c = -x * 2
    possible_solutions = [
        (-b + sqrt(b ** 2 - 4 * a * c)) / 2 * a,
        (-b - sqrt(b ** 2 - 4 * a * c)) / 2 * a,
    ]
    return max([round(i) for i in possible_solutions])


def plot_throw(init_velocity):
    init_pos = [0, 0]

    velocity = init_velocity
    pos = init_pos
    in_target = False
    passed = False

    grid = pd.DataFrame(
        "blue",
        columns=["color"],
        index=pd.MultiIndex.from_product(target_area, names=["x", "y"]),
    ).reset_index()
    grid = pd.concat([grid, pd.DataFrame({"x": [pos[0]], "y": pos[1], "color": "red"})])
    while (not in_target) & (not passed):
        velocity, pos = step(velocity, pos)
        in_target = in_target_area(target_area, pos)
        passed = passed_target_area(target_area, pos)
        grid = pd.concat(
            [grid, pd.DataFrame({"x": [pos[0]], "y": pos[1], "color": "red"})]
        )
    grid.plot.scatter(x="x", y="y", c="color")


def check_throw(velocity):
    init_pos = [0, 0]
    pos = init_pos
    in_target = False
    passed = False

    while (not in_target) & (not passed):
        velocity, pos = step(velocity, pos)
        in_target = in_target_area(target_area, pos)
        passed = passed_target_area(target_area, pos)
    return in_target


# ---------------- part 1 ----------------

##  asuuming we start with y_velocity. we reach y = 0 with velocity
## -y_velocity - 1. An we need max y_velocity, that keeps us with in the range
## meaning the starting y_velocity should be -lower_end_y_range - 1
##
## we then choose x such that it reaches and stays in the range of x
## while having enough x velocity:
## to get up n steps
## to hover y_velocity is 0
## n steps to gow down
## and one more to reach the target area

max_accepted_y_vel = -min(target_area[1]) - 1
accepted_x_vel = max_accepted_y_vel
while True:
    x_reach = sum_first_n(accepted_x_vel)
    if x_reach in target_area[0]:
        break
    if x_reach >= target_area[0].stop:
        accepted_x_vel -= 1
    if x_reach < target_area[0].start:
        accepted_x_vel += 1
plot_throw(init_velocity=[accepted_x_vel, max_accepted_y_vel])
print("highest y point : " + str(sum_first_n(max_accepted_y_vel)))

# ---------------- part 2 ----------------
max_accepted_y_vel = -min(target_area[1]) - 1
min_accepted_y_vel = min(target_area[1])
min_accepted_x_vel = get_n_from_sum(target_area[0].start)
max_accepted_x_vel = target_area[0].stop

all_accepted = set()
for y in range(min_accepted_y_vel, max_accepted_y_vel + 1):
    for x in range(min_accepted_x_vel, max_accepted_x_vel + 1):
        in_target = check_throw([x, y])
        if in_target:
            all_accepted.add((x, y))
print("All possible throws: " + str(len(all_accepted)))
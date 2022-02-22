##### Day 22 #####
# https://adventofcode.com/2021/day/22

# ------------------------------------------------
# imports
# ------------------------------------------------
import re
import numpy as np

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
with open("input.csv", "r") as file:
    lines = file.readlines()
lines = [l.replace("\n", "") for l in lines]

# ------------------------------------------------
# Solution
# ------------------------------------------------
def getRange(xy_lst, grid50=False, shift=0):
    start = int(xy_lst[0])
    end = int(xy_lst[1]) + 1
    if grid50:
        if start < -50:
            start = -50
        if end < -50:
            end = -50
        if start > 51:
            start = 51
        if end > 51:
            end = 51
    return range(start + shift, end + shift)


def getCube(line, grid50=False, shift=0):
    pattern = re.compile("x=|y=|z=|on |off ")
    return [
        getRange(x.split(".."), grid50, shift) for x in pattern.sub("", line).split(",")
    ]


def intersected(cube_1, cube_2):
    if (len(cube_1) == 0) | (len(cube_2) == 0):
        return False
    x_intersects = (
        (cube_1[0].start in cube_2[0])
        | (cube_1[0].stop - 1 in cube_2[0])
        | (cube_2[0].start in cube_1[0])
        | (cube_2[0].stop - 1 in cube_1[0])
    )
    y_intersects = (
        (cube_1[1].start in cube_2[1])
        | (cube_1[1].stop - 1 in cube_2[1])
        | (cube_2[1].start in cube_1[1])
        | (cube_2[1].stop - 1 in cube_1[1])
    )
    z_intersects = (
        (cube_1[2].start in cube_2[2])
        | (cube_1[2].stop - 1 in cube_2[2])
        | (cube_2[2].start in cube_1[2])
        | (cube_2[2].stop - 1 in cube_1[2])
    )
    return x_intersects & y_intersects & z_intersects


def cubeIntersect(cube_1, cube_2):
    if intersected(cube_1, cube_2):
        start_x = max(cube_1[0].start, cube_2[0].start)
        start_y = max(cube_1[1].start, cube_2[1].start)
        start_z = max(cube_1[2].start, cube_2[2].start)

        end_x = min(cube_1[0].stop, cube_2[0].stop)
        end_y = min(cube_1[1].stop, cube_2[1].stop)
        end_z = min(cube_1[2].stop, cube_2[2].stop)

        return [range(start_x, end_x), range(start_y, end_y), range(start_z, end_z)]
    else:
        return []


def cubeSize(cube):
    if len(cube) == 0:
        return 0
    return len(cube[0]) * len(cube[1]) * len(cube[2])


def getSizes(cubes):
    total_size = 0
    for cube, sign in cubes:
        total_size = total_size + sign * cubeSize(cube)
    return total_size


# ---------------- part 1 ----------------
## method 1:
## brute force with numpy arrays (better for a fixed -moderate- grid size)
cubes = np.zeros((101, 101, 101))
for line in lines:
    on = line.startswith("on") + 0
    cube_wch = getCube(line, True, 50)
    cubes[
        cube_wch[0].start : cube_wch[0].stop,
        cube_wch[1].start : cube_wch[1].stop,
        cube_wch[2].start : cube_wch[2].stop,
    ] = on
cubes.sum()
## 596989.0

## method 2:
## a more scalabe method with cubes represented as 3-tuple of ranges
cubes = []
for line in lines:
    on = line.startswith("on")
    sign_new = 1 if on else -1
    cube_new = getCube(line, grid50=True)
    for cube_old, sign_old in cubes.copy():
        if intersected(cube_old, cube_new):
            cubes.append((cubeIntersect(cube_old, cube_new), -sign_old))
    if on:
        cubes.append((cube_new, sign_new))
getSizes(cubes.copy())
## 596989

# ---------------- part 2 ----------------
## solved as in method 2 from part 1.
## Remove the grid50=True arument from the getCube call
on_cubes = []
for line in lines:
    on = line.startswith("on")
    sign_new = 1 if on else -1
    cube_new = getCube(line)
    for cube_old, sign_old in on_cubes.copy():
        if intersected(cube_old, cube_new):
            on_cubes.append((cubeIntersect(cube_old, cube_new), -sign_old))
    if on:
        on_cubes.append((cube_new, sign_new))
getSizes(on_cubes.copy())
## 1160011199157381

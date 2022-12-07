##### Day 7 #####
# https://adventofcode.com/2022/day/7

# ------------------------------------------------
# imports
# ------------------------------------------------
import re

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
with open("input.csv", "r") as file:
    lines = [x.replace("\n", "") for x in file.readlines()]


FILESYSTEM_TREE = {"/": []}
FILE_SIZES = {}
FOLDER_SIZES = {}
TOTAL_DISK_SPACE = 70_000_000
NEEDED_SPACE = 30_000_000
# ------------------------------------------------
# Solution
# ------------------------------------------------
def get_current_loc(folder, curr_loc):
    if folder == "..":
        if curr_loc == "/":
            return curr_loc
        else:
            new_loc = [k for k, v in FILESYSTEM_TREE.items() if curr_loc in v]
            if len(new_loc) == 1:
                return new_loc[0]
            else:
                print(
                    f"Check your tree, the folder {folder} does not seem to exist in another folder"
                )
    else:
        if folder in FILESYSTEM_TREE.get(curr_loc, []):
            return folder
        else:
            print(f"{folder} is not in {curr_loc}")
            return curr_loc


def get_current_loc(move_to_loc, current_loc):
    if move_to_loc == "..":
        new_loc = "/" + "/".join(current_loc.split("/")[:-1])
    else:
        # TODO : check existance
        new_loc = current_loc + "/" + move_to_loc
    return re.sub("[/]+", "/", new_loc)


# ---------------- part 1 ----------------
current_loc = "/"
for line in lines:
    if "$ cd" in line:
        current_loc = get_current_loc(line.split(" ")[-1], current_loc)
        print(current_loc)
    elif "$ ls" not in line:
        line_info = line.split(" ")
        FILESYSTEM_TREE[current_loc] = FILESYSTEM_TREE.get(current_loc, []) + [
            get_current_loc(line_info[-1], current_loc)
        ]
        if line_info[0].isnumeric():
            FILE_SIZES[get_current_loc(line_info[-1], current_loc)] = int(line_info[0])
            FOLDER_SIZES[current_loc] = FOLDER_SIZES.get(current_loc, 0) + int(
                line_info[0]
            )
        else:
            FOLDER_SIZES[current_loc] = FOLDER_SIZES.get(current_loc, 0)
all_folders = list(FILESYSTEM_TREE.keys())
rev_rang = reversed(range(len(all_folders)))
for i in rev_rang:
    folder = all_folders[i]
    contents = FILESYSTEM_TREE.get(folder)
    for item in contents:
        if item in all_folders:
            FOLDER_SIZES[folder] = FOLDER_SIZES[folder] + FOLDER_SIZES[item]

print(sum([v for k, v in FOLDER_SIZES.items() if v < 100000]))
# ---------------- part 2 ----------------
free_space = TOTAL_DISK_SPACE - FOLDER_SIZES.get("/")
need_to_free = NEEDED_SPACE - free_space
min([x for x in FOLDER_SIZES.values() if x >= need_to_free])

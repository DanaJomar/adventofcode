##### Day 10 #####
# https://adventofcode.com/2021/day/10

# ------------------------------------------------
# imports
# ------------------------------------------------
import pandas as pd
import numpy as np
from itertools import compress

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
with open("input.csv", "r") as file:
    lines = file.readlines()
lines = [l.replace("\n", "") for l in lines]
# ------------------------------------------------
# Solution
# ------------------------------------------------
# ---------------- part 1 ----------------
open_brackets = ["[", "(", "<", "{"]
close_brackets = ["]", ")", ">", "}"]
brackets = {"(": ")", "[": "]", "<": ">", "{": "}"}
penalty = {")": 3, "]": 57, "}": 1197, ">": 25137}


def is_corrupt(l):
    corrupt = False
    penalty_ = 0
    open_stack = []
    matched_brackets = pd.DataFrame(
        columns=["open", "close", "should_close", "open_idx", "close_idx"]
    )
    for i, c in enumerate(l):
        if c in open_brackets:
            open_stack.append(i)
        if c in close_brackets:
            open_loc = open_stack.pop()
            matched_brackets = matched_brackets.append(
                pd.DataFrame(
                    {
                        "open": [l[open_loc]],
                        "close": [c],
                        "should_close": [brackets.get(l[open_loc])],
                        "open_idx": [open_loc],
                        "close_idx": [i],
                    }
                )
            )
    matched_brackets.reset_index(drop=True, inplace=True)
    false_matches = np.where(
        matched_brackets["close"] != matched_brackets["should_close"]
    )[0]
    if len(false_matches) != 0:
        illegal_char = matched_brackets.loc[false_matches[0], "close"]
        corrupt = True
        penalty_ = penalty.get(illegal_char)

    # print(l)
    # print("------------------")
    # print(matched_brackets)
    # print("------------------")
    return corrupt, penalty_, open_stack


total_penalty = 0
corrupted = []
open_stacks = []
for l in lines:
    corrupt, penalty_, open_stack = is_corrupt(l)
    total_penalty += penalty_
    corrupted.append(corrupt)
    open_stacks.append(open_stack)
print(total_penalty)

# ---------------- part 2 ----------------
score_addition = {")": 1, "]": 2, "}": 3, ">": 4}

not_corrupted = [not x for x in corrupted]
valid_lines = list(compress(lines, not_corrupted))
valid_lines_open_loc = list(compress(open_stacks, not_corrupted))

all_scores = []
for i in range(len(valid_lines)):
    line_score = 0
    l = valid_lines[i]
    open_loc = valid_lines_open_loc[i]
    while len(open_loc) > 0:
        b_loc = open_loc.pop()
        closing_b = brackets.get(l[b_loc])
        line_score = line_score * 5 + score_addition.get(closing_b)
    all_scores.append(line_score)
all_scores.sort()
all_scores[int(np.floor(len(all_scores) / 2))]
## 1605968119
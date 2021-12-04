##### Day 4 #####
# https://adventofcode.com/2021/day/4

# ------------------------------------------------
# imports
# ------------------------------------------------
import pandas as pd
import numpy as np
import io

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------

with open("input.csv", "r") as file:
    lines = file.readlines()
drawn = lines[0]
drawn = [int(x) for x in drawn.split(",")]
sep_loc = np.where(["\n" == x for x in lines])[0]
board_start = (sep_loc + 1).tolist()
board_end = sep_loc[1:].tolist() + [len(lines)]

boards = {}
for i in range(len(board_start)):
    boards["b" + str(i)] = [
        pd.read_csv(
            io.StringIO("".join(lines[board_start[i] : board_end[i]])),
            header=None,
            delim_whitespace=True,
        ),
        pd.DataFrame(False, columns=range(5), index=range(5)),
    ]
# ------------------------------------------------
# Solution
# ------------------------------------------------
# ---------------- part 1 ----------------
def run_game(boards, drawn):
    for n in drawn:
        for board in boards:
            boards[board][1] = boards[board][1] | (boards[board][0] == n)
            if (
                (boards[board][1].sum(axis=0) == 5).sum()
                + (boards[board][1].sum(axis=1) == 5).sum()
            ) > 0:
                return board, n, boards[board]


board_name, last_drawn, board = run_game(boards, drawn)

np.nansum(board[0][~board[1]].values) * last_drawn
## 27027.0

# ---------------- part 2 ----------------
while len(boards) > 0:
    board_name, last_drawn, board = run_game(boards, drawn)
    boards.pop(board_name)
    print(len(boards))

np.nansum(board[0][~board[1]].values) * last_drawn
## 36975.0
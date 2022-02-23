##### Day 21 #####
# https://adventofcode.com/2021/day/21

# ------------------------------------------------
# imports
# ------------------------------------------------

import itertools
import collections

from numpy import argmax

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
# Player 1 starting position: 5
# Player 2 starting position: 6
player1_start_position = 5  # 4
player2_start_position = 6  # 8
# ------------------------------------------------
# Solution
# ------------------------------------------------
def adapt_position(position, dice_value):
    return (position + dice_value - 1) % 10 + 1


# ---------------- part 1 ----------------


def deterministic_dice(last_run):
    dice_value = (last_run % 100) + 1
    return dice_value


def one_turn(player_position, last_dice_value):
    for _ in range(3):
        last_dice_value = deterministic_dice(last_dice_value)
        player_position = adapt_position(player_position, last_dice_value)
    return player_position, last_dice_value


player1_position = player1_start_position
player2_position = player2_start_position
player1_points = 0
player2_points = 0
last_dice_value = 0
end_game = False
die_rolls = 0
while not end_game:
    player1_position, last_dice_value = one_turn(player1_position, last_dice_value)
    player1_points += player1_position
    die_rolls += 3
    if player1_points >= 1000:
        end_game = False
        break
    player2_position, last_dice_value = one_turn(player2_position, last_dice_value)
    player2_points += player2_position
    die_rolls += 3
    if player2_points >= 1000:
        end_game = False
        break
print("Part 1:")
print("Player 1 scored: " + str(player1_points) + " points")
print("Player 2 scored: " + str(player2_points) + " points")
print("Die rolls: " + str(die_rolls))
print("Puzzle's answer: " + str(min(player1_points, player2_points) * die_rolls))
print("----------------------------------------------------------")
## 1002474

# ---------------- part 2 ----------------
def one_turn_quantum(state, univ_cnt, games, wins):
    position1, points1, position2, points2 = state
    for roll_value, roll_univ_cnt in ROLL_VALUES.items():
        position1_new = adapt_position(position1, roll_value)
        points1_new = points1 + position1_new
        if points1_new >= 21:
            wins[0] += univ_cnt * roll_univ_cnt
        else:
            for roll_value_2, roll_univ_cnt_2 in ROLL_VALUES.items():
                position2_new = adapt_position(position2, roll_value_2)
                points2_new = points2 + position2_new
                if points2_new >= 21:
                    wins[1] += univ_cnt * roll_univ_cnt * roll_univ_cnt_2
                else:
                    new_state = (position1_new, points1_new, position2_new, points2_new)
                    games[new_state] = (
                        games.get(new_state, 0)
                        + univ_cnt * roll_univ_cnt * roll_univ_cnt_2
                    )
    return wins


all_rolls_per_turn = list(itertools.product(*[range(1, 4), range(1, 4), range(1, 4)]))
ROLL_VALUES = collections.Counter([sum(x) for x in all_rolls_per_turn])
wins = [0, 0]
running_games = {(player1_start_position, 0, player2_start_position, 0): 1}
while len(running_games) > 0:
    current_games = running_games.copy()
    running_games = {}
    for state, univ_cnt in current_games.items():
        wins = one_turn_quantum(state, univ_cnt, running_games, wins)
print("Part 2:")
print("Player " + str(argmax(wins) + 1) + " won.")
print("Score: " + str(max(wins)))
print("----------------------------------------------------------")
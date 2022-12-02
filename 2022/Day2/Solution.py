##### Day 2 #####
# https://adventofcode.com/2022/day/2

# ------------------------------------------------
# imports
# ------------------------------------------------

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
with open("input.csv", "r") as file:
    lines = file.readlines()

strategy = [x.replace("\n", "").split(" ") for x in lines]

choice_foe = {"A": ["Y", "B"], "B": ["Z", "C"], "C": ["X", "A"]}
choice_value = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}
# ------------------------------------------------
# Solution
# ------------------------------------------------
# ---------------- part 1 ----------------
opp_score = 0
my_score = 0
for round_ in strategy:
    opp_choice = round_[0]
    my_choice = round_[1]
    # draw
    if choice_value[opp_choice] == choice_value[my_choice]:
        opp_outcome_score = 3
        my_outcome_score = 3
    # win
    elif my_choice in choice_foe[opp_choice]:
        opp_outcome_score = 0
        my_outcome_score = 6
    # lose
    else:
        opp_outcome_score = 6
        my_outcome_score = 0
    opp_score = opp_score + choice_value[opp_choice] + opp_outcome_score
    my_score = my_score + choice_value[my_choice] + my_outcome_score

print(my_score)
# ---------------- part 2 ----------------
opp_score = 0
my_score = 0
for round_ in strategy:
    opp_choice = round_[0]
    res_should = round_[1]
    # draw
    if res_should == "Y":
        opp_outcome_score = 3
        my_outcome_score = 3
        my_choice = opp_choice
    # win
    elif res_should == "Z":
        opp_outcome_score = 0
        my_outcome_score = 6
        my_choice = choice_foe[opp_choice][1]
    # lose
    else:
        opp_outcome_score = 6
        my_outcome_score = 0
        my_choice = (
            set(["A", "B", "C"])
            .difference(set(choice_foe[opp_choice][1]).union(set(opp_choice)))
            .pop()
        )
    opp_score = opp_score + choice_value[opp_choice] + opp_outcome_score
    my_score = my_score + choice_value[my_choice] + my_outcome_score

print(my_score)

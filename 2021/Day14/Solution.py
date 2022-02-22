##### Day 14 #####
# https://adventofcode.com/2021/day/14

# ------------------------------------------------
# imports
# ------------------------------------------------
from collections import Counter

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
with open("input.csv", "r") as file:
    lines = file.readlines()
lines = [x.replace("\n", "").replace('"', "") for x in lines]
polymer_template = lines[0]
formula = [x.split(" -> ") for x in lines[2:]]
formula = {x[0]: x[1] for x in formula}
# ------------------------------------------------
# Solution
# ------------------------------------------------
# ---------------- part 1 ----------------
def n_gram(list, n):
    return [list[i : i + n] for i in range(len(list) - n + 1)]


polymer_template = lines[0]
for _ in range(10):
    # print(polymer_template)
    bigrams = n_gram(polymer_template, 2)
    new_template = []
    for bigram in bigrams:
        new_template.append(bigram[0] + formula.get(bigram))
    polymer_template = "".join(new_template) + polymer_template[-1]

len(polymer_template)
letter_counts = {i: polymer_template.count(i) for i in set(polymer_template)}
key_max = max(letter_counts.keys(), key=(lambda k: letter_counts[k]))
key_min = min(letter_counts.keys(), key=(lambda k: letter_counts[k]))

print(letter_counts[key_max] - letter_counts[key_min])
## 3831

# ---------------- part 2 ----------------

polymer_template = lines[0]
bigrams = n_gram(polymer_template, 2)

bigrams_counts = Counter(bigrams)
letter_counts = Counter(polymer_template)
for _ in range(40):
    round_bigrams_counts = Counter()
    for bigram in bigrams_counts.keys():
        insertion = formula.get(bigram)
        round_bigrams_counts[bigram[0] + insertion] += bigrams_counts.get(bigram, 0)
        round_bigrams_counts[insertion + bigram[-1]] += bigrams_counts.get(bigram, 0)
        letter_counts[insertion] += bigrams_counts.get(bigram, 0)
    bigrams_counts = round_bigrams_counts
final_count = letter_counts.most_common()
print(final_count[0][1] - final_count[-1][1])
## 5725739914282

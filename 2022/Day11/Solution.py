##### Day 11 #####
# https://adventofcode.com/2022/day/11

# ------------------------------------------------
# imports
# ------------------------------------------------
import re
import numpy as np

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------

# ------------------------------------------------
# Solution
# ------------------------------------------------
class Monkey:
    def __init__(self, text):
        self.parse_text(text)
        self.inspections = 0

    def parse_text(self, text):
        text_splitted = text.split("\n")
        self.mon_id = int(re.findall(r"\b\d+\b", text_splitted[0])[0])
        self.items = np.array(
            [int(x) for x in re.findall(r"\b\d+\b", text_splitted[1])]
        )
        self.op_during_inspection = re.findall(r"old.*", text_splitted[2])[0]
        # self.op_during_inspection = op_during_inspection.replace("old", "{worry_level}")
        self.test_value = int(re.findall(r"\b\d+\b", text_splitted[3])[0])
        self.when_true = int(re.findall(r"\b\d+\b", text_splitted[4])[0])
        self.when_false = int(re.findall(r"\b\d+\b", text_splitted[5])[0])

    def breathe(self, breath_value):
        # print("\tbreathe")
        if breath_value != 0:
            self.items = self.items % breath_value
        else:
            self.items = self.items // 3
        # print("\t", self.items)

    def inspect_items(self, breath_value):
        # print("\tinspect_items")
        self.inspections = self.inspections + len(self.items)
        self.items = eval(self.op_during_inspection.replace("old", "self.items"))
        # print("\t", self.items)
        self.breathe(breath_value)

    def test_and_assign(self):
        # print("\ttest_and_assign")
        test_result = (self.items % self.test_value) == 0
        throws = {
            self.when_true: self.items[test_result],
            self.when_false: self.items[~test_result],
        }
        self.items = np.array([])
        # print("\t", self.items)
        return throws

    def add_to_items(self, new_items):
        # print("\tadd_to_items")
        self.items = np.append(self.items, new_items)
        # print("\t", self.mon_id, self.items)


def print_monkies(monkies):
    for _, monkey in monkies.items():
        print(
            f"{monkey.mon_id} ---- {monkey.items} ---- {monkey.inspections} ---- {monkey.inspections + len(monkey.items)}"
        )


def watch_monkies(input_file, rounds, breath_value):
    with open(input_file, "r") as f:
        lines = f.read()
    lines = lines.split("\n\n")
    monkies = {}
    for line in lines:
        new_monkey = Monkey(line)
        monkies[new_monkey.mon_id] = new_monkey
        breath_value = breath_value * int(re.findall(r"divisible by (\d+)", line)[0])

    for i in range(rounds):
        # print(f"round: {i}")
        # inspections = []
        for _, monkey in monkies.items():
            # print(f"{monkey.mon_id}")
            monkey.inspect_items(breath_value)
            throws = monkey.test_and_assign()
            for throw_to, throw_items in throws.items():
                monkies.get(throw_to).add_to_items(throw_items)
            # inspections.append(monkey.inspections)
        # print(inspections)
        # print("-----------")
    return monkies


# ---------------- part 1 ----------------
monkies = watch_monkies("input.csv", 20, breath_value=0)
inspections = []
for id, monkey in monkies.items():
    # print(id)
    # print(monkey.items)
    inspections.append(monkey.inspections)
inspections.sort()
print(inspections[-2] * inspections[-1])

# ---------------- part 2 ----------------
monkies = watch_monkies("input.csv", 10000, breath_value=1)
inspections = []
for id, monkey in monkies.items():
    # print(id)
    # print(monkey.items)
    inspections.append(monkey.inspections)
inspections.sort()
print(inspections[-2] * inspections[-1])

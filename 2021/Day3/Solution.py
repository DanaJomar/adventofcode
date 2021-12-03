##### Day 3 #####
# https://adventofcode.com/2021/day/3

# ------------------------------------------------
# imports
# ------------------------------------------------
from numpy.core.numeric import _ones_like_dispatcher
import pandas as pd

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------

report = pd.read_csv("input.csv", dtype=str, delim_whitespace=True, header=None)
report = (
    pd.DataFrame(report.iloc[:, 0].str.split("").tolist())
    .apply(pd.to_numeric)
    .dropna(axis=1)
)
# ------------------------------------------------
# Solution
# ------------------------------------------------
# ---------------- part 1 ----------------
def most_common(data):
    nrows = data.shape[0]
    ones_per_col = data.sum(axis=0)
    return (ones_per_col >= (nrows / 2)).values + 0


gamma_rate = most_common(report)
epslilon_rate = 1 - gamma_rate

gamma_dec = int("".join(gamma_rate.astype(str).tolist()), 2)
epsilon_dec = int("".join(epslilon_rate.astype(str).tolist()), 2)

power_consumption = gamma_dec * epsilon_dec
print(power_consumption)
## 2640986
# ---------------- part 2 ----------------
def most_common_per_pos(data, position):
    return most_common(data)[position]


def bit_criteria(data, rating_type="O"):
    filtered_data = data.copy()
    for i in range(data.shape[1]):
        if filtered_data.shape[0] == 1:
            return filtered_data
        val = most_common_per_pos(filtered_data, i)
        if rating_type == "CO2":
            val = 1 - val
        filtered_data = filtered_data[filtered_data.iloc[:, i] == val]
    return filtered_data


# oxygen generator rating
filtered_report = report.copy()
while filtered_report.shape[0] > 1:
    filtered_report = bit_criteria(filtered_report)

filtered_report
ox_rat = int("".join(filtered_report.iloc[0].astype(str).tolist()), 2)

# CO2 generator rating
filtered_report = report.copy()
while filtered_report.shape[0] > 1:
    filtered_report = bit_criteria(filtered_report, "CO2")

filtered_report
co2_rat = int("".join(filtered_report.iloc[0].astype(str).tolist()), 2)

life_support_rating = ox_rat * co2_rat
print(life_support_rating)
# 6822109
##### Day 13 #####
# https://adventofcode.com/2022/day/13

# ------------------------------------------------
# imports
# ------------------------------------------------

# ------------------------------------------------
# read and prepare input
# -----------------------------------------------

# ------------------------------------------------
# Solution
# ------------------------------------------------
def compare_int(x, y):
    if x != y:
        return x < y


def compare(x, y):
    comparison = []
    if isinstance(x, int):
        if isinstance(y, int):
            comparison = comparison + [compare_int(x, y)]
        else:
            comparison = comparison + compare([x], y)
    elif isinstance(y, int):
        comparison = comparison + compare(x, [y])
    else:
        element_wise_compare = [None]
        for i, j in zip(x, y):
            element_wise_compare = element_wise_compare + compare(i, j)
        if (len([x for x in element_wise_compare if x is not None]) == 0) & (
            len(x) != len(y)
        ):
            comparison = comparison + [len(x) < len(y)]
        else:
            comparison = comparison + element_wise_compare
    return comparison


def compare_packets(packet_1, packet_2):
    if packet_1 == packet_2:
        return True
    # print(packet_1, packet_2)
    comparison = compare(packet_1, packet_2)
    # print(comparison)
    comparison_clean = [x for x in comparison if x is not None]
    return comparison_clean[0]


def right_order_sum(input_file):
    with open(input_file, "r") as file:
        lines = file.read()
    data = lines.split("\n\n")
    order = []
    all_packets = []
    for i in range(len(data)):
        packets = [eval(x) for x in data[i].split("\n")]
        all_packets = all_packets + packets
        if compare_packets(packets[0], packets[1]):
            order.append(i)
    return order, all_packets


def quicksort(elements, start, end):
    if start < end:
        pivote_idx, elements = partition(elements, start, end)
        elements = quicksort(elements, start, pivote_idx - 1)
        elements = quicksort(elements, pivote_idx + 1, end)
    return elements


def partition(elements, start, end):
    value_to_compare = elements[end]
    j = start - 1
    for i in range(start, end):
        if compare_packets(elements[i], value_to_compare):
            j += 1
            elements = swap(elements, i, j)
    elements = swap(elements, j + 1, end)
    return j + 1, elements


def swap(elements, i, j):
    tmp = elements[i]
    elements[i] = elements[j]
    elements[j] = tmp
    return elements


# ---------------- part 1 ----------------
rightly_ordered, packets = right_order_sum("input.csv")
print(sum([x + 1 for x in rightly_ordered]))
# ---------------- part 2 ----------------
# add the new packets
packets = packets + [[[2]], [[6]]]

packets_ordered = quicksort(packets, 0, len(packets) - 1)
(packets_ordered.index([[2]]) + 1) * (packets_ordered.index([[6]]) + 1)

##### Day 16 #####
# https://adventofcode.com/2021/day/16

# ------------------------------------------------
# imports
# ------------------------------------------------
from math import log2, prod

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------

with open("input.csv", "r") as file:
    lines = file.readlines()
hex_packet_input = lines[0]
# examples:
examples_part1 = [
    "D2FE28",  # versions: 6
    "38006F45291200",  # versions: 1, 6, 2
    "EE00D40C823060",  # versions: 7, 2, 4, 1
    "8A004A801A8002F478",  # versions sum: 16
    "620080001611562C8802118E34",  # versions sum: 12
    "C0015000016115A2E0802F182340",  # versions sum: 23
    "A0016C880162017C3686B18A3D4780",  # versions sum: 31
]
examples_part2 = [
    "C200B40A82",  # 1 + 2 = 3
    "04005AC33890",  # 6 * 9 = 54
    "880086C3E88112",  # min(7, 8, 9) = 7
    "CE00C43D881120",  # max(7, 8, 9) = 9
    "D8005AC2A8F0",  # 5 < 15 = 1
    "F600BC2D8F",  # 5 > 15 = 0
    "9C005AC2F8F0",  # 5 == 15 = 0
    "9C0141080250320F1802104A08",  # 1 + 3 == 2 * 2 = 1
]
# ------------------------------------------------
# Solution
# ------------------------------------------------
def get_literal(literal_groups):
    literal = ""
    for i in range(0, len(literal_groups), 5):
        group = literal_groups[i : i + 5]
        literal += group[1:]
        if group[0] == "0":
            break
    return literal


def parse_type_4(binary_string):
    packetGroups = binary_string[6:]
    literal = get_literal(packetGroups)
    return literal


# ---------------- part 1 ----------------
def get_versions(hex_packet):
    num_of_bits = int(len(hex_packet) * log2(16))
    full_binary_string = bin(int(hex_packet, 16))[2:].zfill(num_of_bits)

    versions = []
    queue = [full_binary_string]
    while len(queue) > 0:
        binary_string = queue.pop()
        versionNum = int(binary_string[:3], 2)
        typeID = int(binary_string[3:6], 2)
        versions.append(versionNum)
        if typeID == 4:
            literal = parse_type_4(binary_string)
            literal_len = len(literal) + len(literal) / 4
            packet_len = int(literal_len + 6)
            remain = binary_string[packet_len:]
            if len(remain) >= 11:
                queue.append(remain)
        else:
            lengthTypeID = binary_string[6]
            if lengthTypeID == "0":
                start_char = 7 + 15
                subPacketLeng = int(binary_string[7:start_char], 2)
                queue.append(binary_string[start_char : (start_char + subPacketLeng)])
                remain = binary_string[(start_char + subPacketLeng) :]
                if len(remain) >= 11:
                    queue.append(remain)
            if lengthTypeID == "1":
                start_char = 7 + 11
                queue.append(binary_string[start_char:])
    return versions


for hex_packet in examples_part1:
    print(hex_packet)
    print(sum(get_versions(hex_packet)))
print(sum(get_versions(hex_packet_input)))

# ---------------- part 2 ----------------
FUNS = {
    0: sum,
    1: prod,
    2: min,
    3: max,
    5: lambda x: (x[0] > x[1]) + 0,
    6: lambda x: (x[0] < x[1]) + 0,
    7: lambda x: (x[0] == x[1]) + 0,
}


def compute(binary_string):
    typeID = int(binary_string[3:6], 2)
    if typeID == 4:
        literal = parse_type_4(binary_string)
        # the length of the literal + one bit per group
        literal_len = len(literal) + len(literal) / 4
        # plus 6 bits for the header
        length_parsed = int(literal_len + 6)
        return literal, length_parsed  # int(literal, 2)
    else:
        lengthTypeID = binary_string[6]
        if lengthTypeID == "0":
            literals = []
            start_char = 7 + 15
            subPacketLeng = int(binary_string[7:start_char], 2)
            length_so_far = 0
            while length_so_far < subPacketLeng:
                literal, sub_length_parsed = compute(binary_string[start_char:])
                length_so_far += sub_length_parsed
                start_char += sub_length_parsed
                literals.append(literal)
            literals_int = [int(l, 2) for l in literals]
            result_int = FUNS[typeID](literals_int)
            print(
                typeID, "\t", literals_int, " \t result: ", result_int, "\n------------"
            )
            length_parsed = 7 + 15 + subPacketLeng
            return bin(result_int)[2:], length_parsed
        if lengthTypeID == "1":
            literals = []
            start_char = 7 + 11
            parsed_length = start_char
            subPacketCnt = int(binary_string[7:start_char], 2)
            for i in range(subPacketCnt):
                literal, sub_length_parsed = compute(binary_string[start_char:])
                start_char += sub_length_parsed
                literals.append(literal)
                parsed_length += sub_length_parsed
            literals_int = [int(l, 2) for l in literals]
            result_int = FUNS[typeID](literals_int)
            print(
                typeID, "\t", literals_int, " \t result: ", result_int, "\n------------"
            )
            return bin(result_int)[2:], parsed_length


print("Examples:")
for hex_packet in examples_part2:
    print("===============================================================")
    print(hex_packet)
    num_of_bits = int(len(hex_packet) * log2(16))
    full_binary_string = bin(int(hex_packet, 16))[2:].zfill(num_of_bits)
    result, length = compute(full_binary_string)
    print(int(result, 2))
    print("===============================================================")

print("\n" * 5)
print("Input:")
print("===============================================================")
num_of_bits = int(len(hex_packet_input) * log2(16))
full_binary_string = bin(int(hex_packet_input, 16))[2:].zfill(num_of_bits)
result, length = compute(full_binary_string)
print(int(result, 2))
print("===============================================================")

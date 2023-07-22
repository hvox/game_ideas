from math import log2, ceil

CHARSET = (
    "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_~"
    "!\"#$%&'()*+,-./:;<=>?@[\\]^`{|} "
    "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
)


BASES = {
    10: (8, 3),
    16: (8, 2),
    32: (40, 8),
    64: (24, 4),
    85: (32, 5),
    91: (13, 2),
    93: (85, 13),
    94: (72, 11),
    95: (256, 39),
    96: (79, 12),
    98: (33, 5),
    99: (53, 8),
    102: (20, 3),
    107: (128, 19),
    128: (7, 1),
}


def debug(string: str):
    print(string, end="")


def parse_int(string: str, base: int):
    number = 0
    for i, char in enumerate(reversed(string)):
        number += CHARSET.find(char) * base**i
    return number


def stringify_int(number: int, length: int, base: int):
    string = []
    for _ in range(length):
        string.append(CHARSET[number % base])
        number //= base
    return "".join(string)


def binary(data: bytes):
    binary = []
    for i in range(len(data) * 8):
        binary.append(str(data[i // 8] >> i % 8 & 1))
    return "".join(binary)


def encode(data: bytes, base: int):
    bits, chars = BASES[base]
    data_bits = binary(data)
    assert len(data_bits) % bits == 0
    code = []
    for i in range(0, len(data_bits), bits):
        number = int(data_bits[i: i + bits], 2)
        code.append(stringify_int(number, chars, base))
    return "".join(code)


def calculate_delta_per_byte(base):
    bits, chars = BASES[base]
    data = bytearray(range(256 // bits * bits))
    data_encoded = encode(data, base)
    counter = 0
    for i in range(0, len(data)):
        debug(f" \r{base} {i/len(data)*100:0.1f}%")
        for value in range(256):
            data[i] = value
            delta = {i for i, (x, y) in enumerate(zip(data_encoded, encode(data, base))) if x != y}
            counter += len(delta)
        data[i] = i
    return counter / len(data) / 256


def table_to_str(table: list[list[str]]) -> str:
    table = [[str(x) for x in row] for row in table]
    if not table or not table[0]:
        return ""
    column_widths = [0] * len(table[0])
    for row in table[1:]:
        for i, cell in enumerate(row):
            column_widths[i] = max(column_widths[i], len(cell))
    lines = ["  ".join(h.center(w) for h, w in zip(table[0], column_widths))]
    for row in table[1:]:
        line = []
        for header, cell, width in zip(table[0], row, column_widths):
            line.append(cell.rjust(width).center(len(header)))
        lines.append(" " + "  ".join(line))
    return " " + "\n".join(lines)


table = [["base", "cost", "η", "ch/kb", "Δ/B"]]
for base, (bits, chars) in BASES.items():
    kbyte = 8192 // bits * chars + ceil(8192 % bits / log2(base))
    # kbit = 1024 // bits * chars + ceil(1024 % bits / log2(base))
    delta_per_byte = calculate_delta_per_byte(base)
    efficiency = bits / chars / 8 * 100
    print(f"\r {base}", f"{8/(bits/chars) - 1:.1%}",
          f"{efficiency:5.2f}%", kbyte, f"{delta_per_byte:g}")
    table.append((base, f"{8/(bits/chars) - 1:.1%}",
                 f"{efficiency:5.2f}%", kbyte, f"{delta_per_byte:g}"))
print("\r" + table_to_str(table))

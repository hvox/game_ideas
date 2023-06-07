from collections import defaultdict
from math import gcd

STEAM_SURVEY_MAY_2023 = """
    1024 x 768 0.20% -0.02%
    1280 x 800 0.46% 0.00%
    1280 x 720 0.26% -0.01%
    1280 x 1024 0.57% -0.03%
    1360 x 768 0.96% +0.01%
    1366 x 768 5.22% -0.06%
    1440 x 900 1.95% +0.02%
    1600 x 900 1.40% -0.11%
    1680 x 1050 0.92% -0.04%
    1920 x 1200 0.71% 0.00%
    1920 x 1080 64.33% -0.19%
    2560 x 1080 0.87% -0.04%
    2560 x 1600 2.19% +0.07%
    2560 x 1440 12.88% +0.39%
    3440 x 1440 1.52% -0.06%
    3840 x 2160 2.68% -0.07%
""".strip("\n").split("\n")


def table_to_str(table: list[list[str]]) -> str:
    if not table or not table[0]:
        return ""
    column_widths = [0] * len(table[0])
    for row in table:
        for i, cell in enumerate(row):
            column_widths[i] = max(column_widths[i], len(cell))
    lines = []
    for i, row in enumerate(table):
        line = []
        for cell, width in zip(row, column_widths):
            line.append(cell.rjust(width) if i else cell.center(width))
        lines.append(" " + "  ".join(line))
    return "\n".join(lines)


frequencies = defaultdict(lambda: 0)
for line in STEAM_SURVEY_MAY_2023:
    width, _, height, freq, _ = line.strip().split(" ")
    w, h = map(int, (width, height))
    ratio = (w // gcd(w, h), h // gcd(w, h))
    frequencies[ratio] += int(freq[:-1].replace(".", ""))
table = [["freq", "w&h", "err"]]
for (w, h), freq in reversed(sorted(frequencies.items(), key=lambda item: item[1])):
    err = abs(w / h - 16 / 9) * 100
    table.append([f"{freq/100:0.2f}%", f"{w}:{h}", f"{err:0.1f}%"])
print(table_to_str(table))

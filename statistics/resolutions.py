from collections import defaultdict
from math import gcd, ceil

STEAM_SURVEY_MAY_2023 = """
    1280 x 720 0.22% 0.00%
    1280 x 800 0.52% +0.08%
    1280 x 1024 0.34% -0.03%
    1360 x 768 0.62% -0.01%
    1366 x 768 3.46% -0.10%
    1440 x 900 1.03% -0.01%
    1600 x 900 0.99% -0.04%
    1680 x 1050 0.62% -0.04%
    1920 x 1080 58.45% -0.37%
    1920 x 1200 1.05% -0.02%
    2560 x 1600 2.89% -0.25%
    2560 x 1080 0.89% 0.00%
    2560 x 1440 19.86% +0.87%
    2880 x 1800 0.26% 0.00%
    3440 x 1440 2.11% -0.02%
    3840 x 2160 3.44% -0.10%
    5120 x 1440 0.28% +0.01%
""".strip(
    "\n"
).split(
    "\n"
)


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


fit_resolution = [160, 90]
fat_resolution = fit_resolution.copy()
frequencies = defaultdict(lambda: 0)
for line in STEAM_SURVEY_MAY_2023:
    width, _, height, freq, _ = line.strip().split(" ")
    freq = int(freq[:-1].replace(".", ""))
    w, h = map(int, (width, height))
    ratio = (w // gcd(w, h), h // gcd(w, h))
    pixel_size = min(w // fit_resolution[0], h // fit_resolution[1])
    fat_resolution[0] = max(fat_resolution[0], ceil(w / pixel_size))
    fat_resolution[1] = max(fat_resolution[1], ceil(h / pixel_size))
    print(f"{freq/100:6} {f"{w}:{h}":>9} -> {ceil(w/pixel_size)}x{ceil(h/pixel_size)}")
    frequencies[ratio] += freq
print("Recommended resolution:",
      f"fit={fit_resolution[0]}x{fit_resolution[1]}, "
      f"fat={fat_resolution[0]}x{fat_resolution[1]}")
table = [["freq", "w&h", "err", "w/h"]]
for (w, h), freq in reversed(sorted(frequencies.items(), key=lambda item: item[1])):
    err = abs(w / h - 16 / 9) * 100
    table.append([f"{freq/100:0.2f}%", f"{w}:{h}", f"{err:0.1f}%", f"{w/h:0.3f}"])
print(table_to_str(table))

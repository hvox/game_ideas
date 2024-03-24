from itertools import islice
from time import monotonic as time
from random import shuffle


def bit(mask: int, index: int):
    return bool((mask >> (index - 1)) & 1)


TILES = [0] * 2 + list(
    mask
    for mask in range(256)
    if bit(mask, 1) <= bit(mask, 2) & bit(mask, 4)
    and bit(mask, 3) <= bit(mask, 2) & bit(mask, 5)
    and bit(mask, 6) <= bit(mask, 4) & bit(mask, 7)
    and bit(mask, 8) <= bit(mask, 7) & bit(mask, 5)
)


def chunked(iterable, n: int):
    it = iter(iterable)
    while chunk := list(islice(it, n)):
        yield chunk


def print_grid(grid: list[int]):
    for row in reversed(list(chunked(grid, 7))):
        up = "".join("".join("░█"[bit(x, i)] * 2 for i in (6, 7, 8)) for x in row)
        mid = "".join("▓▓".join("░█"[bit(x, i)] * 2 for i in (4, 5)) for x in row)
        down = "".join("".join("░█"[bit(x, i)] * 2 for i in (1, 2, 3)) for x in row)
        print("\n".join((up, mid, down)))


def is_grid_tilable(grid: list[int]) -> bool:
    return True
    for y in range(4):
        row = grid[y * 4: y * 4 + 4]
        if row[0] & 1 != (row[3] & 2) // 2 or (row[0] & 4) // 4 != (row[3] & 8) // 8:
            return False
    for x in range(4):
        col = [grid[x + y * 4] for y in range(4)]
        if bool(col[3] & 4) != bool(col[0] & 1) or bool(col[3] & 8) != bool(col[0] & 2):
            return False
    return True


def search():
    def f(i: int, tiles: list[int]):
        x = i % 7
        y = i // 7
        if y == 7:
            yield list(grid)
            return
        if grid[i] != -1:
            yield from f(i + 1, tiles)
            return
        # if i == 48: print(bytes(grid[:i]).hex() + "--" * (49 - i))
        for j, t in enumerate(tiles):
            left = grid[x - 1 + y * 7] if x > 0 else 0
            if bit(t, 1) != bit(left, 3) or bit(t, 4) != bit(left, 5) or bit(t, 6) != bit(left, 8):
                continue
            down = grid[x + (y - 1) * 7] if y > 0 else 0
            if bit(t, 1) != bit(down, 6) or bit(t, 2) != bit(down, 7) or bit(t, 3) != bit(down, 8):
                continue
            grid[i] = t
            yield from f(i + 1, tiles[:j] + tiles[j + 1:])
        grid[i] = -1

    grid = [-1] * 49
    grid[48] = grid[6] = grid[0 + 6 * 7] = 0
    return f(0, list(sorted(set(TILES) - {0})))


t0 = time()
grids = []
try:
    for i, grid in enumerate(search()):
        grids.append(grid)
        print(i, ":", grid)
        print_grid(grid)
except KeyboardInterrupt:
    pass
dt = time() - t0
j = 0
# for i, grid in enumerate(sorted(grids), 1):
#     if not is_grid_tilable(grid):
#         continue
#     j += 1
#     print("\n", i, " : ", j, " : ", grid, end="\n\n")
#     print_grid(grid)
print(f"\nBtw the algorithm found {len(grids)} grids in {dt:.2f} seconds.")
print(f"This is {dt/len(grids)*10**3:.0f} ms per grid!")

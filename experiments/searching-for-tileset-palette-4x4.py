import random
from itertools import product

tiles = "  :▄ : ▄:▄▄:▀ :█ :▀▄:█▄: ▀:▄▀: █:▄█:▀▀:█▀:▀█:██".split(":")


def print_grid(grid: list[int]):
    for i in range(0, 16, 4):
        print("".join(tiles[i] for i in grid[i: i + 4]))


def check_grid(grid: list[int]):
    rows = [grid[i: i + 4] for i in range(0, 16, 4)]
    for x, y in product(range(4), repeat=2):
        if x > 0 and rows[y][x] & 1 != (rows[y][x - 1] & 2) // 2:
            return False
        if x > 0 and (rows[y][x] & 4) // 4 != (rows[y][x - 1] & 8) // 8:
            return False
        if y > 0 and (rows[y][x] & 4) // 4 != (rows[y - 1][x] & 1) // 1:
            return False
        if y > 0 and (rows[y][x] & 8) // 8 != (rows[y - 1][x] & 2) // 2:
            return False
    return True


def search():
    def f(i: int):
        x = i % 4
        y = i // 4
        for cell in range(16):
            if cell in grid:
                continue
            if x > 0:
                left = grid[x - 1 + y * 4]
                if cell & 1 != (left & 2) // 2 or cell & 4 != (left & 8) // 2:
                    continue
            if y > 0:
                up = grid[x + (y - 1) * 4]
                if (cell & 4) // 4 != up & 1 or (cell & 8) // 4 != up & 2:
                    continue
            grid[i] = cell
            if i == 15:
                yield list(grid)
            yield from f(i + 1)
            grid[i] = -1
    grid = [-1] * 16
    return f(0)


for i, grid in enumerate(search(), 1):
    assert check_grid(grid)
    print("\n", i)
    print_grid(grid)

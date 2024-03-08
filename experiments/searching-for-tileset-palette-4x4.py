from itertools import product

# mask:  0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
tiles = "  :▄ : ▄:▄▄:▀ :█ :▀▄:█▄: ▀:▄▀: █:▄█:▀▀:█▀:▀█:██".split(":")


def print_grid(grid: list[int]):
    eor = "\x1b[0m"
    for i in range(0, 16, 4):
        print(end="\x1b[97m\x1b[40m")
        row = "".join(tiles[j] for _ in range(9) for j in grid[i: i + 4])
        print(row + eor)


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


def is_grid_tilable(grid: list[int]) -> bool:
    for y in range(4):
        row = grid[y * 4: y * 4 + 4]
        if row[0] & 1 != (row[3] & 2) // 2 or (row[0] & 4) // 4 != (row[3] & 8) // 8:
            return False
    for x in range(4):
        col = [grid[x + y * 4] for y in range(4)]
        if bool(col[0] & 4) != bool(col[3] & 1) or bool(col[0] & 8) != bool(col[3] & 2):
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


j = 0
for i, grid in enumerate(sorted(search()), 1):
    assert check_grid(grid)
    if not is_grid_tilable(grid):
        continue
    j += 1
    print("\n", i, " : ", j, " : ", grid)
    for _ in range(10):
        print_grid(grid)

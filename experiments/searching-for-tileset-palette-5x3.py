from time import monotonic as time

# mask:      0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
TILES_STR = "  :▄ : ▄:▄▄:▀ :█ :▀▄:█▄: ▀:▄▀: █:▄█:▀▀:█▀:▀█:██".split(":")
TILES = list(range(1, 16))
w, h = 5, 3


def print_grid(grid: list[int]):
    eor = "\x1b[0m"
    for i in reversed(range(0, w * h, w)):
        print(end="\x1b[97m\x1b[40m")
        row = "".join(TILES_STR[j] for _ in range(1) for j in grid[i: i + w])
        print(row + eor)


def is_grid_tilable(grid: list[int]) -> bool:
    for y in range(h):
        row = grid[y * w: y * w + w]
        if row[0] & 1 != (row[-1] & 2) // 2 or (row[0] & 4) // 4 != (row[-1] & 8) // 8:
            return False
    for x in range(w):
        col = [grid[x + y * w] for y in range(h)]
        if bool(col[-1] & 4) != bool(col[0] & 1) or bool(col[-1] & 8) != bool(col[0] & 2):
            return False
    return True


def search():
    def f(i: int):
        if i == w * h:
            yield list(grid)
            return
        x = i % w
        y = i // w
        for cell in TILES:
            if cell in grid:
                continue
            if x > 0:
                left = grid[x - 1 + y * w]
                if cell & 1 != (left & 2) // 2 or cell & 4 != (left & 8) // 2:
                    continue
            if y > 0:
                down = grid[x + (y - 1) * w]
                if (down & 4) // 4 != cell & 1 or (down & 8) // 4 != cell & 2:
                    continue
            grid[i] = cell
            yield from f(i + 1)
            grid[i] = -1

    grid = [-1] * 16
    return f(0)


t0 = time()
grids = list(search())
dt = time() - t0
j = 0
for i, grid in enumerate(sorted(grids), 1):
    if not is_grid_tilable(grid):
        continue
    j += 1
    print("\n", i, " : ", j, " : ", grid, end="\n\n")
    for _ in range(1):
        print_grid(grid)
print(f"\nBtw the algorithm found {len(grids)} grids in {dt:.2f} seconds.")
print(f"This is {dt/len(grids)*10**6:.0f} μs per grid!")

from itertools import product


def is_continuous(grid: tuple[int, ...]) -> bool:
    if 1 not in grid:
        return False
    i = next(i for i, x in enumerate(grid) if x)
    queue, visited = [i], {i}
    while queue:
        i = queue.pop()
        if i % 3 > 0 and grid[i - 1] and i - 1 not in visited:
            visited.add(i - 1)
            queue.append(i - 1)
        if i % 3 < 2 and grid[i + 1] and i + 1 not in visited:
            visited.add(i + 1)
            queue.append(i + 1)
        if i // 3 > 0 and grid[i - 3] and i - 3 not in visited:
            visited.add(i - 3)
            queue.append(i - 3)
        if i // 3 < 2 and grid[i + 3] and i + 3 not in visited:
            visited.add(i + 3)
            queue.append(i + 3)
    return len(visited) == sum(grid)


def distinct_continuous_grids() -> set[tuple[int, ...]]:
    grids = set()
    for grid in product(range(2), repeat=9):
        if not is_continuous(grid):
            continue
        holed_grid = list(grid)
        holed_grid[4] = 0
        if is_continuous(tuple(holed_grid)):
            grids.add(tuple(holed_grid))
        else:
            grids.add(grid)
    return grids


# for grid in product(range(2), repeat=9):
#     print(["", "continuous"][is_continuous(grid)])
#     print(grid[:3])
#     print(grid[3:6])
#     print(grid[6:])
counter = sum(map(is_continuous, product(range(2), repeat=9)))
print("Continious grids 3x3:", counter)
print("When ignoring center:", len(distinct_continuous_grids()))

from itertools import product


def is_continuous(grid: tuple[int, ...], w: int, h: int) -> bool:
    if 1 not in grid:
        return False
    i = next(i for i, x in enumerate(grid) if x)
    queue, visited = [i], {i}
    while queue:
        i = queue.pop()
        if i % w > 0 and grid[i - 1] and i - 1 not in visited:
            visited.add(i - 1)
            queue.append(i - 1)
        if i % w < w - 1 and grid[i + 1] and i + 1 not in visited:
            visited.add(i + 1)
            queue.append(i + 1)
        if i // w > 0 and grid[i - w] and i - w not in visited:
            visited.add(i - w)
            queue.append(i - 3)
        if i // w < h - 1 and grid[i + w] and i + w not in visited:
            visited.add(i + w)
            queue.append(i + w)
    return len(visited) == sum(grid)


def continuous_grids(w: int, h: int) -> set[tuple[int, ...]]:
    grids = set()
    for grid in product(range(2), repeat=w*h):
        if is_continuous(grid, w, h):
            grids.add(grid)
    return grids


# for grid in product(range(2), repeat=6):
#     print(["", "continuous"][is_continuous(grid, 2, 3)])
#     print(grid[:2])
#     print(grid[2:4])
#     print(grid[4:])
width, height = 2, 3
grids = continuous_grids(width, height)
print(f"Continious grids {width}x{height}:", len(grids))
print("If we add one fully empty block:", 1 + len(grids))

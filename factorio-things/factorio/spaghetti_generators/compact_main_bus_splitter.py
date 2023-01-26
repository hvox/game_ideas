from ..entities import Entities, EntityAttributes, belt, underground, assembler, splitter
from fractions import Fraction
from dataclasses import dataclass
from typing import Self
import itertools


def get_line_left(lines: list[tuple[str, int]], material: str) -> tuple[int, int]:
    x = 0
    for i, (line, width) in enumerate(lines):
        if line == material:
            return i, x
        x += width + 2
    raise ValueError(f"{material} not found in the main bus")


def main_bus(lines: list[tuple[str, int]], splits: list[list[str | None]]) -> Entities:
    entities: Entities = {}
    y0 = 0
    # x1 = (len(lines) - 1) * 2 + sum(width for _, width in lines)
    y1 = sum(len(split) + 1 for split in splits) - 1
    for y in range(y0 - 4, y1 + 4):
        x = 0
        for material, width in lines:
            for dx in range(width):
                entities[x + dx + 0.5, y + 0.5] = belt(1, 0)
            x += width + 2
    for split in splits:
        if len(split) == 0:
            y0 += 1
            continue
        *inputs, output = split
        for input in inputs:
            if input is None:
                y0 += 1
                continue
            index, x = get_line_left(lines, input)
            _, width = lines[index]
            if (x + width - 0.5, y0 - 0.5) in entities:
                del entities[x + width - 0.5, y0 - 0.5]
                entities[x + width, y0 - 0.5] = splitter(1, 1, 0, 1)
            else:
                entities[x + width, y0 - 0.5] = splitter(1, 1, 1, 1)
            for dx in range(1, width):
                del entities[x + width - dx - 0.5, y0 + dx - 0.5]
                del entities[x + width - dx + 0.5, y0 + dx - 0.5]
                entities[x + width - dx, y0 + dx - 0.5] = splitter(1, 1, 0, 1)
            x += width + 1
            entities[x - 0.5, y0 + 0.5] = belt(1, 2)
            for _, width in lines[index+1:]:
                left, right = underground(1, 2)
                entities[x + 0.5, y0 + 0.5] = left
                x += width + 2
                entities[x - 0.5, y0 + 0.5] = right
            y0 += 1
        if output is None:
            y0 += 2
            continue
        index, x = get_line_left(lines, output)
        _, width = lines[index]
        del entities[x + width - 0.5, y0 + 1.5]
        entities[x + width, y0 + 1.5] = splitter(1, 0, 1, -1, output)
        # TODO: check if top-going splitters work here as good as at inputs
        for dx in range(1, width):
            del entities[x + width - dx - 0.5, y0 - dx + 1.5]
            del entities[x + width - dx + 0.5, y0 - dx + 1.5]
            entities[x + width - dx, y0 - dx + 1.5] = splitter(1, 1, 0, 1)
        x += width + 1
        entities[x - 0.5, y0 + 0.5] = belt(1, 0)
        for _, width in lines[index+1:]:
            input, output = underground(1, -2)
            entities[x + 0.5, y0 + 0.5] = output
            x += width + 2
            entities[x - 0.5, y0 + 0.5] = input
        y0 += 2
    return entities

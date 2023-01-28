from fractions import Fraction
from math import ceil
from ...recipes import MATERIALS, RECIPES
from ...entities import Entities
from ...calculator import get_total_assembly_made
from ..compact_main_bus_splitter import main_bus
from ..assemly_line_generator import assembly_line


BELT_SPEED = 15

# TODO: I am fucking here...
# I was trying to put together assembly line genaration and main bus splitter4
# Also it might as well do calculations about what intermideate ingridients are needed and
# in what amounts.


def design(*products: dict[str, Fraction]) -> Entities:
    main_bus_materials = get_total_assembly_made(*products)
    assert all(amount < 4 * BELT_SPEED for amount in main_bus_materials.values())
    main_bus_lines = [(mat, ceil(x / 15)) for mat, x in reversed(main_bus_materials.items())]
    splits: list[list[str | None]] = []
    entites: Entities = {}
    x0 = (len(main_bus_lines) - 1) * 2 + sum(width for _, width in main_bus_lines)
    y0 = -1
    for product, amount in main_bus_materials.items():
        if product not in RECIPES or RECIPES[product].facility != "assembler":
            continue
        split, line = assembly_line(product, amount)
        for (x, y), entity in line.items():
            entites[x0 + x, y0 + y] = entity
        splits.append(split)
        y0 += len(split) + 1
    for pos, entity in main_bus(main_bus_lines, splits).items():
        entites[pos] = entity
    return entites

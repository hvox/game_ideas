from ..entities import Entities, belt, underground, assembler, splitter, inserter, electric_pole
from fractions import Fraction
from ..recipes import Recipe, RECIPES, MATERIALS
from dataclasses import dataclass
from typing import Self, Any
from math import ceil
import itertools


BELT_THROUGHPUT = 15
ASSEMBLY_SPEED = Fraction("0.75")
MAX_INSERTER_SPEED = Fraction("2.25")  # TODO: add support for fast inserters


def assembly_line(product: str, throughput: Fraction) -> tuple[list[str | None], Entities]:
    if throughput > BELT_THROUGHPUT:
        raise ValueError("Throughput of output material is unachievable")
    recipe = RECIPES[product]
    inputs = {inp: recipe.ingredients[inp] * throughput for inp in sorted(
        (inp for inp, _ in recipe.ingredients.items()), key=lambda x: MATERIALS[x])}
    if any(throughput > BELT_THROUGHPUT for throughput in inputs.values()):
        raise ValueError("Throughput of input material is unachievable")
    main_bus_splitter_configuration: list[str | None]
    match list(inputs):
        case [inp1]:
            main_bus_splitter_configuration = [None, None, None, inp1, product]
        case [inp1, inp2]:
            main_bus_splitter_configuration = [inp1, None, None, None, None, inp2, product]
        case [inp1, inp2, inp3]:
            main_bus_splitter_configuration = [inp1, inp2, None, None, None, None, inp3, product]
        case _:
            # TODO: Support four input recipes using inner splitter
            raise ValueError(f"Unsupported number of inputs: {len(inputs)}")
    assembly_throughput = min(ASSEMBLY_SPEED / recipe.creation_time, MAX_INSERTER_SPEED)
    for ingridient_amount in recipe.ingredients.values():
        ingridient_throughput = MAX_INSERTER_SPEED / ingridient_amount
        assembly_throughput = min(assembly_throughput, ingridient_throughput)
    assemblers = ceil(throughput / assembly_throughput / 2) * 2
    print(f"assemblers for {product}:", float(throughput / assembly_throughput), "->", assemblers)
    # Assembly bottom left
    x0 = 1 if len(inputs) < 4 else 4
    y0 = (len(inputs) > 1) + len(inputs) - 1
    # Assembly top right
    x1, y1 = x0 + 3 * assemblers, y0 + 3
    entities: Entities = {}
    entities[x0 - 0.5, y1 + 2.5] = belt(1, -2)  # output
    entities[x0 - 0.5, y1 + 1.5] = belt(1, 2)  # inputs[-1]
    if len(inputs) > 1:
        entities[x0 - 0.5, y0 - 0.5] = belt(1, 2)  # inputs[-2]
        entities[x0 + 0.5, y0 - 0.5] = belt(1, 4)
    if len(inputs) > 2:
        entities[x0 - 0.5, y0 - 1.5] = belt(1, 4)  # inputs[-3]
        entities[x0 - 0.5, y0 - 2.5] = belt(1, 2)
    inserters: list[Entities] = [{} for _ in range(len(inputs) + 1)]
    if assemblers % 4 != 2:
        entities[x0 + 0.5, y0 + 4.5] = underground(1, 2)[0]
    for i in range(0, assemblers, 2):
        x, y = x0 + 3 * i, y0
        for dx in range(6):
            entities[x + dx + 0.5, y + 5.5] = belt(1, -2)
        entities[x + 3.5, y + 3.5] = electric_pole(1)
        entities[x + 1.5, y + 1.5] = assembler(2, product, 0)
        entities[x + 4.5, y + 1.5] = assembler(2, product, 0)
        if assemblers % 4 == 2:
            entities[x + 0.5, y + 4.5] = belt(1, 2)
            inserters[-1][x + 1.5, y + 3.5] = inserter(1, 0)
            entities[x + 1.5, y + 4.5], entities[x + 5.5, y + 4.5] = underground(1, 2)
            inserters[-2][x + 2.5, y + 3.5] = inserter(1, 4)
            entities[x + 2.5, y + 4.5] = belt(1, 0)
            inserters[-2][x + 4.5, y + 3.5] = inserter(1, 4)
            entities[x + 4.5, y + 4.5] = belt(1, 0)
            inserters[-1][x + 5.5, y + 3.5] = inserter(1, 0)
        else:
            inserters[-2][x + 1.5, y + 3.5] = inserter(1, 4)
            entities[x + 1.5, y + 4.5] = belt(1, 0)
            inserters[-1][x + 2.5, y + 3.5] = inserter(1, 0)
            entities[x + 4.5, y + 4.5], entities[x + 2.5, y + 4.5] = underground(1, 2)
            entities[x + 3.5, y + 4.5] = belt(1, 2)
            inserters[-1][x + 4.5, y + 3.5] = inserter(1, 0)
            inserters[-2][x + 5.5, y + 3.5] = inserter(1, 4)
            entities[x + 5.5, y + 4.5] = belt(1, 0)
    for i in range(0, assemblers, 2):
        x, y = x0 + 3 * i, y0
        if len(inputs) == 2:
            y2 = y - 2  # bottom of inputs[-2]
            entities[x + 0.5, y2 + 0.5] = belt(1, 2)
            entities[x + 1.5, y2 + 0.5] = belt(1, 2)
            inserters[-3][x + 1.5, y2 + 1.5] = inserter(1, 4)
            entities[x + 2.5, y2 + 0.5] = belt(1, 2)
            entities[x + 3.5, y2 + 0.5] = belt(1, 2)
            entities[x + 3.5, y2 + 1.5] = electric_pole(1)
            entities[x + 4.5, y2 + 0.5] = belt(1, 2)
            inserters[-3][x + 4.5, y2 + 1.5] = inserter(1, 4)
            entities[x + 5.5, y2 + 0.5] = belt(1, 2)
        elif len(inputs) == 3:
            y3 = y - 3  # bottom of inputs[-3]
            entities[x + 0.5, y3 + 0.5] = belt(1, 2)
            entities[x + 0.5, y3 + 1.5] = belt(1, 2)
            entities[x + 1.5, y3 + 0.5] = belt(1, 2)
            entities[x + 1.5, y3 + 1.5], entities[x + 5.5, y3 + 1.5] = underground(1, 2)
            inserters[-3][x + 1.5, y3 + 2.5] = inserter(1, 4)
            entities[x + 2.5, y3 + 0.5] = belt(1, 0)
            entities[x + 2.5, y3 + 1.5] = belt(1, 2)
            inserters[-4][x + 2.5, y3 + 2.5] = inserter(1, 4)
            entities[x + 3.5, y3 + 1.5] = belt(1, 2)
            entities[x + 3.5, y3 + 2.5] = electric_pole(1)
            entities[x + 4.5, y3 + 0.5] = belt(1, 2)
            entities[x + 4.5, y3 + 1.5] = belt(1, 4)
            inserters[-4][x + 4.5, y3 + 2.5] = inserter(1, 4)
            entities[x + 5.5, y3 + 0.5] = belt(1, 2)
            inserters[-3][x + 5.5, y3 + 2.5] = inserter(1, 4)
    x, y = x0 + assemblers // 2 * 3, y0 + 4
    entities[x - 0.5, y + 0.5] = belt(1, 2)
    entities[x + 0.5, y + 0.5] = belt(1, 0)
    entities[x + 1.5, y + 0.5] = belt(1, -2)
    entities[x + 1.5, y + 1.5] = belt(1, 4)
    if assemblers == 2:
        del entities[x1 - 1.5, y1 + 2.5]
        del entities[x1 - 0.5, y1 + 2.5]
    for pos, entity in (pair for group in inserters for pair in group.items()):
        entities[pos] = entity
    return main_bus_splitter_configuration, entities

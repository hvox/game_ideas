from ..materials import Material
from fractions import Fraction
from dataclasses import dataclass
from typing import Self

BELT_SPEED = Fraction("15")
BELT = "transport-belt"

Entities = dict[tuple[float, float], tuple[str, dict[str, int | str]]]


@dataclass
class MainBus:
    lines: list[tuple[Material, Fraction]]

    def split_out(self, lines: list[tuple[Material, Fraction]]) -> Entities:
        assert all(amount <= BELT_SPEED for _, amount in lines)
        entities: Entities = {}
        for y, (material, amount) in enumerate(lines):
            # TODO: I am here trying to split each material individualy
            ...

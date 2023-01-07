from ..materials import Material
from fractions import Fraction
from dataclasses import dataclass
import itertools

BELT_SPEED = Fraction("15")
BELT = "transport-belt"
UNDERGROUND_BELT = "underground-belt"
SPLITTER = "splitter"

Entities = dict[tuple[float, float], tuple[str, dict[str, int | str]]]


@dataclass
class MainBus:
    lines: list[tuple[Material, Fraction]]

    def split_out(self, lines: list[tuple[Material, Fraction]]) -> Entities:
        assert all(amount <= BELT_SPEED for _, amount in lines)
        entities: Entities = {}
        for y, (target_material, target_amount) in enumerate(lines):
            y *= 2
            for x, (material, amount) in enumerate(self.lines):
                if target_material == material:
                    break
                for dx, dy in itertools.product((1.5, 2.5), (0.5, 1.5)):
                    entities[4 * x + dx, y + dy] = (BELT, {"direction": 0})
            # TODO: use target amounts for more accurate splitting
            entities[4*x + 1.5, y + 0.5] = (BELT, {"direction": 0})
            splitter = (SPLITTER, {"direction": 0})
            if target_amount > BELT_SPEED / 2:
                splitter[1]["output_priority"] = "right"
            entities[4*x + 3.0, y + 0.5] = splitter
            entities[4*x + 2.0, y + 1.5] = (SPLITTER, {"direction": 0, "output_priority": "right"})
            entities[4*x + 3.5, y + 1.5] = (BELT, {"direction": 2})
            assert amount >= target_amount
            self.lines[x] = (material, amount - target_amount)
            for x, (material, amount) in enumerate(self.lines[x + 1:], x + 1):
                for dx, dy in itertools.product((1.5, 2.5), (0.5, 1.5)):
                    entities[4 * x + dx, y + dy] = (BELT, {"direction": 0})
                inp = (UNDERGROUND_BELT, {"direction": 2, "type": "input"})
                out = (UNDERGROUND_BELT, {"direction": 2, "type": "output"})
                entities[4 * x + 0.5, y + 1.5] = inp
                entities[4 * x + 3.5, y + 1.5] = out
        return entities

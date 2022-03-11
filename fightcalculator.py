import dataclasses


@dataclasses.dataclass
class Squad:
    warriors: int
    health_per_unit: float
    damage_per_second: float

    def __matmul__(self, other):
        units1, h1, dps1 = dataclasses.astuple(self)
        units2, h2, dps2 = dataclasses.astuple(other)
        th1, th2 = h1 * units1, h2 * units2
        th1 = max(0, th1 - units2 * dps2)
        th2 = max(0, th2 - units1 * dps1)
        return Squad(th1 / h1, h1, dps1), Squad(th2 / h2, h2, dps2)

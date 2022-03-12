# If we currently have two fighting squads of health A and B, DPS of α and β.
# Then after some time τ we will have this situation:
# A(τ) = ((A(0) - B(0)√(β/α)) * e^(τ*√(αβ)) + (A(0) + B(0)√(β/α)) * e^(-τ*√(αβ))) / 2
# B(τ) = ((B(0) - A(0)√(α/β)) * e^(τ*√(αβ)) + (B(0) + A(0)√(α/β)) * e^(-τ*√(αβ))) / 2
# Using the equations above we can find such τ = δ so that B(τ) = 0.
# δ = ln( (A*√α + B*√β) / √(α*A(0)^2 - β*B(0)^2) ) / √(αβ)
# And using this δ we can find A(δ) at the moment δ when B(δ) = 0.
# A(δ) = ((A(0) - B(0)√(β/α)) * (A*√α + B*√β) / √(α*A(0)^2 - β*B(0)^2) + (A(0) + B(0)√(β/α)) / (A*√α + B*√β) / √(α*A(0)^2 - β*B(0)^2)) / 2
#      = A(0) * √(1 - β*B(0)^2 / (α*A(0)^2))
# Or simply:
# A(δ) = A(0) * √(1 - φ/π), where φ = β*B(0)^2 and π = α*A(0)^2


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

    def fight_to_death(self, other):
        units1, h1, dps1 = dataclasses.astuple(self)
        units2, h2, dps2 = dataclasses.astuple(other)
        th1, td1 = units1 * h1, units1 * dps1
        th2, td2 = units2 * h2, units2 * dps2
        if th1 * td1 < th2 * td2:
            return tuple(reversed(other.fight_to_death(self)))
        units1 *= (1 - (th2 * td2) / (th1 * td1)) ** 0.5
        return Squad(units1, h1, dps1), Squad(0, h2, dps2)

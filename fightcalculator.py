# If we have two fighting squads with such stats:
# Total health of units of squad #1: A.
# Total damage per second of squad #1: α.
# Total health of units of squad #2: B.
# Total damage per second of squad #2: β.
#
# Then after some time τ we will have this situation:
# A(τ) = ((A - B√(Aβ/αB)) * e^(τ*√(αβ/AB)) + (A + B√(Aβ/αB)) * e^(-τ*√(αβ/AB))) / 2
# B(τ) = ((B - A√(Bα/βA)) * e^(τ*√(αβ/AB)) + (B + A√(Bα/βA)) * e^(-τ*√(αβ/AB))) / 2
# Or in terms of hyperbolic functions:
# A(τ) = A * ch(τ * √(αβ/AB)) - B√(Aβ/αB) * sh(τ * √(αβ/AB))
# B(τ) = B * ch(τ * √(αβ/AB)) - A√(Bα/βA) * sh(τ * √(αβ/AB))
#
# Assume Aα > Bβ, therefore squad #1 is going to win.
# Using the equations above we can find such τ = δ so that B(τ) = 0.
# δ =  √(AB/αβ) * ln((√(Aα) + √(Bβ)) / √(Aα - Bβ))
#
# And using this δ we can find A(δ) at the moment δ when B(δ) = 0.
# A(δ) = A * √(1 - Bβ/Aα)


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

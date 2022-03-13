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


from math import log, cosh as ch, sinh as sh
import dataclasses


@dataclasses.dataclass
class Squad:
    warriors: int
    health_per_unit: float
    damage_per_second: float

    def stats(self):
        total_health = self.warriors * self.health_per_unit
        total_dps = self.warriors * self.damage_per_second
        return (total_health, total_dps)

    def __mul__(self, factor):
        health = self.health_per_unit
        dps = self.damage_per_second
        return Squad(self.warriors * factor, health, dps)

    def __matmul__(self, other):
        (health1, dps1), (health2, dps2) = self.stats(), other.stats()
        new_health1 = max(0, health1 - dps2)
        new_health2 = max(0, health2 - dps1)
        return self * (new_health1 / health1), other * (new_health2 / health2)

    def time_to_death(self, other):
        (th1, td1), (th2, td2) = self.stats(), other.stats()
        t = (th1 * th2 / td1 / td2) ** 0.5
        f1, f2 = reversed(sorted((th1 * td1, th2 * td2)))
        return t * log((f1**0.5 + f2**0.5) / (f1 - f2) ** 0.5)

    def fight(self, other, delta_time=1):
        (A, α), (B, β) = self.stats(), other.stats()
        x = delta_time * (α * β / A / B) ** 0.5
        new_A = A * ch(x) - B * (A / B * β / α) ** 0.5 * sh(x)
        new_B = B * ch(x) - A * (B / A * α / β) ** 0.5 * sh(x)
        return self * (new_A / A), other * (new_B / B)

    def fight_to_death(self, other):
        (th1, td1), (th2, td2) = self.stats(), other.stats()
        if th1 * td1 < th2 * td2:
            return tuple(reversed(other.fight_to_death(self)))
        return self * (1 - (th2 * td2) / (th1 * td1)) ** 0.5, other * 0

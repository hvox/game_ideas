# If we have two fighting squads with such stats:
# Total health of units of squad #1: A.
# Total damage per second of squad #1: α.
# Total health of units of squad #2: B.
# Total damage per second of squad #2: β.
#
# At every moment every squad gets damage from another one.
# dA(τ)/dτ = -β * B(τ) / B
# dB(τ)/dτ = -α * A(τ) / A
#
# Solving the system above we get dependence of squad total health on
# the duration of the fight.
# In other words after some time τ we will have these total healths:
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
    units: int
    total_health: float
    total_damage_per_second: float

    def stats(self):
        total_health = self.total_health
        total_dps = self.total_damage_per_second
        return (total_health, total_dps, total_health * total_dps)

    def __mul__(self, factor):
        health = self.total_health * factor
        dps = self.total_damage_per_second * factor
        return Squad(self.units * factor, health, dps)

    def __matmul__(self, other):
        (A, α, _), (B, β, _) = self.stats(), other.stats()
        new_A = max(0, A - β)
        new_B = max(0, B - α)
        return self * (new_A / A), other * (new_B / B)

    def time_to_death(self, other):
        (A, α, αA), (B, β, βB) = self.stats(), other.stats()
        t = (A / α * B / β) ** 0.5
        return t * log((αA**0.5 + βB**0.5) / abs(αA - βB) ** 0.5)

    def fight(self, other, delta_time=1):
        (A, α, αA), (B, β, βB) = self.stats(), other.stats()
        x = delta_time * (α * β / A / B) ** 0.5
        new_A = A * ch(x) - B * (A / B * β / α) ** 0.5 * sh(x)
        new_B = B * ch(x) - A * (B / A * α / β) ** 0.5 * sh(x)
        return self * (new_A / A), other * (new_B / B)

    def fight_to_death(self, other):
        (A, α, αA), (B, β, βB) = self.stats(), other.stats()
        if αA < βB:
            return tuple(reversed(other.fight_to_death(self)))
        return self * (1 - βB / αA) ** 0.5, other * 0

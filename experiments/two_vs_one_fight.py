# Guys #1 and #2  VS  guy #3
#
# Guy #1:
#   attack: α
#   health: A
# Guy #2:
#   attack: β
#   health: B
# Guy #3:
#   attack: χ
#   health: C
#
# dA(τ)/dτ = -χ * C(τ) / C * A/(A+B)
# dB(τ)/dτ = -χ * C(τ) / C * B/(A+B)
# dC(τ)/dτ = -α * A(τ) / A - β * B(τ) / B
#
# The situation is absolute equivalent of two guys with stats
# (α+β, A+B) and (χ, C) respectively.

from math import inf, sqrt, log as ln, cosh as ch, sinh as sh
from random import randint


def f2(Aα, Bβ, τ):
    (A, α), (B, β), r = Aα, Bβ, sqrt
    return A * ch(τ * r(α * β / A / B)) - B * r(A * β / α / B) * sh(
        τ * r(α * β / A / B)
    ), B * ch(τ * r(α * β / A / B)) - A * r(B * α / β / A) * sh(
        τ * r(α * β / A / B)
    )
def f(Aα, Bβ, Cχ, τ):
    (A, α), (B, β), (C, χ), r = Aα, Bβ, Cχ, sqrt
    AB, C = f2((A + B, α + β), (C, χ), τ)
    return AB * A / (A + B), AB * B / (A + B), C


def g2(Aα, Bβ):
    (A, α), (B, β), r = Aα, Bβ, sqrt
    if A * α < B * β:
        return g2(Bβ, Aα)
    return r(A * B / α / β) * ln((r(A * α) + r(B * β)) / r(A * α - B * β))
def g(Aα, Bβ, Cχ):
    (A, α), (B, β), (C, χ), r = Aα, Bβ, Cχ, sqrt
    return g2((A + B, α + β), (C, χ))


def h2(Aα, Bβ):
    (A, α), (B, β), r = Aα, Bβ, sqrt
    if A * α < B * β:
        return h2(Bβ, Aα)
    return A * r(1 - B * β / A / α)

def h(Aα, Bβ, Cχ):
    (A, α), (B, β), (C, χ), r = Aα, Bβ, Cχ, sqrt
    return h2((A + B, α + β), (C, χ))


def test(A0, α, B0, β, C0, χ):
    A, B, C = float(A0), float(B0), float(C0)
    dt = 0.001
    current_t = 0
    # print(f"{A:.06} {B:.5} =?= {A:.5} {B:.5} :", 0)
    err_during_fight = 0
    for i in range(100000):
        if A < 0.1**6 or B < 0.1**6 or C < 0.1**6 or dt <= 0.1**12:
            break
        delta_A = -χ / C0 * C *   (A / (A + B))
        delta_B = -χ / C0 * C *   (B / (A + B))
        delta_C = -α / A0 * A  - β / B0 * B
        A_alt, B_alt, C_alt = f((A0, α), (B0, β), (C0, χ), current_t + dt)

        current_t += dt
        A += dt * delta_A
        B += dt * delta_B
        C += dt * delta_C
        dt = min(-A / delta_A, -B / delta_B, -C/delta_C) / 1000
        err_during_fight = max( err_during_fight, abs(A - A_alt) + abs(B - B_alt))
        # print(f"{A:10.06} {B:10.06} =?= {A_alt:10.06} {B_alt:10.06} :", abs(A - A_alt) + abs(B - B_alt))
    death_time_error = abs(current_t - g((A0, α), (B0, β), (C0, χ)))
    fight_result_error = abs(max(A + B, C) - h((A0, α), (B0, β), (C0, χ)))
    return err_during_fight, death_time_error, fight_result_error


for i in range(1, 11):
    A, B, C = (randint(1000, 10000) for _ in range(3))
    α, β, χ = (randint(1, 100) for _ in range(3))
    print(f"     t{i}")
    print(f"{A=}\t{α=}\n{B=}\t{β=}\n{C=}\t{χ=}")
    print("error:", *map(round, test(A, α, B, β, C, χ)))

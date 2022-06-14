# Guy #1:
#   attack: α
#   health: A
# Guy #2:
#   attack: α
#   health: A
#
# dA(τ)/dτ = -β * B(τ) / B
# dB(τ)/dτ = -α * A(τ) / A
#
# A(τ) = A * ch(τ * √(αβ/AB)) - B√(Aβ/αB) * sh(τ * √(αβ/AB))
# B(τ) = B * ch(τ * √(αβ/AB)) - A√(Bα/βA) * sh(τ * √(αβ/AB))
#
# If guy #1 is more powerful than the guy #2, i.e. Aα > Bβ
# t =  √(AB/αβ) * ln((√(Aα) + √(Bβ)) / √(Aα - Bβ)) -- time of death of guy #2
# A(t) = A * √(1 - Bβ/Aα) -- heath of guy #1 after fight
################################################################################

from math import inf, sqrt, log as ln, cosh as ch, sinh as sh
from random import randint


def f(Aα, Bβ, τ):
    (A, α), (B, β), r = Aα, Bβ, sqrt
    return A * ch(τ * r(α * β / A / B)) - B * r(A * β / α / B) * sh(
        τ * r(α * β / A / B)
    ), B * ch(τ * r(α * β / A / B)) - A * r(B * α / β / A) * sh(
        τ * r(α * β / A / B)
    )


def g(Aα, Bβ):
    (A, α), (B, β), r = Aα, Bβ, sqrt
    if A * α < B * β:
        return g(Bβ, Aα)
    return r(A * B / α / β) * ln((r(A * α) + r(B * β)) / r(A * α - B * β))


def h(Aα, Bβ):
    (A, α), (B, β), r = Aα, Bβ, sqrt
    if A * α < B * β:
        return h(Bβ, Aα)
    return A * r(1 - B * β / A / α)


def test(A0, α, B0, β):
    A, B = float(A0), float(B0)
    dt = 0.001
    current_t = 0
    # print(f"{A:.06} {B:.5} =?= {A:.5} {B:.5} :", 0)
    err_during_fight = 0
    for i in range(100000):
        if A < 0.00001 or B < 0.000001 or dt <= 0.00000001:
            break
        delta_A = -β / B0 * B
        delta_B = -α / A0 * A
        A_alt, B_alt = f((A0, α), (B0, β), current_t + dt)

        current_t += dt
        A += dt * delta_A
        B += dt * delta_B
        dt = min(-A / delta_A, -B / delta_B) / 1000
        err_during_fight = max(
            err_during_fight, abs(A - A_alt) + abs(B - B_alt)
        )
        # print(f"{A:10.06} {B:10.06} =?= {A_alt:10.06} {B_alt:10.06} :", abs(A - A_alt) + abs(B - B_alt))
    death_time_error = abs(current_t - g((A0, α), (B0, β)))
    fight_result_error = abs(max(A, B) - h((A0, α), (B0, β)))
    return err_during_fight, death_time_error, fight_result_error


for i in range(1, 11):
    A, B = (randint(1000, 10000) for _ in range(2))
    α, β = (randint(1, 100) for _ in range(2))
    print(f"     t{i}")
    print(f"A={A}\t{α=}\nB={B}\t{β=}")
    print("error:", *map(round, test(A, α, B, β)))

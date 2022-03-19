from fightcalculator import Squad
import matplotlib.pyplot as plt


def compute_result_of_a_fight1(A, α, B, β, C, γ):
    a, b, c = Squad(1, A, α), Squad(1, B, β), Squad(1, C, γ)
    a, b, c = Squad.fight3_to_death(a, b, c)
    return a.units, b.units, c.units


def compute_result_of_a_fight2(A, α, B, β, C, γ):
    a, b, c = Squad(1, A, α), Squad(1, B, β), Squad(1, C, γ)
    a, b, c = Squad.fight3_to_death(a, b, c, 10 ** (-3))
    return a.units, b.units, c.units


def dependence_on_attack_stats(A, α, B, β, C, γ, f):
    statistics = []
    for x in (1 + i / 16 for i in range(65)):
        a, b, c = f(A, α, B, β, C, γ * x)
        statistics.append((x, c))
    return statistics


def dependence_on_health_stats(A, α, B, β, C, γ, f):
    statistics = []
    for x in (1 + i / 16 for i in range(65)):
        a, b, c = f(A, α, B, β, C * x, γ)
        statistics.append((x, c))
    return statistics


def plot(statistics, color):
    plt.xlim([1, 5])
    plt.ylim([0, 1])
    plt.plot([x for x, y in statistics], [y for x, y in statistics], color)

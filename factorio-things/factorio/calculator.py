from fractions import Fraction as Rat
from .libs.dict_arithmetic import dict_max
from .recipes import MATERIALS, RECIPES


def dict_diff(dict1: dict, dict2: dict) -> dict:
    result = dict(dict1)
    for key in dict2:
        if key in dict1:
            del result[key]
    return result


def dict_and(dict1: dict, dict2: dict) -> dict:
    result = {}
    for key, value in dict1.items():
        if key in dict2:
            result[key] = value
    return result


def get_total_for_one_product_set(target_materials: dict[str, Rat]) -> dict[str, Rat]:
    total = dict(target_materials)
    for material in reversed(MATERIALS):
        if material not in total or material not in RECIPES:
            continue
        for ingridient, amount in RECIPES[material].ingredients.items():
            total[ingridient] = total.get(ingridient, Rat(0)) + amount * total[material]
    return total


def get_total(*alternative_product_sets: dict[str, Rat]) -> dict[str, Rat]:
    total = dict_max(*(get_total_for_one_product_set(prod) for prod in alternative_product_sets))
    return dict(sorted(total.items(), key=lambda p: (MATERIALS[p[0]], p[0])))


def rationalize_values(dct: dict) -> dict[str, Rat]:
    return dict((((k, Rat(v).limit_denominator(100)) for k, v in dct.items())))

import materials
from materials import Material
from fractions import Fraction as Rat


# TODO: use datastructures with this operation implemented
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


def get_total(target_materials: dict[Material, Rat]) -> dict[Material, Rat]:
    total = dict(target_materials)
    # TODO: use something like queue to optimize that
    for material in reversed(sorted(materials.MATERIALS)):
        if material not in total:
            continue
        for ingridient, amount in material.ingredients.items():
            total[ingridient] = total.get(ingridient, 0) + amount * total[material]
    return dict(total)


def rationalize_values(dct: dict) -> dict[Material, Rat]:
    return dict((((k, Rat(v).limit_denominator(100)) for k, v in dct.items())))


if __name__ == "__main__":
    target = {
        materials.INSERTER: 1,
    }
    total = get_total(rationalize_values(target))
    for material, amount in reversed(sorted(total.items())):
        print(material, ":", amount)

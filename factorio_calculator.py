import graphlib

sort_topologically = lambda g: graphlib.TopologicalSorter(g).static_order()
BELT_THROUGHPUT = 15
materials = {
    "transport belt",
    "copper cable",
    "iron plate",
    "underground belt",
    "splitter",
    "iron gear wheel",
    "copper plate",
    "electronic circuit",
}
recipes = {
    "iron gear wheel": {"iron plate": 2},
    "transport belt": {"iron gear wheel": 0.5, "iron plate": 0.5},
    "underground belt": {"iron plate": 5, "transport belt": 2.5},
    "copper cable": {"copper plate": 0.5},
    "electronic circuit": {"copper cable": 3, "iron plate": 1},
    "splitter": {"iron plate": 5, "transport belt": 4, "electronic circuit": 5},
}
crafting_times = {
    "iron gear wheel": 0.5,
    "transport belt": 0.25,
    "underground belt": 0.5,
    "copper cable": 0.25,
    "electronic circuit": 0.5,
    "splitter": 1,
}


def get_total_raw_materials(material, amount=1):
    if not (recipe := recipes.get(material, None)):
        return {material: amount}
    raw = {}
    for material, x in recipe.items():
        x *= amount
        for raw_material, y in get_total_raw_materials(material, x).items():
            raw[raw_material] = raw.get(raw_material, 0) + y
    return raw


def get_total_raw_time(material):
    return crafting_times.get(material, 0) + sum(
        get_total_raw_time(ingr) for ingr in recipes.get(material, set())
    )


def get_intermediate_materials(material, amount=1):
    if not (recipe := recipes.get(material, None)):
        return {}
    materials = {}
    for material, x in recipe.items():
        materials[material] = materials.get(material, 0) + x * amount
        for mat, x in get_intermediate_materials(material, x * amount).items():
            materials[mat] = materials.get(mat, 0) + x
    return materials


def get_assembly_plan(target, amount=1):
    raw_materials = get_total_raw_materials(target, amount)
    intermediates = get_intermediate_materials(target, amount)
    materials = raw_materials | intermediates | {target: amount}
    G = {ingr: recipes[ingr] for ingr in intermediates if ingr in recipes}
    assembly_order = list(sort_topologically(G)) + [target]
    return [(mat, materials[mat]) for mat in assembly_order]


target = input("target material: ")
if ":" in target:
    target, target_amount = target.split(":")
    target_amount = float(target_amount)
else:
    target_amount = 1.0
target = target.strip().lower()
if target not in materials:
    print(f"ERROR: what is {target}?")
    exit(1)
dt = get_total_raw_time(target)
raw = get_total_raw_materials(target, target_amount)
print(" -", target, ":", dt, " required materials:", raw)
for material, amount in get_assembly_plan(target, target_amount):
    if material in raw:
        print(f"run {amount} belts of {material}")
        continue
    ingredients = {m: x * amount for m, x in recipes[material].items()}
    asms = 2 * crafting_times[material] * amount * BELT_THROUGHPUT
    print(
        f"use {asms} assemblers to make {amount} belts of {material} "
        + f"out of {ingredients}"
    )

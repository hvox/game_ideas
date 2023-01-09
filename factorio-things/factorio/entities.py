ENTITY_ATTRIBUTES = dict[str, object]
ENTITY = tuple[str, ENTITY_ATTRIBUTES]
ENTITIES = dict[tuple[float, float], ENTITY]

BELTS = ["transport-belt", "fast-transport-belt", "express-transport-belt"]
UNDERGROUND_BELTS = ["underground-belt", "fast-underground-belt", "express-underground-belt"]
SPLITTERS = ["splitter", "fast-splitter", "express-splitter"]
ASSEMBLY_MACHINES = ["assembly-machine-1", "assembly-machine-2", "assembly-machine-3"]


def belt(lvl: int, direction: int) -> ENTITY:
    assert 1 <= lvl <= 3
    name = BELTS[lvl - 1]
    return (name, {"direction": direction % 8 // 2 * 2})


def underground(lvl: int, direction: int) -> tuple[ENTITY, ENTITY]:
    assert 1 <= lvl <= 3
    name = UNDERGROUND_BELTS[lvl - 1]
    inp = {"direction": direction % 8 // 2 * 2, "type": "input"}
    out = {"direction": direction % 8 // 2 * 2, "type": "output"}
    return ((name, inp), (name, out))


def splitter(
    lvl: int,
    direction: int,
    input_prioriy: int = 0,
    output_priority: int = 0,
    filter_material: str = "",
) -> ENTITY:
    assert 1 <= lvl <= 3
    name = SPLITTERS[lvl - 1]
    attributes: ENTITY_ATTRIBUTES = {"direction": direction % 8 // 2 * 2}
    if input_prioriy:
        attributes["input_prioriy"] = ["", "right", "left"][input_prioriy]
    if output_priority:
        attributes["output_priority"] = ["", "right", "left"][output_priority]
    if filter_material:
        attributes["filter"] = filter_material
    return (name, attributes)


def assembler(lvl: int, produced_material: str = "", direction: int = 0) -> ENTITY:
    assert 1 <= lvl <= 3
    name = ASSEMBLY_MACHINES[lvl - 1]
    attributes: ENTITY_ATTRIBUTES = {"direction": direction % 8 // 2 * 2}
    if produced_material:
        attributes["recipe"] = produced_material
    return (name, attributes)

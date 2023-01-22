EntityAttributes = dict[str, object]
Entity = tuple[str, EntityAttributes]
Entities = dict[tuple[float, float], Entity]

BELTS = ["transport-belt", "fast-transport-belt", "express-transport-belt"]
UNDERGROUND_BELTS = ["underground-belt", "fast-underground-belt", "express-underground-belt"]
SPLITTERS = ["splitter", "fast-splitter", "express-splitter"]
ASSEMBLY_MACHINES = ["assembly-machine-1", "assembly-machine-2", "assembly-machine-3"]


def belt(lvl: int, direction: int) -> Entity:
    assert 1 <= lvl <= 3
    name = BELTS[lvl - 1]
    return (name, {"direction": direction % 8 // 2 * 2})


def underground(lvl: int, direction: int) -> tuple[Entity, Entity]:
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
) -> Entity:
    assert 1 <= lvl <= 3
    name = SPLITTERS[lvl - 1]
    attributes: EntityAttributes = {"direction": direction % 8 // 2 * 2}
    if input_prioriy:
        attributes["input_prioriy"] = ["", "right", "left"][input_prioriy]
    if output_priority:
        attributes["output_priority"] = ["", "right", "left"][output_priority]
    if filter_material:
        attributes["filter"] = filter_material
    return (name, attributes)


def assembler(lvl: int, produced_material: str = "", direction: int = 0) -> Entity:
    assert 1 <= lvl <= 3
    name = ASSEMBLY_MACHINES[lvl - 1]
    attributes: EntityAttributes = {"direction": direction % 8 // 2 * 2}
    if produced_material:
        attributes["recipe"] = produced_material
    return (name, attributes)

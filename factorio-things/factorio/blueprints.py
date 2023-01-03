import zlib
import base64
import json


DIRECTED_STRUCTURES = {"transport-belt", "splitter", "express-loader", "underground-belt"}


def decode(encoded: str) -> dict[tuple[float, float], tuple[str, dict[str, str]]]:
    assert encoded[0] == "0"
    compressed = base64.b64decode(encoded[1:])
    decoded = json.loads(zlib.decompress(compressed).decode())
    entities = {}
    for entity in decoded["blueprint"]["entities"]:
        name = entity["name"]
        x = entity["position"]["x"]
        y = -entity["position"]["y"]
        attrs = {k: v for k, v in entity.items() if k not in ("name", "position", "entity_number")}
        if name in DIRECTED_STRUCTURES and "direction" not in attrs:
            attrs["direction"] = 0
        entities[x, y] = (name, attrs)
    return entities


def encode(entities: dict[tuple[float, float], tuple[str, dict[str, str]]]) -> str:
    entities_json = []
    for i, ((x, y), (name, attrs)) in enumerate(entities.items()):
        entity_json = dict(attrs)
        entity_json["entity_number"] = i + 1
        entity_json["position"] = {"x": x, "y": -y}
        entity_json["name"] = name
        entities_json.append(entity_json)
    json_obj = {"blueprint": {"entities": entities_json}}
    compressed = zlib.compress(json.dumps(json_obj).encode(), 9)
    return "0" + base64.b64encode(compressed).decode()


def rotated(
    origin_x: float, origin_y: float,
    entities: dict[tuple[float, float], tuple[str, dict[str, str]]],
) -> dict[tuple[float, float], tuple[str, dict[str, str]]]:
    rotated_entities = {}
    for (x, y), (name, entity) in entities.items():
        dx, dy = x - origin_x, y - origin_y
        rotated_entity = dict(entity)
        if "direction" in rotated_entity:
            rotated_entity["direction"] = (rotated_entity["direction"] - 2) % 8 or 8
        rotated_entities[origin_x - dy, origin_y + dx] = (name, rotated_entity)
    return rotated_entities


if __name__ == "__main__":
    import clipboard
    sample = "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"
    blueprint = decode(sample)
    print(blueprint)
    print({name for name, _ in blueprint.values()})
    rotated_blueprint = rotated(0, 0, blueprint)
    encoded = encode(rotated_blueprint)
    print(encoded)
    clipboard.copy(encoded)

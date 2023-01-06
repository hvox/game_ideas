from .libs.bitarray import BitArray


SUPPORTED_ENTITIES = ["transport-belt"]


def encode_entity(
    pos: tuple[float, float], name: str, attrs: dict[str, str | int]
) -> tuple[tuple[int, int], BitArray]:
    if name not in SUPPORTED_ENTITIES:
        raise ValueError(f"Unsupported entity: {name}")
    return encode_transport_belt(pos, attrs)


def decode_transport_belt(
    pos: tuple[int, int], code: BitArray, offset: int = 0
) -> tuple[tuple[float, float], dict[str, str | int], int]:
    pass



def encode_transport_belt(
    pos: tuple[float, float], attrs: dict[str, str | int]
) -> tuple[tuple[int, int], BitArray]:
    encoded_pos = tuple(as_int(x - 0.5) for x in pos)
    assert len(attrs) == 1
    direction = attrs["direction"] % 8 // 2
    return encoded_pos, BitArray.from_unsigned(direction, 2)


def decode_transport_belt(
    pos: tuple[int, int], code: BitArray, offset: int = 0
) -> tuple[tuple[float, float], dict[str, str | int], int]:
    decoded_pos = tuple(x + 0.5 for x in pos)
    direction = code[offset: offset + 2].to_unsigned() * 2
    return decoded_pos, {"direction": direction}, offset + 2


def as_int(x: float) -> int:
    if x.is_integer():
        return int(x)
    raise ValueError(f"{x} is not really an integer")

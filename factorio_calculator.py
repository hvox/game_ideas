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

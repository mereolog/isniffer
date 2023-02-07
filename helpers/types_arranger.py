def arrange_types_by_levels_of_subsumptions(type_subsumptions: dict) -> dict:
    levelled_types_at_levels = dict()
    level = 0
    while len(type_subsumptions) > 0:
        types_at_level = gather_types_at_level(type_subsumptions=type_subsumptions)
        levelled_types_at_levels[level] = types_at_level
        type_subsumptions = \
            remove_levelled_types(
                type_subsumptions=type_subsumptions,
                types_at_level=types_at_level)
        level += 1
    dict(sorted(levelled_types_at_levels.items()))
    return levelled_types_at_levels
    
    
def gather_types_at_level(type_subsumptions: dict) -> list:
    types_at_level = list()
    some_types_were_gathered = False
    minimal_length_of_subsuming_types = -1
    while (not some_types_were_gathered):
        minimal_length_of_subsuming_types += 1
        for type, subsumed_types in type_subsumptions.items():
            if len(subsumed_types) == minimal_length_of_subsuming_types:
                types_at_level.append(type)
                some_types_were_gathered = True
    return types_at_level


def remove_levelled_types(type_subsumptions: dict, types_at_level: list):
    type_subsumptions_copy = type_subsumptions.copy()
    for type, subsuming_types in type_subsumptions_copy.items():
        if len(subsuming_types) == 0:
            type_subsumptions.pop(type)
    type_subsumptions_copy = type_subsumptions.copy()
    for levelled_type in types_at_level:
        for subsuming_types in type_subsumptions_copy.values():
            if levelled_type in subsuming_types:
                subsuming_types.remove(levelled_type)
    return type_subsumptions
    
    
def __get_all_types(type_subsumptions: dict) -> set:
    all_types = set()
    for type, subsumed_types in type_subsumptions.items():
        all_types = all_types.union(set(subsumed_types))
        all_types.add(type)
    return all_types
    
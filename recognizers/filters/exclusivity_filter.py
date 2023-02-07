def filter_to_exclusive_cis(identity_criteria_for_types: dict) -> dict:
    filtered_identity_criteria_for_types = identity_criteria_for_types.copy()
    for type_1, identity_criteria_for_type_1 in identity_criteria_for_types.items():
        for type_2, identity_criteria_for_type_2 in identity_criteria_for_types.items():
            if not type_1 == type_2:
                common_criteria = set(identity_criteria_for_type_1).intersection(set(identity_criteria_for_type_2))
                for common_criterion in common_criteria:
                    filtered_identity_criteria_for_types[type_1].pop(common_criterion)
                    filtered_identity_criteria_for_types[type_2].pop(common_criterion)
    return filtered_identity_criteria_for_types
        
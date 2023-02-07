def filter_to_unique_cis(identity_criteria_for_types: dict) -> dict:
    filtered_identity_criteria_for_types = identity_criteria_for_types.copy()
    for type, identity_criteria_for_type in identity_criteria_for_types.items():
        if len(identity_criteria_for_type) > 1:
            filtered_identity_criteria_for_types.pop(type)
        
    return filtered_identity_criteria_for_types
        
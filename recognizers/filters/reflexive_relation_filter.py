# def filter_to_non_reflexive_cis(identity_criteria_for_types: dict, reflexive_relations: set) -> dict:
#     filtered_identity_criteria_for_types = identity_criteria_for_types.copy()
#     for type, identity_criteria_for_type in identity_criteria_for_types.items():
#         for identity_criterion_for_type in identity_criteria_for_type:
#             if identity_criterion_for_type in reflexive_relations:
#                 filtered_identity_criteria_for_types[type].pop(identity_criterion_for_type)
#
#     return filtered_identity_criteria_for_types

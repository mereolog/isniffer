import logging

from recognizers.subsumption_checkers import check_if_type_1_is_subsumed_to_type_2, \
    check_if_relation_1_is_subsumed_to_relation_2


def filter_i_identity_criterionby_type_subsumptions(identity_criteria_for_types: dict, theory: str, temp_file_path: str, keep_temp_files=True) -> dict:
    filtered_identity_criteria_for_types = identity_criteria_for_types.copy()
    for type_1, identity_criteria_for_type_1 in identity_criteria_for_types.items():
        for type_2, identity_criteria_for_type_2 in identity_criteria_for_types.items():
            type_1_is_subsumed_to_type_2 = check_if_type_1_is_subsumed_to_type_2(type_1=type_1, type_2=type_2,theory=theory,temp_file_path=temp_file_path,keep_temp_files=keep_temp_files)
            if type_1_is_subsumed_to_type_2:
                logging.info(msg='Dropping all identity criteria for ' + type_1 + ' because it is inherited from its supertype.')
                filtered_identity_criteria_for_types.pop(type_1)

    return filtered_identity_criteria_for_types


def filter_i_identity_criterion_by_relation_subsumptions(identity_criteria_for_types: dict, theory: str, temp_file_path: str, keep_temp_files=True) -> dict:
    filtered_identity_criteria_for_types = identity_criteria_for_types.copy()
    for type, identity_criteria_for_type in identity_criteria_for_types.items():
        identity_criteria_for_type_copy = identity_criteria_for_type.copy()
        for identity_criterion_for_type_1 in identity_criteria_for_type:
            relation_1 = identity_criterion_for_type_1.relation
            arity_1 = identity_criterion_for_type_1.arity
            for identity_criterion_for_type_2 in identity_criteria_for_type:
                relation_2 = identity_criterion_for_type_1.relation
                arity_2 = identity_criterion_for_type_2.arity
                if relation_1 == relation_2:
                    continue
                if arity_1 == arity_2:
                    continue
                arity = arity_1
                identity_criterion_1_is_subsumed_to_2 = \
                    check_if_relation_1_is_subsumed_to_relation_2(
                        relation_1=relation_1,
                        relation_2=relation_2,
                        theory=theory,
                        temp_file_path=temp_file_path,
                        keep_temp_files=keep_temp_files,
                        arity=arity)
                
                if identity_criterion_1_is_subsumed_to_2:
                    logging.info(msg='Dropping an identity criteria for ' + type + ' because it is inherited from its supertype.')
                    identity_criteria_for_type_copy.pop(relation_1)
        filtered_identity_criteria_for_types[type] = identity_criteria_for_type_copy
                
    return filtered_identity_criteria_for_types


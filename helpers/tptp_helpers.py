from common.constants import DUMMY_CONSTANT_1, DUMMY_CONSTANT_2, VARIABLE_PREFIX


def generate_i_identity_criterion_candidate_tptp_formula(
        relation: str,
        arity: int,
        i_identity_criterion_position=-1) -> str:
    i_identity_criterion_condition_1 = relation + '('
    i_identity_criterion_condition_2 = relation + '('
    variables = '['
    for sequence_position in range(1, arity + 1):
        if -1 < i_identity_criterion_position == sequence_position:
            i_identity_criterion_condition_1 = i_identity_criterion_condition_1 + DUMMY_CONSTANT_1 + ','
            i_identity_criterion_condition_2 = i_identity_criterion_condition_2 + DUMMY_CONSTANT_2 + ','
        else:
            variable = VARIABLE_PREFIX + str(sequence_position)
            i_identity_criterion_condition_1 = i_identity_criterion_condition_1 + variable + ','
            i_identity_criterion_condition_2 = i_identity_criterion_condition_2 + variable + ','
            variables = variables + variable + ','
    i_identity_criterion_condition_1 = i_identity_criterion_condition_1[:-1] + ')'
    i_identity_criterion_condition_2 = i_identity_criterion_condition_2[:-1] + ')'
    variables = variables[:-1] + ']'
    tptp_i_identity_criterion_candidate = '! ' + variables + ' : (' + i_identity_criterion_condition_1 + '<=>' + i_identity_criterion_condition_2 + ')'
    
    return tptp_i_identity_criterion_candidate


def adorn_tptp_formula(tptp_formula: str, identifier: int, formula_type='axiom') -> str:
    adorned_tptp_formula = 'fof(axiom' + str(identifier) + ',' + formula_type + ', ' + tptp_formula + ').'
    return adorned_tptp_formula
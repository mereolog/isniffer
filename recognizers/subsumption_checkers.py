import logging

from common.constants import *
from helpers.consistency_result import ProverResult
from helpers.tptp_helpers import generate_i_identity_criterion_candidate_tptp_formula, adorn_tptp_formula
from helpers.vampire_decider import decide_whether_theory_is_consistent


def check_if_relation_1_is_subsumed_to_relation_2(
        relation_1: str, 
        relation_2: str, 
        arity: int, 
        theory: str, 
        temp_file_path: str, 
        keep_temp_files=True) -> bool:
    if relation_1 == relation_2:
        return False

    for i_identity_criterion_position in range(1, arity + 1):
        bare_tptp_i_identity_criterion_candidate_1 = \
            generate_i_identity_criterion_candidate_tptp_formula(
                relation=relation_1,
                arity=arity,
                i_identity_criterion_position=i_identity_criterion_position)
        bare_tptp_i_identity_criterion_candidate_2 = \
            generate_i_identity_criterion_candidate_tptp_formula(
                relation=relation_2,
                arity=arity,
                i_identity_criterion_position=i_identity_criterion_position)
        bare_tptp_i_identity_criterion_candidate_1 = bare_tptp_i_identity_criterion_candidate_1.replace(DUMMY_CONSTANT_1, DUMMY_VARIABLE_1)
        bare_tptp_i_identity_criterion_candidate_1 = bare_tptp_i_identity_criterion_candidate_1.replace(DUMMY_CONSTANT_2, DUMMY_VARIABLE_2)
        bare_tptp_i_identity_criterion_candidate_2 = bare_tptp_i_identity_criterion_candidate_2.replace(DUMMY_CONSTANT_1, DUMMY_VARIABLE_1)
        bare_tptp_i_identity_criterion_candidate_2 = bare_tptp_i_identity_criterion_candidate_2.replace(DUMMY_CONSTANT_2, DUMMY_VARIABLE_2)
        
        implication_1_to_2 = \
            '!' + '[' + DUMMY_VARIABLE_1 + ',' + DUMMY_VARIABLE_2 + ']' + ' : ' + '(' + bare_tptp_i_identity_criterion_candidate_1 + ' => ' + bare_tptp_i_identity_criterion_candidate_2 + ')'
        
        tptp_implication_1_to_2 = adorn_tptp_formula(tptp_formula=implication_1_to_2, identifier=2,formula_type='conjecture')
        
        theory_with_i_identity_criterion_candidate_2_not_subsumes_1_test = theory + '\n' + tptp_implication_1_to_2
        theory_with_i_identity_criterion_candidate_2_not_subsumes_1_test_file_name = temp_file_path + 'i_identity_criterion_candidate_subsumption_' + relation_1 + '_subsumes_' + relation_2[0]
        theory_with_i_identity_criterion_candidate_2_not_subsumes_1_test_file = open(
            file=theory_with_i_identity_criterion_candidate_2_not_subsumes_1_test_file_name + '.in', mode='w')
        theory_with_i_identity_criterion_candidate_2_not_subsumes_1_test_file.write(theory_with_i_identity_criterion_candidate_2_not_subsumes_1_test)
        theory_with_i_identity_criterion_candidate_2_not_subsumes_1_test_file.close()
        
        theory_with_relation_2_not_subsuming_1_is_consistent = \
            decide_whether_theory_is_consistent(
                theory_file_name=theory_with_i_identity_criterion_candidate_2_not_subsumes_1_test_file_name,
                keep_temp_files=keep_temp_files)
        
        if theory_with_relation_2_not_subsuming_1_is_consistent == ProverResult.THEOREM:
            return True
        
        elif theory_with_relation_2_not_subsuming_1_is_consistent == ProverResult.UNDECIDED:
            logging.warning(
                'Vampire could not decide whether ci based on ' + str(relation_1) + ' subsumes ci based on ' + str(relation_2))
            return False


def check_if_type_1_is_subsumed_to_type_2(
        type_1: str, 
        type_2: str, 
        theory: str, 
        temp_file_path: str, 
        keep_temp_files=True) -> bool:
    if type_1 == type_2:
        return False
    tptp_class_axiom_1 = 'fof(axiom1' + ', axiom,' + type_1 + '(' + DUMMY_CONSTANT_1 + ')).'
    tptp_class_axiom_2 = 'fof(axiom2' + ', axiom, ~(' + type_2 + '(' + DUMMY_CONSTANT_1 + '))).'
    theory_with_type_2_not_subsumes_1_test = theory + '\n' + '\n'.join([tptp_class_axiom_1, tptp_class_axiom_2])
    theory_with_type_2_not_subsumes_1_test_file_name = temp_file_path + 'type_subsumption' + type_1 + '_and_not_' + type_2
    theory_with_type_2_not_subsumes_1_test_file = open(file=theory_with_type_2_not_subsumes_1_test_file_name + '.in', mode='w')
    theory_with_type_2_not_subsumes_1_test_file.write(theory_with_type_2_not_subsumes_1_test)
    theory_with_type_2_not_subsumes_1_test_file.close()
    
    theory_with_type_2_not_subsuming_1_is_consistent = \
        decide_whether_theory_is_consistent(
            theory_file_name=theory_with_type_2_not_subsumes_1_test_file_name,
            keep_temp_files=keep_temp_files)
    
    if theory_with_type_2_not_subsuming_1_is_consistent == ProverResult.INCONSISTENT:
        return True
    
    elif theory_with_type_2_not_subsuming_1_is_consistent == ProverResult.UNDECIDED:
        logging.warning('Vampire could not decide whether ' + type_2 + ' subsumes ' + type_1)
        return False
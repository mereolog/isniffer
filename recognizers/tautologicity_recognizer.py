import logging

import tqdm as tqdm

from common.constants import DUMMY_CONSTANT_TEMPLATE
from common.patterns import sentence_with_non_monadic_predicates_pattern
from helpers.consistency_result import ProverResult
from helpers.tptp_helpers import generate_i_identity_criterion_candidate_tptp_formula, adorn_tptp_formula
from helpers.vampire_decider import decide_whether_theory_is_consistent
from objects.identity_criterion_candidate import IdentityCriterionCandidate


def find_tautological_i_identity_criteria_candidates_in_theory(
        theory_file_name: str,
        temp_file_path: str,
        theory_id: str,
        logging_file_name=str(),
        keep_temp_files=False) -> list:
    if len(logging_file_name) > 0:
        logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', level=logging.INFO,datefmt='%m/%d/%Y %I:%M:%S %p', filename=logging_file_name)
    else:
        logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', level=logging.WARN,datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('Finding tautological relations in theory ' + theory_id)
    
    theory_file = open(theory_file_name)
    theory = theory_file.read()
    theory_file.close()
    sentences_with_non_monadic_predicates = set(sentence_with_non_monadic_predicates_pattern.findall(string=theory))
    
    relations_with_arities = list()
    for sentence_with_non_monadic_predicate in sentences_with_non_monadic_predicates:
        non_monadic_predicate_with_arity = tuple([sentence_with_non_monadic_predicate[0], str(sentence_with_non_monadic_predicate[1]).count(',') + 1])
        if non_monadic_predicate_with_arity not in relations_with_arities:
            relations_with_arities.append(non_monadic_predicate_with_arity)
    
    tautological_i_identity_criterion_candidates = list()
    for relation_with_arity in tqdm.tqdm(relations_with_arities, desc='checked relations', position=0):
        relation = relation_with_arity[0]
        arity = relation_with_arity[1]
        
        for index in range(1, arity + 1):
            tptp_i_identity_criteria_axiom = \
                generate_i_identity_criterion_candidate_tptp_formula(
                    relation=relation,arity=arity,
                    i_identity_criterion_position=index)

            tptp_non_tautological_i_identity_criteria_axiom = '~' + tptp_i_identity_criteria_axiom
            
            adorned_tptp_non_tautological_i_identity_criteria_axiom = \
                adorn_tptp_formula(
                    tptp_formula=tptp_non_tautological_i_identity_criteria_axiom,
                    identifier=1)
            
            theory_with_tautological_i_identity_criterion_candidates_test = theory + '\n' + adorned_tptp_non_tautological_i_identity_criteria_axiom
            theory_with_tautological_i_identity_criterion_candidates_test_file_name = temp_file_path + 'ici_tautology_test_for_' + relation + '_at_' + str(index)
            theory_with_tautological_i_identity_criterion_candidates_test_file = open(file=theory_with_tautological_i_identity_criterion_candidates_test_file_name + '.in', mode='w')
            theory_with_tautological_i_identity_criterion_candidates_test_file.write(theory_with_tautological_i_identity_criterion_candidates_test)
            theory_with_tautological_i_identity_criterion_candidates_test_file.close()
    
            theory_with_tautological_i_identity_criterion_candidates_is_consistent = \
                decide_whether_theory_is_consistent(
                    theory_file_name=theory_with_tautological_i_identity_criterion_candidates_test_file_name,
                    keep_temp_files=keep_temp_files)
    
            if theory_with_tautological_i_identity_criterion_candidates_is_consistent == ProverResult.INCONSISTENT:
                tautological_i_identity_criterion_candidates.append(
                    IdentityCriterionCandidate(
                        relation=relation,
                        arity=arity,
                        identity_position=index))
    
            elif theory_with_tautological_i_identity_criterion_candidates_is_consistent == ProverResult.UNDECIDED:
                logging.warning('Vampire could not decide whether identity criterion based on ' + str(relation) + ' is tautological')

    logging.info(
        'All tautological relations in theory ' + theory_id + ' are found. Found ' + str(len(tautological_i_identity_criterion_candidates)) + ' relations.')
    
    return tautological_i_identity_criterion_candidates

import logging

import tqdm as tqdm

from common.constants import DUMMY_CONSTANT_1, DUMMY_CONSTANT_2, DUMMY_VARIABLE_1, DUMMY_VARIABLE_2
from common.patterns import sentence_with_monadic_predicates_pattern, sentence_with_non_monadic_predicates_pattern
from helpers.consistency_result import ProverResult
from helpers.tptp_helpers import generate_i_identity_criterion_candidate_tptp_formula, adorn_tptp_formula
from helpers.vampire_decider import decide_whether_theory_is_consistent


def find_type_subsumptions_in_theory(
        theory_file_name: str,
        temp_file_path: str,
        theory_id: str,
        logging_file_name=str(),
        keep_temp_files=False) -> dict:
    if len(logging_file_name) > 0:
        logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p', filename=logging_file_name)
    else:
        logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', level=logging.WARN,datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('Finding type subsumptions in theory ' + theory_id)

    theory_file = open(theory_file_name)
    theory = theory_file.read()
    theory_file.close()
    sentences_with_monadic_predicates = set(sentence_with_monadic_predicates_pattern.findall(string=theory))
    
    monadic_predicates = set()
    for sentence_with_monadic_predicate in sentences_with_monadic_predicates:
        monadic_predicates.add(sentence_with_monadic_predicate[0])
       
    type_subsumptions = dict()
    for type_1 in tqdm.tqdm(monadic_predicates, desc='checked subtype candidates', position=0):
        for type_2 in tqdm.tqdm(monadic_predicates, desc='checked supertype candidates for type : ' + type_1, position=1):
            if type_1 == type_2:
                continue
            if type_1 in type_subsumptions:
                types_type_1_is_subsumed_to = type_subsumptions[type_1]
                if type_2 in types_type_1_is_subsumed_to:
                    continue
            
            tptp_class_axiom_1 = 'fof(axiom1' + ', axiom,' + type_1 + '(' + DUMMY_CONSTANT_1 + ')).'
            tptp_class_axiom_2 = 'fof(axiom2' + ', axiom, ~(' + type_2 + '(' + DUMMY_CONSTANT_1 + '))).'
            theory_with_type_2_not_subsumes_1_test = theory + '\n' + '\n'.join([tptp_class_axiom_1, tptp_class_axiom_2])
            theory_with_type_2_not_subsumes_1_test_file_name = temp_file_path + 'type_' + type_1 + '_subsumed_to_' + type_2
            theory_with_type_2_not_subsumes_1_test_file = open(file=theory_with_type_2_not_subsumes_1_test_file_name + '.in', mode='w')
            theory_with_type_2_not_subsumes_1_test_file.write(theory_with_type_2_not_subsumes_1_test)
            theory_with_type_2_not_subsumes_1_test_file.close()

            theory_with_type_2_not_subsuming_1_is_consistent = \
                decide_whether_theory_is_consistent(
                    theory_file_name=theory_with_type_2_not_subsumes_1_test_file_name,
                    keep_temp_files=keep_temp_files)
            
            if theory_with_type_2_not_subsuming_1_is_consistent == ProverResult.INCONSISTENT:
                if type_1 in type_subsumptions:
                    types_type_1_is_subsumed_to = type_subsumptions[type_1]
                else:
                    types_type_1_is_subsumed_to = list()
                    type_subsumptions[type_1] = types_type_1_is_subsumed_to
                if type_2 not in types_type_1_is_subsumed_to:
                    types_type_1_is_subsumed_to.append(type_2)

                __transitievly_close_subsumptions(subsumptions=type_subsumptions)
                
            elif theory_with_type_2_not_subsuming_1_is_consistent == ProverResult.UNDECIDED:
                logging.warning('Vampire could not decide whether ' + type_2 + ' subsumes ' + type_1)
        
        if type_1 not in type_subsumptions:
            type_subsumptions[type_1] = list()
        
    for type, subsuming_types in type_subsumptions.items():
        for subsuming_type in subsuming_types:
            if subsuming_type in type_subsumptions:
                if type in type_subsumptions[subsuming_type]:
                    logging.warning(msg='Type ' + type + ' is equivalent to ' + subsuming_type)

    logging.info('All subsumptions in theory ' + theory_id + ' are found.')

    return type_subsumptions


def find_i_identity_criterion_candidate_subsumptions_in_theory(
        theory_file_name: str,
        temp_file_path: str,
        theory_id: str,
        logging_file_name=str(),
        keep_temp_files=False) -> dict:
    if len(logging_file_name) > 0:
        logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', level=logging.WARN, datefmt='%m/%d/%Y %I:%M:%S %p', filename=logging_file_name)
    else:
        logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', level=logging.WARN,datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('Finding relation subsumptions in theory ' + theory_id)
    
    theory_file = open(theory_file_name)
    theory = theory_file.read()
    theory_file.close()
    sentences_with_non_monadic_predicates = set(sentence_with_non_monadic_predicates_pattern.findall(string=theory))
    
    relations_with_arities = list()
    for sentence_with_non_monadic_predicate in sentences_with_non_monadic_predicates:
        non_monadic_predicate_with_arity = tuple([sentence_with_non_monadic_predicate[0], str(sentence_with_non_monadic_predicate[1]).count(',') + 1])
        if non_monadic_predicate_with_arity not in relations_with_arities:
            relations_with_arities.append(non_monadic_predicate_with_arity)
    
    i_identity_criterion_candidate_subsumptions = dict()
    for relation_with_arity_1 in tqdm.tqdm(relations_with_arities, desc='checked supertype candidates', position=0):
        relation_1 = relation_with_arity_1[0]
        relation_1_arity = relation_with_arity_1[1]
        for relation_with_arity_2 in tqdm.tqdm(relations_with_arities, desc='checked subtype candidates for type: ' + relation_1,position=1):
            relation_2 = relation_with_arity_2[0]
            relation_2_arity = relation_with_arity_2[1]
            if relation_1 == relation_2:
                continue
            if not relation_1_arity == relation_2_arity:
                continue
            arity = relation_1_arity
            if relation_2 in i_identity_criterion_candidate_subsumptions:
                relations_subsumed_by_relation_2 = i_identity_criterion_candidate_subsumptions[relation_2]
                relations_subsumed_by_relation_2_copy = relations_subsumed_by_relation_2.copy()
                for relation_subsumed_by_relation_2 in relations_subsumed_by_relation_2_copy:
                    if relation_subsumed_by_relation_2 in i_identity_criterion_candidate_subsumptions:
                        if relation_with_arity_1 in i_identity_criterion_candidate_subsumptions[relation_subsumed_by_relation_2]:
                            relations_subsumed_by_relation_2.append(relation_1)
                            continue

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

                tptp_implication_1_to_2 = adorn_tptp_formula(tptp_formula=implication_1_to_2, identifier=2, formula_type='conjecture')
                
                theory_with_i_identity_criterion_candidate_2_not_subsumes_1_test = theory + '\n' + tptp_implication_1_to_2
                theory_with_i_identity_criterion_candidate_2_not_subsumes_1_test_file_name = temp_file_path + 'i_identity_criterion_candidate_subsumption_' + relation_with_arity_1[0] + '_and_not_' + relation_with_arity_2[0]
                theory_with_i_identity_criterion_candidate_2_not_subsumes_1_test_file = open(file=theory_with_i_identity_criterion_candidate_2_not_subsumes_1_test_file_name + '.in', mode='w')
                theory_with_i_identity_criterion_candidate_2_not_subsumes_1_test_file.write(theory_with_i_identity_criterion_candidate_2_not_subsumes_1_test)
                theory_with_i_identity_criterion_candidate_2_not_subsumes_1_test_file.close()
                
                theory_with_relation_2_not_subsuming_1_is_consistent = \
                    decide_whether_theory_is_consistent(
                        theory_file_name=theory_with_i_identity_criterion_candidate_2_not_subsumes_1_test_file_name,
                        keep_temp_files=keep_temp_files)
                
                if theory_with_relation_2_not_subsuming_1_is_consistent == ProverResult.THEOREM:
                    if relation_2 in i_identity_criterion_candidate_subsumptions:
                        relations_subsumed_by_relation_2 = i_identity_criterion_candidate_subsumptions[relation_2]
                    else:
                        relations_subsumed_by_relation_2 = list()
                        i_identity_criterion_candidate_subsumptions[relation_2] = relations_subsumed_by_relation_2
                    if relation_1 not in relations_subsumed_by_relation_2:
                        relations_subsumed_by_relation_2.append(relation_1)

                    __transitievly_close_subsumptions(subsumptions=i_identity_criterion_candidate_subsumptions)
                
                elif theory_with_relation_2_not_subsuming_1_is_consistent == ProverResult.UNDECIDED:
                    logging.warning(
                        'Vampire could not decide whether ci based on ' + str(relation_1) + ' subsumes ci based on ' + str(relation_2))
    
    return i_identity_criterion_candidate_subsumptions


def __transitievly_close_subsumptions(subsumptions: dict):
    for predicate in subsumptions.keys():
        predicates_predicate_is_subsumed_to = subsumptions[predicate]
        predicates_predicate_is_subsumed_to_copy = predicates_predicate_is_subsumed_to.copy()
        for predicate_predicate_is_subsumed_to in predicates_predicate_is_subsumed_to_copy:
            if predicate_predicate_is_subsumed_to in subsumptions:
                predicates_predicate_is_subsumed_to = list(set(predicates_predicate_is_subsumed_to + subsumptions[predicate_predicate_is_subsumed_to]))
                
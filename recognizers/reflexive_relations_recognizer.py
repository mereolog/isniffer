import itertools
import logging
import os

import tqdm as tqdm

from common.constants import DUMMY_CONSTANT_1, DUMMY_CONSTANT_2, VARIABLE_PREFIX, DUMMY_CONSTANT_TEMPLATE
from common.patterns import sentence_with_non_monadic_predicates_pattern
from helpers.consistency_result import ProverResult
from helpers.predicate_helpers import find_constant_indices_in_argument_sequence
from helpers.vampire_decider import decide_whether_theory_is_consistent


def __get_domain_disjunction(predicate: str, focus_argument: str, arity: int) -> str:
    domain_disjunction = str()
    arguments = [focus_argument]
    for index in range(1, arity):
        arguments.append(DUMMY_CONSTANT_TEMPLATE+str(index))
    
    arguments_permutations = list(itertools.permutations(arguments))

    for arguments_permutation in arguments_permutations:
        domain_disjunction += '|' + predicate + '(' + ','.join(arguments_permutation) + ')'
        
    domain_disjunction = '(' + domain_disjunction[1:] + ')'

    return domain_disjunction


def find_reflexive_relations_in_theory(
        theory_file_name: str,
        temp_file_path: str,
        theory_id: str,
        logging_file_name=str(),
        keep_temp_files=False) -> list:
    logging.info('Finding reflexive relations')
    if len(logging_file_name) > 0:
        logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', level=logging.WARN, datefmt='%m/%d/%Y %I:%M:%S %p', filename=logging_file_name)
    else:
        logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', level=logging.WARN,datefmt='%m/%d/%Y %I:%M:%S %p')
    
    reflexive_relations = set()
    
    theory_file = open(theory_file_name)
    theory = theory_file.read()
    theory_file.close()
    sentences_with_non_monadic_predicates = set(sentence_with_non_monadic_predicates_pattern.findall(string=theory))

    non_monadic_predicates_with_arities = list()
    for sentence_with_non_monadic_predicate in sentences_with_non_monadic_predicates:
        non_monadic_predicate_with_arity = [sentence_with_non_monadic_predicate[0],str(sentence_with_non_monadic_predicate[1]).count(',') + 1]
        if non_monadic_predicate_with_arity not in non_monadic_predicates_with_arities:
            non_monadic_predicates_with_arities.append(non_monadic_predicate_with_arity)
    
    for non_monadic_predicate_with_arity in tqdm.tqdm(non_monadic_predicates_with_arities, desc='checked relations', position=0):
        non_monadic_predicate = non_monadic_predicate_with_arity[0]
        non_monadic_predicate_arity = non_monadic_predicate_with_arity[1]

        arguments = [DUMMY_CONSTANT_1, DUMMY_CONSTANT_2]
        for predicate_argument_position in range(1, non_monadic_predicate_arity - 1):
            arguments.append(VARIABLE_PREFIX + str(predicate_argument_position))
        
        arguments_permutations = list(itertools.permutations(arguments))
        
        for arguments_permutation in arguments_permutations:
            variables_in_arguments_premutation = list()
            for argument in arguments_permutation:
                if argument == DUMMY_CONSTANT_1 or argument == DUMMY_CONSTANT_2:
                    continue
                else:
                    variables_in_arguments_premutation.append(argument)
            identity_axiom = DUMMY_CONSTANT_1 + ' = ' + DUMMY_CONSTANT_2
            object_is_in_domains_axiom = __get_domain_disjunction(predicate=non_monadic_predicate, focus_argument=DUMMY_CONSTANT_1, arity=non_monadic_predicate_arity)
            relation_axiom = non_monadic_predicate + '(' + ','.join(arguments_permutation) + ')'
            if len(variables_in_arguments_premutation) > 0:
                relation_axiom = '? ' + '[' + ','.join(variables_in_arguments_premutation) + ']' + ' : ~(' + relation_axiom + ')'
            else:
                relation_axiom = '~(' + relation_axiom + ')'
            tptp_identity_axiom = 'fof(axiom_1, axiom,' + identity_axiom + ').'
            tptp_object_is_in_domains_axiom = 'fof(axiom_2, axiom,' + object_is_in_domains_axiom + ').'
            tptp_relation_axiom = 'fof(axiom_3, axiom,' + relation_axiom + ').'

            reflexive_range = find_constant_indices_in_argument_sequence(argument_sequence=arguments_permutation)
            
            theory_with_not_reflexive_relation_test = theory + '\n' + '\n'.join([tptp_identity_axiom, tptp_object_is_in_domains_axiom, tptp_relation_axiom])
            theory_with_not_reflexive_relation_test_local_file_name = theory_id + '_reflexive_test_' + non_monadic_predicate + '_' + '-'.join(reflexive_range)
            theory_with_not_reflexive_relation_test_file_name = os.path.join(temp_file_path, theory_with_not_reflexive_relation_test_local_file_name)
            theory_with_not_reflexive_relation_test_file = open(file=theory_with_not_reflexive_relation_test_file_name + '.in', mode='w')
            theory_with_not_reflexive_relation_test_file.write(theory_with_not_reflexive_relation_test)
            theory_with_not_reflexive_relation_test_file.close()
    
            theory_with_not_reflexive_relation_is_consistent = \
                decide_whether_theory_is_consistent(
                    theory_file_name=theory_with_not_reflexive_relation_test_file_name,
                    keep_temp_files=keep_temp_files)
            
            if theory_with_not_reflexive_relation_is_consistent == ProverResult.INCONSISTENT:
                reflexive_relations.add(tuple([non_monadic_predicate, tuple(reflexive_range)]))
                
            elif theory_with_not_reflexive_relation_is_consistent == ProverResult.UNDECIDED:
                logging.warning('Vampire could not decide whether ' + non_monadic_predicate + ' is reflexive.')
            
    return list(reflexive_relations)

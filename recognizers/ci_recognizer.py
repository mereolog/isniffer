import logging
import os.path

import tqdm as tqdm

from common.constants import DUMMY_CONSTANT_1, DUMMY_CONSTANT_2
from common.patterns import sentence_with_monadic_predicates_pattern, sentence_with_non_monadic_predicates_pattern
from helpers.consistency_result import ProverResult
from helpers.tptp_helpers import generate_i_identity_criterion_candidate_tptp_formula, adorn_tptp_formula
from helpers.types_arranger import arrange_types_by_levels_of_subsumptions
from helpers.vampire_decider import decide_whether_theory_is_consistent
from objects.identity_criterion_recognition_config import IdentityCriterionRecognitionConfig
from objects.identity_criterion_candidate import IdentityCriterionCandidate
from recognizers.ci_recognizer_helper import get_support_data_if_required
from recognizers.filters.filter_aggregator import filter_identity_criteria


def recognize_criteria_of_identity_in_theory(
        theory_file_name: str,
        theory_id: str,
        temp_file_path: str,
        recognition_config: IdentityCriterionRecognitionConfig,
        type_subsumptions_in_theory_file_name=str(),
        tautological_ici_candidates_file_name=str(),
        logging_file_name=str(),
        keep_temp_files=False):
    if len(logging_file_name) > 0:
        logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', level=logging.INFO,datefmt='%m/%d/%Y %I:%M:%S %p', filename=logging_file_name)
    else:
        logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s', level=logging.WARN,datefmt='%m/%d/%Y %I:%M:%S %p')

    logging.info('Finding identity criteria in theory ' + theory_id)

    logging.info('Loading input data')
    theory_file = open(theory_file_name)
    theory = theory_file.read()
    theory_file.close()

    type_subsumptions, tautological_i_identity_criterion_candidates = \
        get_support_data_if_required(
            theory=theory,
            theory_id=theory_id,
            temp_file_path=temp_file_path,
            keep_temp_files=keep_temp_files,
            recognition_config=recognition_config,
            type_subsumptions_in_theory_file_name=type_subsumptions_in_theory_file_name,
            tautological_relations_file_name=tautological_ici_candidates_file_name)
    
    sentences_with_non_monadic_predicates = set(sentence_with_non_monadic_predicates_pattern.findall(string=theory))
    sentences_with_monadic_predicates = set(sentence_with_monadic_predicates_pattern.findall(string=theory))
    types = set()
    for sentence_with_monadic_predicate in sentences_with_monadic_predicates:
        types.add(sentence_with_monadic_predicate[0])
    relations_with_arities = list()
    for sentence_with_non_monadic_predicate in sentences_with_non_monadic_predicates:
        relation_with_arity = [sentence_with_non_monadic_predicate[0], str(sentence_with_non_monadic_predicate[1]).count(',') + 1]
        if relation_with_arity not in relations_with_arities:
            relations_with_arities.append(relation_with_arity)
    
    type_subsumptions_copy = dict()
    for type, type_subsumption in type_subsumptions.items():
        type_subsumptions_copy[type] = list(type_subsumption)
    types_arranged_by_subsumption_levels = arrange_types_by_levels_of_subsumptions(type_subsumptions=type_subsumptions_copy)
    ordered_types = list()
    for ordered_types_at_level in types_arranged_by_subsumption_levels.values():
        ordered_types += ordered_types_at_level
        
    tested_relations_with_i_identity_criterion_position_identifiers = list()
    logging.info('Finding criteria of identity')
    identity_criteria_for_types = dict()
    count = 0
    for type in tqdm.tqdm(ordered_types, desc='checked types', position=0):
        tested_relations_with_i_identity_criterion_position_identifiers.clear()
        tptp_class_axiom_1 = 'fof(axiom' + str(count) +', axiom,' + type + '(' + DUMMY_CONSTANT_1 + ')).'
        count = count + 1
        tptp_class_axiom_2 = 'fof(axiom' + str(count) +', axiom,' + type + '(' + DUMMY_CONSTANT_2 + ')).'
        tptp_difference = 'fof(diff' + str(count) + ', axiom, ' + DUMMY_CONSTANT_1 + '!=' + DUMMY_CONSTANT_2 + ').'
        for relation_with_arity in tqdm.tqdm(relations_with_arities, desc='checked ci candidates for type '+type, position=1, leave=False):
            relation = relation_with_arity[0]
            arity = relation_with_arity[1]
                
            for i_identity_criterion_position in range(1, arity + 1):
                if recognition_config.non_tautologicity:
                    for tautological_i_identity_criterion_candidate in tautological_i_identity_criterion_candidates:
                        if tautological_i_identity_criterion_candidate['relation'] == relation and tautological_i_identity_criterion_candidate['identity_position'] == i_identity_criterion_position :
                            continue
                
                i_identity_criterion_candidate_is_carried_from_supertype = \
                    __check_if_i_identity_criterion_candidate_is_carried_from_supertype(
                        i_identity_criterion_candidate=relation,
                        i_identity_criterion_candidate_position=i_identity_criterion_position,
                        type=type,
                        identity_criteria_for_types=identity_criteria_for_types,
                        type_subsumptions=type_subsumptions)
                
                if i_identity_criterion_candidate_is_carried_from_supertype:
                    logging.info(
                        msg='Identity criterion ' + relation + ' (at place ' + str(i_identity_criterion_position) + ') for type ' + type + ' is inherited from its supertype.')
                    continue
                
                bare_tptp_i_identity_criterion_candidate = \
                    generate_i_identity_criterion_candidate_tptp_formula(
                        relation=relation,
                        arity=arity,
                        i_identity_criterion_position=i_identity_criterion_position)
                tptp_i_identity_criterion_candidate = adorn_tptp_formula(tptp_formula=bare_tptp_i_identity_criterion_candidate,identifier=count)
                count = count + 1
                theory_with_i_identity_criterion_candidate = theory + '\n' + '\n'.join([tptp_class_axiom_1, tptp_class_axiom_2, tptp_i_identity_criterion_candidate, tptp_difference])
                theory_with_i_identity_criterion_candidate_local_file_name = 'ci_' + '_'.join([theory_id,type, relation, '@', '-'.join(str(i_identity_criterion_position))])
                theory_with_i_identity_criterion_candidate_file_name = os.path.join(temp_file_path,theory_with_i_identity_criterion_candidate_local_file_name)
                theory_file_i_identity_criterion_candidate = open(file=theory_with_i_identity_criterion_candidate_file_name + '.in', mode='w')
                theory_file_i_identity_criterion_candidate.write(theory_with_i_identity_criterion_candidate)
                theory_file_i_identity_criterion_candidate.close()

                if [relation, i_identity_criterion_position] in tested_relations_with_i_identity_criterion_position_identifiers:
                    continue
            
                theory_with_i_identity_criterion_candidate_is_consistent = \
                    decide_whether_theory_is_consistent(
                        theory_file_name=theory_with_i_identity_criterion_candidate_file_name)

                tested_relations_with_i_identity_criterion_position_identifiers.append([relation, i_identity_criterion_position])

                if theory_with_i_identity_criterion_candidate_is_consistent == ProverResult.INCONSISTENT:
                    if type in identity_criteria_for_types:
                        identity_criteria_for_type = identity_criteria_for_types[type]
                    else:
                        identity_criteria_for_type = list()
                        identity_criteria_for_types[type] = identity_criteria_for_type
                    identity_criteria_for_type.append(IdentityCriterionCandidate(relation=relation, identity_position=i_identity_criterion_position, arity=arity))
                elif theory_with_i_identity_criterion_candidate_is_consistent == ProverResult.UNDECIDED:
                    logging.warning(
                        msg='Vampire could not decide whether '+relation+' at argument place '+'-'.join(str(i_identity_criterion_position))+' is a identity criterion for '+type)
    
    filtered_identity_criteria_for_types = \
        filter_identity_criteria(
            identity_criteria_for_types=identity_criteria_for_types,
            recognition_config=recognition_config,
            temp_file_path=temp_file_path,
            keep_temp_files=keep_temp_files,
            theory=theory)

    logging.info(
        'All identity criteria in theory ' + theory_id + ' are found.' + 'Found ' + str(len(filtered_identity_criteria_for_types)) + 'criteria.')
    
    return filtered_identity_criteria_for_types


def __check_if_i_identity_criterion_candidate_is_carried_from_supertype(
        i_identity_criterion_candidate: str,
        i_identity_criterion_candidate_position: int,
        type: str,
        identity_criteria_for_types: dict,
        type_subsumptions: dict) -> bool:
    if type not in type_subsumptions:
        return False
    for type_with_ci, identity_criteria in identity_criteria_for_types.items():
        for identity_criterion in identity_criteria:
            identity_criterion_relation = identity_criterion.relation
            identity_criterion_position = identity_criterion.identity_position
            if not i_identity_criterion_candidate == identity_criterion_relation or not i_identity_criterion_candidate_position == identity_criterion_position:
                continue
            if type_with_ci in type_subsumptions[type]:
                return True
    return False
    
    
    

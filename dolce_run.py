import os
import os
import time

from common.metadata_adorner import adorn_results_dict_with_metadata
from helpers.json_helpers import write_python_object_to_json_file
from objects.identity_criterion_candidate import IdentityCriterionCandidate
from objects.identity_criterion_recognition_config import IdentityCriterionRecognitionConfig
from recognizers.ci_recognizer import recognize_criteria_of_identity_in_theory
from recognizers.subsumptions_recognizer import find_type_subsumptions_in_theory
from recognizers.tautologicity_recognizer import find_tautological_i_identity_criteria_candidates_in_theory
from tablifier import tablify_identity_criteria

timestr = time.strftime("%Y%m%d-%H%M%S")
logging_file_name = os.path.join('outputs/dolce/', 'logging' + timestr + '.log')

# dolce_type_subsumptions = \
#     find_type_subsumptions_in_theory(
#         theory_file_name='inputs/dolce.tptp',
#         temp_file_path='outputs/dolce/subsumptions/',
#         theory_id='dolce',
#         keep_temp_files=True,
#         logging_file_name=logging_file_name)
#
# write_python_object_to_json_file(
#     python_object=dolce_type_subsumptions,
#     json_file_path='outputs/dolce/',
#     json_generic_file_name='dolce_type_subsumptions',
#     timestr=timestr)



# dolce_tautological_i_identity_criteria_candidates = \
#     find_tautological_i_identity_criteria_candidates_in_theory(
#         theory_file_name='inputs/dolce.tptp',
#         temp_file_path='outputs/dolce/tautological_relations/',
#         theory_id='dolce',
#         keep_temp_files=True)
#
# write_python_object_to_json_file(
#     python_object=dolce_tautological_i_identity_criteria_candidates,
#     json_file_path='outputs/dolce/',
#     json_generic_file_name='dolce_tautological_i_identity_criteria_candidates',
#     timestr=timestr)


# dolce_recognition_config_1 = \
#     IdentityCriterionRecognitionConfig(
#         non_tautologicity=False,
#         type_maximality=False,
#         uniqueness=False,
#         partial_exclusivity=False)
#
# dolce_criteria_of_identity = \
#     recognize_criteria_of_identity_in_theory(
#         theory_file_name='inputs/dolce.tptp',
#         temp_file_path='outputs/dolce/cis/',
#         theory_id='dolce',
#         keep_temp_files=True,
#         type_subsumptions_in_theory_file_name='outputs/dolce/dolce_type_subsumptions_20230131-172945.json',
#         tautological_ici_candidates_file_name='outputs/dolce/dolce_tautological_i_identity_criteria_candidates_20230201-083045.json',
#         recognition_config=dolce_recognition_config_1,
#         logging_file_name=logging_file_name)
#
# adorned_dolce_criteria_of_identity = \
#     adorn_results_dict_with_metadata(
#         results_dict=dolce_criteria_of_identity,
#         recognition_config=dolce_recognition_config_1)
#
# write_python_object_to_json_file(
#     python_object=adorned_dolce_criteria_of_identity,
#     json_file_path='outputs/dolce/',
#     json_generic_file_name='dolce_identity_criteria',
#     timestr=timestr)

tablify_identity_criteria(
    json_file_location='outputs/dolce/dolce_identity_criteria_20230201-085854.json',
    table_location='outputs/dolce/dolce_identity_criteria_20230201-085854.xlsx')
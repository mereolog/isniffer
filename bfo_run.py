import os
import os
import time

from common.metadata_adorner import adorn_results_dict_with_metadata
from helpers.json_helpers import write_python_object_to_json_file
from objects.identity_criterion_recognition_config import IdentityCriterionRecognitionConfig
from recognizers.ci_recognizer import recognize_criteria_of_identity_in_theory
from recognizers.subsumptions_recognizer import find_type_subsumptions_in_theory
from recognizers.tautologicity_recognizer import find_tautological_i_identity_criteria_candidates_in_theory

timestr = time.strftime("%Y%m%d-%H%M%S")
logging_file_name = os.path.join('outputs/bfo_minus/', 'logging_' + timestr + '.log')

# bfo_type_subsumptions = \
#     find_type_subsumptions_in_theory(
#         theory_file_name='inputs/bfo_minus.tptp',
#         temp_file_path='outputs/bfo_minus/subsumptions/',
#         theory_id='bfo_minus',
#         keep_temp_files=True,
#         logging_file_name=logging_file_name)
#
# write_python_object_to_json_file(
#     python_object=bfo_type_subsumptions,
#     json_file_path='outputs/bfo_minus/',
#     json_generic_file_name='bfo_type_subsumptions',
#     timestr=timestr)


# bfo_tautological_i_identity_criteria_candidates = \
#     find_tautological_i_identity_criteria_candidates_in_theory(
#         theory_file_name='inputs/bfo_minus.tptp',
#         temp_file_path='outputs/bfo_minus/tautological_i_identity_criteria_candidates/',
#         theory_id='bfo_minus',
#         logging_file_name=logging_file_name,
#         keep_temp_files=True)
#
# write_python_object_to_json_file(
#     python_object=bfo_tautological_i_identity_criteria_candidates,
#     json_file_path='outputs/bfo_minus/',
#     json_generic_file_name='bfo_tautological_i_identity_criteria_candidates',
#     timestr=timestr)


# bfo_recognition_config_1 = \
#     IdentityCriterionRecognitionConfig(
#         non_tautologicity=False,
#         type_maximality=False,
#         uniqueness=False,
#         partial_exclusivity=False)
#
# bfo_criteria_of_identity = \
#     recognize_criteria_of_identity_in_theory(
#         theory_file_name='inputs/bfo_minus.tptp',
#         temp_file_path='outputs/bfo_minus/cis/',
#         theory_id='bfo_minus',
#         keep_temp_files=True,
#         type_subsumptions_in_theory_file_name='outputs/bfo_minus/bfo_type_subsumptions_20230130-140557.json',
#         tautological_ici_candidates_file_name='outputs/bfo_minus/bfo_tautological_i_identity_criteria_candidates_20230130-151144.json',
#         recognition_config=bfo_recognition_config_1,
#         logging_file_name=logging_file_name)
#
# adorned_bfo_criteria_of_identity = \
#     adorn_results_dict_with_metadata(
#         results_dict=bfo_criteria_of_identity,
#         recognition_config=bfo_recognition_config_1)
#
# write_python_object_to_json_file(
#     python_object=adorned_bfo_criteria_of_identity,
#     json_file_path='outputs/bfo_minus/',
#     json_generic_file_name='bfo_identity_criteria',
#     timestr=timestr)
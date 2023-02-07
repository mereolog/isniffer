import os
import os
import time

from common.metadata_adorner import adorn_results_dict_with_metadata
from helpers.json_helpers import write_python_object_to_json_file
from objects.identity_criterion_recognition_config import IdentityCriterionRecognitionConfig
from recognizers.ci_recognizer import recognize_criteria_of_identity_in_theory
from recognizers.subsumptions_recognizer import find_type_subsumptions_in_theory
from recognizers.tautologicity_recognizer import find_tautological_i_identity_criteria_candidates_in_theory
from tablifier import tablify_identity_criteria

timestr = time.strftime("%Y%m%d-%H%M%S")
logging_file_name = os.path.join('outputs/ufo/', 'logging_' + timestr + '.log')

# ufo_type_subsumptions = \
#     find_type_subsumptions_in_theory(
#         theory_file_name='inputs/ufo_fixed.tptp',
#         temp_file_path='outputs/ufo/subsumptions/',
#         theory_id='ufo',
#         keep_temp_files=True,
#         logging_file_name=logging_file_name)
#
# write_python_object_to_json_file(
#     python_object=ufo_type_subsumptions,
#     json_file_path='outputs/ufo/',
#     json_generic_file_name='ufo_type_subsumptions',
#     timestr=timestr)


# ufo_tautological_i_identity_criteria_candidates = \
#     find_tautological_i_identity_criteria_candidates_in_theory(
#         theory_file_name='inputs/ufo_fixed.tptp',
#         temp_file_path='outputs/ufo/tautological_i_identity_criteria_candidates/',
#         theory_id='ufo',
#         keep_temp_files=True)
#
# write_python_object_to_json_file(
#     python_object=ufo_tautological_i_identity_criteria_candidates,
#     json_file_path='outputs/ufo/',
#     json_generic_file_name='ufo_tautological_i_identity_criteria_candidates',
#     timestr=timestr)


# ufo_recognition_config_1 = \
#     IdentityCriterionRecognitionConfig(
#         non_tautologicity=True,
#         type_maximality=False,
#         uniqueness=False,
#         partial_exclusivity=False)
#
# ufo_criteria_of_identity = \
#     recognize_criteria_of_identity_in_theory(
#         theory_file_name='inputs/ufo_fixed.tptp',
#         temp_file_path='outputs/ufo/cis/',
#         theory_id='ufo',
#         keep_temp_files=True,
#         type_subsumptions_in_theory_file_name='outputs/ufo/ufo_type_subsumptions_20230202-145014.json',
#         tautological_ici_candidates_file_name='outputs/ufo/ufo_tautological_i_identity_criteria_candidates_20230202-061740.json',
#         recognition_config=ufo_recognition_config_1,
#         logging_file_name=logging_file_name)
#
# adorned_ufo_criteria_of_identity = \
#     adorn_results_dict_with_metadata(
#         results_dict=ufo_criteria_of_identity,
#         recognition_config=ufo_recognition_config_1)
#
# write_python_object_to_json_file(
#     python_object=adorned_ufo_criteria_of_identity,
#     json_file_path='outputs/ufo/',
#     json_generic_file_name='ufo_identity_criteria',
#     timestr=timestr)

tablify_identity_criteria(
    json_file_location='outputs/ufo/ufo_identity_criteria_20230203-084404_modified.json',
    table_location='outputs/ufo/ufo_identity_criteria_20230203-084404.xlsx')
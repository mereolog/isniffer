from helpers.json_helpers import read_python_object_from_json_file
from objects.identity_criterion_recognition_config import IdentityCriterionRecognitionConfig
from recognizers.reflexive_relations_recognizer import find_reflexive_relations_in_theory
from recognizers.subsumptions_recognizer import find_type_subsumptions_in_theory
from recognizers.tautologicity_recognizer import find_tautological_i_identity_criteria_candidates_in_theory


def get_support_data_if_required(
        theory: str,
        theory_id: str,
        temp_file_path: str,
        keep_temp_files: bool,
        type_subsumptions_in_theory_file_name: str,
        tautological_relations_file_name: str,
        recognition_config: IdentityCriterionRecognitionConfig) -> tuple:
    if type_subsumptions_in_theory_file_name == str():
        type_subsumptions = \
            find_type_subsumptions_in_theory(
                theory_file_name=theory,
                temp_file_path=temp_file_path,
                theory_id=theory_id,
                keep_temp_files=keep_temp_files)
    else:
        type_subsumptions = read_python_object_from_json_file(json_file_name=type_subsumptions_in_theory_file_name)
    
    if recognition_config.non_tautologicity:
        if tautological_relations_file_name == str():
            tautological_i_identity_criterion_candidates = \
                find_tautological_i_identity_criteria_candidates_in_theory(
                    theory_file_name=theory,
                    temp_file_path=temp_file_path,
                    theory_id=theory_id,
                    keep_temp_files=keep_temp_files)
        else:
            tautological_i_identity_criterion_candidates = read_python_object_from_json_file(json_file_name=tautological_relations_file_name)
    else:
        tautological_i_identity_criterion_candidates = set()
        
    # if recognition_config.non_circularity:
    #     if reflexive_relations_file_name == str():
    #         reflexive_relations = \
    #             find_reflexive_relations_in_theory(
    #                 theory_file_name=theory,
    #                 temp_file_path=temp_file_path,
    #                 theory_id=theory_id,
    #                 keep_temp_files=keep_temp_files)
    #     else:
    #         reflexive_relations = read_python_object_from_json_file(json_file_name=reflexive_relations_file_name)
    # else:
    #     reflexive_relations = set()
        
    return type_subsumptions, tautological_i_identity_criterion_candidates
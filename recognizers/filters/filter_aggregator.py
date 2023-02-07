import logging

from objects.identity_criterion_recognition_config import IdentityCriterionRecognitionConfig
from recognizers.filters.exclusivity_filter import filter_to_exclusive_cis
from recognizers.filters.subsumption_filter import filter_i_identity_criterion_by_relation_subsumptions
from recognizers.filters.uniqueness_filter import filter_to_unique_cis


def filter_identity_criteria(
        identity_criteria_for_types: dict,
        recognition_config: IdentityCriterionRecognitionConfig,
        theory: str,
        temp_file_path: str,
        keep_temp_files: bool) -> dict:
    logging.info('Filter identity criteria wrt requirements ')

    filtered_identity_criteria_for_types = identity_criteria_for_types.copy()
    
    if recognition_config.type_maximality:
        filtered_identity_criteria_for_types = \
            filter_i_identity_criterion_by_relation_subsumptions(
                identity_criteria_for_types=filtered_identity_criteria_for_types,
                theory=theory,
                temp_file_path=temp_file_path,
                keep_temp_files=keep_temp_files)
    if recognition_config.partial_exclusivity:
        filtered_identity_criteria_for_types = \
            filter_to_exclusive_cis(
                identity_criteria_for_types=filtered_identity_criteria_for_types)
    if recognition_config.uniqueness:
        filtered_identity_criteria_for_types = \
            filter_to_unique_cis(
                identity_criteria_for_types=filtered_identity_criteria_for_types)
    
    return filtered_identity_criteria_for_types

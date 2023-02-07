from objects.identity_criterion_recognition_config import IdentityCriterionRecognitionConfig


def adorn_results_dict_with_metadata(results_dict: dict, recognition_config: IdentityCriterionRecognitionConfig) -> dict:
    adorned_results_dict = results_dict.copy()
    metadata = \
        {
            'type_maximality': recognition_config.type_maximality,
            'non_tautologicity': recognition_config.non_tautologicity,
            'uniqueness': recognition_config.uniqueness,
            'partial_exclusivity': recognition_config.partial_exclusivity,
            'minimality': recognition_config.minimality,
            'non_vacuous': recognition_config.non_vacuous,
            'non_circularity': recognition_config.non_circularity,
            'informativness': recognition_config.informativness,
            'non_reflexivity': recognition_config.non_reflexivity,
        }
    adorned_results_dict = \
        adorned_results_dict | {'metadata' : metadata}
    
    return adorned_results_dict
class IdentityCriterionRecognitionConfig:
    def __init__(
            self,
            partial_exclusivity: bool,
            non_tautologicity: bool,
            type_maximality: bool,
            uniqueness: bool):
        self.non_vacuous = False
        self.informativness = False
        self.partial_exclusivity = partial_exclusivity
        self.minimality = False
        self.non_circularity = True
        self.non_tautologicity = non_tautologicity
        self.type_maximality = type_maximality
        self.uniqueness = uniqueness
        self.non_reflexivity = True
        
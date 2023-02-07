class IdentityCriterionCandidate:
    def __init__(self, relation: str, identity_position: int, arity=-1):
        super().__init__()
        self.relation = relation
        self.identity_position = identity_position
        self.arity = arity
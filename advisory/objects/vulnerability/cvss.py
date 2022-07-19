class CVSS:

    def __init__(
        self,
        vector_string: str,
        attack_vector: str,
        attack_complexity: str,
        privilegesRequired: str,
        userInteraction: str,
        scope: str,
        confidentialityImpact: str,
        integrity_impact: str,
        availabilityImpact: str,
        base_core: str,
        base_severity: str,
        exploitability_score: str,
        impact_score: str
    ) -> None:

        self.vector_string = vector_string
        self.attack_vector = attack_vector
        self.attack_complexity = attack_complexity
        self.privilegesRequired = privilegesRequired
        self.userInteraction = userInteraction
        self.scope = scope
        self.confidentialityImpact = confidentialityImpact
        self.integrity_impact = integrity_impact
        self.availabilityImpact = availabilityImpact
        self.base_core = base_core
        self.base_severity = base_severity
        self.exploitability_score = exploitability_score
        self.impact_score = impact_score
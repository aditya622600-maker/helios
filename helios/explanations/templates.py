from helios.contracts.models import CandidateInput

POSITIVE_LABELS = {
    "generation": "high modeled solar-generation potential",
    "physical": "strong usable-roof and shading profile",
    "grid": "favorable grid-proximity screening score",
    "economics": "favorable early economic screening score",
    "confidence": "comparatively strong input-data confidence",
}


def explain(candidate: CandidateInput) -> tuple[list[str], list[str]]:
    values = candidate.normalized.model_dump()
    ordered = sorted(values, key=values.get, reverse=True)
    positives = [POSITIVE_LABELS[name] for name in ordered[:2]]
    cautions: list[str] = []
    if candidate.metrics.shading_factor < 0.75:
        cautions.append("coarse shading proxy indicates possible obstruction losses")
    if candidate.normalized.confidence < 0.65:
        cautions.append("source quality or temporal alignment reduces confidence")
    if candidate.metrics.estimated_rent_inr_month is None:
        cautions.append("rent estimate is unavailable and excluded from economics")
    return positives, cautions

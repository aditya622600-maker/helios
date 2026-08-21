from helios.contracts.models import CandidateInput, Scenario, WeightSet


def exclusion_reasons(candidate: CandidateInput, scenario: Scenario) -> list[str]:
    reasons: list[str] = []
    if candidate.metrics.usable_area_m2 < scenario.minimum_usable_area_m2:
        reasons.append("usable_area_below_minimum")
    if (
        scenario.maximum_grid_distance_m is not None
        and candidate.metrics.grid_distance_m > scenario.maximum_grid_distance_m
    ):
        reasons.append("grid_distance_above_screening_limit")
    if (
        scenario.budget_inr is not None
        and candidate.metrics.estimated_cost_inr is not None
        and candidate.metrics.estimated_cost_inr > scenario.budget_inr
    ):
        reasons.append("estimated_cost_above_budget")
    return reasons


def component_scores(candidate: CandidateInput, weights: WeightSet) -> dict[str, float]:
    raw = candidate.normalized.model_dump()
    return {name: round(value * getattr(weights, name), 6) for name, value in raw.items()}


def total_score(components: dict[str, float]) -> float:
    return round(sum(components.values()), 6)

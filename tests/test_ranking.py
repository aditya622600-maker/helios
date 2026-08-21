from helios.contracts.models import CandidateInput, Scenario, WeightSet
from helios.ranking.scoring import component_scores, exclusion_reasons, total_score


def test_score_and_hard_filter(sample_request: dict) -> None:
    candidate = CandidateInput.model_validate(sample_request["candidates"][0])
    components = component_scores(candidate, WeightSet())
    assert total_score(components) == 0.8285
    assert exclusion_reasons(candidate, Scenario()) == []
    assert exclusion_reasons(candidate, Scenario(minimum_usable_area_m2=200)) == [
        "usable_area_below_minimum"
    ]

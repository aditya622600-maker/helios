import pytest
from pydantic import ValidationError

from helios.contracts.models import WeightSet


def test_weights_must_sum_to_one() -> None:
    with pytest.raises(ValidationError):
        WeightSet(generation=1, physical=1, grid=1, economics=1, confidence=1)

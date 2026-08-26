import pytest
from helios.features.economics import EconomicsInput, calculate_economic_feature
from helios.features.solar import SolarAssumptions, SolarResource, calculate_solar_feature


def f():
    return (
        pytest,
        EconomicsInput,
        calculate_economic_feature,
        SolarAssumptions,
        SolarResource,
        calculate_solar_feature,
    )

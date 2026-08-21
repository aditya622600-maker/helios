from datetime import date

import pytest


@pytest.fixture
def sample_request() -> dict:
    return {
        "region_name": "Demo Ward",
        "aoi_geojson": {
            "type": "Polygon",
            "coordinates": [[[72.80, 19.10], [72.81, 19.10], [72.81, 19.11], [72.80, 19.10]]],
        },
        "reference_date": date(2026, 8, 21).isoformat(),
        "candidates": [
            {
                "candidate_id": "roof-a",
                "name": "Demo rooftop",
                "geometry": {"type": "Point", "coordinates": [72.805, 19.105]},
                "metrics": {
                    "annual_yield_kwh": 25000,
                    "usable_area_m2": 180,
                    "shading_factor": 0.88,
                    "grid_distance_m": 320,
                    "estimated_cost_inr": 900000,
                    "estimated_rent_inr_month": 12000,
                    "provenance_ids": ["nasa-power", "osm"],
                },
                "normalized": {
                    "generation": 0.91,
                    "physical": 0.86,
                    "grid": 0.78,
                    "economics": 0.72,
                    "confidence": 0.81,
                },
            }
        ],
    }

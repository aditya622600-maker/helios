import geopandas as gpd
import json
import numpy as np

print("[1/3] Adding terrain elevation to kharghar_buildings_clean.geojson...")
gdf = gpd.read_file("kharghar_buildings_clean.geojson")

# Model Kharghar's terrain elevation (0m coastal creek baseline up to ~65m towards Kharghar hills)
centroids = gdf.geometry.centroid
lats = centroids.y
lons = centroids.x

gdf['terrain_elevation_m'] = np.round(
    10.0 + (lats - 19.0100) * 320.0 + (lons - 73.0450) * 180.0, 1
)

export_cols = [
    'candidate_id', 'reported_height_m', 'height_confidence', 
    'terrain_elevation_m', 'source', 'geometry'
]
gdf[export_cols].to_file("kharghar_buildings_clean.geojson", driver="GeoJSON")
print(f" Updated {len(gdf)} records with terrain elevation.")

# -------------------------------------------------------------
# 2. Register Solar & Economic Parameters (For Person 3)
# -------------------------------------------------------------
print("[2/3] Generating solar_economic_inputs.json...")
solar_economic_constants = {
    "location": {
        "name": "Kharghar, Navi Mumbai",
        "latitude": 19.0425,
        "longitude": 73.0675,
        "elevation_m_avg": 18.0
    },
    "solar_parameters": {
        "ghi_kwh_m2_year": 1980.0,
        "specific_yield_kwh_kwp_year": 1450.0,
        "panel_efficiency_default": 0.21,
        "system_derate_factor": 0.82,
        "usable_roof_factor_flat": 0.70
    },
    "economic_parameters_inr": {
        "capex_per_kwp_commercial_inr": 48000,
        "capex_per_kwp_residential_inr": 55000,
        "om_per_kwp_year_inr": 800,
        "avg_commercial_tariff_kwh_inr": 9.50,
        "avg_residential_tariff_kwh_inr": 7.20,
        "estimated_roof_rent_inr_m2_month": 35.0
    },
    "provenance": {
        "tariff_source": "MSEDCL Tariff Order (MMR Region)",
        "solar_source": "MNRE India / NREL PVWatts Baseline",
        "date_registered": "2026"
    }
}

with open("solar_economic_inputs.json", "w") as f:
    json.dump(solar_economic_constants, f, indent=2)
print(" Saved: solar_economic_inputs.json")

# -------------------------------------------------------------
# 3. Create Sample Package (10 Buildings for Instant Handoff)
# -------------------------------------------------------------
print("[3/3] Creating sample handoff file...")
sample_gdf = gdf.head(10).copy()
sample_gdf.to_file("sample_kharghar_buildings.geojson", driver="GeoJSON")
print(" Saved: sample_kharghar_buildings.geojson")
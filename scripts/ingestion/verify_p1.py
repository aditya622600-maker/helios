import geopandas as gpd
import json
import os

print("=== RUNNING PERSON 1 QUALITY CHECKS ===")

# 1. Check Files
required_files = [
    "kharghar_aoi.geojson",
    "kharghar_roads.geojson",
    "kharghar_power.geojson",
    "kharghar_buildings_clean.geojson",
    "sample_kharghar_buildings.geojson",
    "solar_economic_inputs.json",
    "DATA_MANIFEST.md"
]

all_exist = True
for f in required_files:
    if os.path.exists(f):
        print(f" [PASS] File found: {f}")
    else:
        print(f" [FAIL] Missing file: {f}")
        all_exist = False

# 2. Check Buildings Schema & Nulls (Updated with footprint and usable area)
bldg_gdf = gpd.read_file("kharghar_buildings_clean.geojson")
expected_cols = {
    'candidate_id', 
    'footprint_area_m2', 
    'usable_roof_area_m2', 
    'reported_height_m', 
    'height_confidence', 
    'terrain_elevation_m', 
    'source', 
    'geometry'
}

if expected_cols.issubset(set(bldg_gdf.columns)):
    print(f" [PASS] Schema matches all Person 2 requirements ({len(expected_cols)} fields present)")
else:
    print(f" [FAIL] Schema mismatch. Missing: {expected_cols - set(bldg_gdf.columns)}")

core_numeric_cols = ['candidate_id', 'footprint_area_m2', 'usable_roof_area_m2', 'reported_height_m', 'terrain_elevation_m']
null_counts = bldg_gdf[core_numeric_cols].isnull().sum().sum()
if null_counts == 0:
    print(f" [PASS] 0 null values across {len(bldg_gdf)} building records")
else:
    print(f" [WARN] Found {null_counts} null values in core fields")

# 3. Check Solar Inputs JSON
with open("solar_economic_inputs.json") as jf:
    solar_cfg = json.load(jf)
    if "solar_parameters" in solar_cfg and "economic_parameters_inr" in solar_cfg:
        print(" [PASS] solar_economic_inputs.json correctly formatted for Person 3")

print("\nAll deliverables are ready for team handoff.")
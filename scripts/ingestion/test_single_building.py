import geopandas as gpd
import json

# 1. Load Clean Buildings Dataset
gdf = gpd.read_file("kharghar_buildings_clean.geojson")

# Select a target building (e.g., KHAR_000123 or the first record)
target_id = "KHAR_000126"
building_match = gdf[gdf['candidate_id'] == target_id]

if building_match.empty:
    bldg = gdf.iloc[0]
else:
    bldg = building_match.iloc[0]

# 2. Load Solar-Economic Constants
with open("solar_economic_inputs.json", "r") as f:
    solar_cfg = json.load(f)

# 3. Print Structured Verification Report
print("=" * 55)
print(f"   HELIOS DATA AUDIT - SINGLE CANDIDATE TEST")
print("=" * 55)
print(f"Candidate ID       : {bldg['candidate_id']}")
print(f"Data Source        : {bldg['source']}")
print("-" * 55)
print("GEOMETRIC & PHYSICAL ATTRIBUTES:")
print(f"• Footprint Area   : {bldg['footprint_area_m2']} m²")
print(f"• Usable Roof Area : {bldg['usable_roof_area_m2']} m² (~{round((bldg['usable_roof_area_m2']/bldg['footprint_area_m2'])*100)}% of footprint)")
print(f"• Structure Height : {bldg['reported_height_m']} m (Confidence: {bldg['height_confidence']})")
print(f"• Base Elevation   : {bldg['terrain_elevation_m']} m above sea level")
print("-" * 55)
print("GEOGRAPHIC COORDINATES (EPSG:4326):")
centroid = bldg.geometry.centroid
print(f"• Centroid (Lat/Lon): {centroid.y:.6f}° N, {centroid.x:.6f}° E")
print(f"• Polygon Vertices  : {len(bldg.geometry.exterior.coords)} boundary points")
print("-" * 55)
print("GLOBAL SOLAR/ECONOMIC CONTEXT (For downstream engines):")
print(f"• Target Region    : {solar_cfg['location']['name']}")
print(f"• Baseline Yield   : {solar_cfg['solar_parameters']['specific_yield_kwh_kwp_year']} kWh/kWp/year")
print(f"• Commercial Capex : ₹{solar_cfg['economic_parameters_inr']['capex_per_kwp_commercial_inr']:,}/kWp")
print("=" * 55)

# 4. JSON Serialization Check (Person 5 API Hand-off compatibility)
print("\nJSON API Compatibility Sample:")
print(json.dumps(bldg.drop('geometry').to_dict(), indent=2))
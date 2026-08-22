import geopandas as gpd
import numpy as np

print("Calculating Footprint and Usable Rooftop Areas...")
gdf = gpd.read_file("kharghar_buildings_clean.geojson")

# 1. Project to UTM Zone 43N (meters) for accurate metric area calculations
gdf_metric = gdf.to_crs(epsg=32643)

# 2. Total Footprint Area (m²)
gdf['footprint_area_m2'] = gdf_metric.geometry.area.round(1)

# 3. Estimated Usable Rooftop Area (m²)
# For typical flat RCC roofs: ~65-70% usable space after edge setbacks (1.5m),
# elevator lift rooms, overhead water tanks, and maintenance walkways.
gdf['usable_roof_area_m2'] = np.round(gdf['footprint_area_m2'] * 0.68, 1)

# Keep standard WGS 84 coordinate system for file export
gdf = gdf.to_crs(epsg=4326)

# Organize columns cleanly
ordered_cols = [
    'candidate_id',
    'footprint_area_m2',
    'usable_roof_area_m2',
    'reported_height_m',
    'height_confidence',
    'terrain_elevation_m',
    'source',
    'geometry'
]

gdf = gdf[ordered_cols]

# Save updated production & sample files
gdf.to_file("kharghar_buildings_clean.geojson", driver="GeoJSON")
gdf.head(10).to_file("sample_kharghar_buildings.geojson", driver="GeoJSON")

print(f" Updated {len(gdf)} buildings with both footprint and usable roof area.")
print("\nSample preview:")
print(gdf[['candidate_id', 'footprint_area_m2', 'usable_roof_area_m2', 'reported_height_m']].head(3).to_string(index=False))
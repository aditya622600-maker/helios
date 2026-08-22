import geopandas as gpd
import osmnx as ox
from shapely.geometry import box
from shapely.validation import make_valid
import warnings
warnings.filterwarnings('ignore')

# -------------------------------------------------------------
# 1. Define Kharghar AOI Bounding Box (Sectors 1 to 36 + Central Park)
# Coordinates: [west, south, east, north]
# -------------------------------------------------------------
WEST, SOUTH, EAST, NORTH = 73.0450, 19.0100, 73.0900, 19.0750
BBOX_TUPLE = (WEST, SOUTH, EAST, NORTH)

print("[1/4] Freezing Kharghar Boundary...")
bbox_geom = box(WEST, SOUTH, EAST, NORTH)
boundary_gdf = gpd.GeoDataFrame({'name': ['Kharghar AOI'], 'geometry': [bbox_geom]}, crs="EPSG:4326")
boundary_gdf.to_file("kharghar_aoi.geojson", driver="GeoJSON")
print(" Saved: kharghar_aoi.geojson")

# Helper function to support all OSMnx versions
def fetch_osm_features(tags):
    try:
        # OSMnx v2.0+ uses bbox=(west, south, east, north)
        return ox.features_from_bbox(bbox=BBOX_TUPLE, tags=tags)
    except TypeError:
        # OSMnx v1.x uses positional: (north, south, east, west)
        return ox.geometries_from_bbox(NORTH, SOUTH, EAST, WEST, tags=tags)

# -------------------------------------------------------------
# 2. Extract Roads as Line Features (No graph topology required)
# -------------------------------------------------------------
print("[2/4] Fetching Road network...")
try:
    roads_raw = fetch_osm_features(tags={"highway": True})
    roads_gdf = roads_raw[roads_raw.geometry.type.isin(['LineString', 'MultiLineString'])].copy()
    keep_cols = [c for c in ['name', 'highway', 'geometry'] if c in roads_gdf.columns]
    roads_gdf = roads_gdf[keep_cols].reset_index(drop=True).to_crs(epsg=4326)
    roads_gdf.to_file("kharghar_roads.geojson", driver="GeoJSON")
    print(f" Saved {len(roads_gdf)} road segments -> kharghar_roads.geojson")
except Exception as e:
    print(f" Warning on roads: {e}")

# -------------------------------------------------------------
# 3. Extract Power Infrastructure
# -------------------------------------------------------------
print("[3/4] Fetching Power Infrastructure...")
try:
    power_tags = {"power": ["substation", "transformer", "line", "minor_line", "plant", "cable"]}
    power_raw = fetch_osm_features(tags=power_tags)
    if not power_raw.empty:
        keep_pwr = [c for c in ['name', 'power', 'geometry'] if c in power_raw.columns]
        power_gdf = power_raw[keep_pwr].reset_index(drop=True).to_crs(epsg=4326)
        power_gdf.to_file("kharghar_power.geojson", driver="GeoJSON")
        print(f" Saved {len(power_gdf)} power entities -> kharghar_power.geojson")
    else:
        print(" No power entities found in OSM.")
except Exception as e:
    print(f" Warning on power: {e}")

# -------------------------------------------------------------
# 4. Extract Buildings, Repair, Filter, & Assign KHAR_xxxx IDs
# -------------------------------------------------------------
print("[4/4] Fetching and processing building footprints...")
bldg_raw = fetch_osm_features(tags={"building": True})

# Keep only 2D polygons
buildings_gdf = bldg_raw[bldg_raw.geometry.type.isin(['Polygon', 'MultiPolygon'])].copy()
print(f"   Raw polygons downloaded: {len(buildings_gdf)}")

# Geometry repair
buildings_gdf['geometry'] = buildings_gdf['geometry'].apply(make_valid)

# Project to UTM 43N (meters) for accurate area filtering
buildings_gdf = buildings_gdf.to_crs(epsg=32643)
buildings_gdf['footprint_m2'] = buildings_gdf.geometry.area

# Remove slivers/artifacts smaller than 20 m²
buildings_gdf = buildings_gdf[buildings_gdf['footprint_m2'] >= 20.0].copy()

# Reproject back to WGS 84 (EPSG:4326)
buildings_gdf = buildings_gdf.to_crs(epsg=4326).reset_index(drop=True)

# Generate Candidate IDs
buildings_gdf['candidate_id'] = [f"KHAR_{i+1:06d}" for i in range(len(buildings_gdf))]

# Height extraction fallback
def parse_height(row):
    h_val = str(row.get('height', ''))
    h_clean = ''.join([c for c in h_val if c.isdigit() or c == '.'])
    if h_clean:
        try:
            return round(float(h_clean), 1), 0.90
        except ValueError:
            pass
    
    lvl_val = str(row.get('building:levels', ''))
    lvl_clean = ''.join([c for c in lvl_val if c.isdigit() or c == '.'])
    if lvl_clean:
        try:
            return round(float(lvl_clean) * 3.2, 1), 0.75
        except ValueError:
            pass
            
    return 14.0, 0.40

height_data = buildings_gdf.apply(parse_height, axis=1)
buildings_gdf['reported_height_m'] = [h[0] for h in height_data]
buildings_gdf['height_confidence'] = [h[1] for h in height_data]
buildings_gdf['source'] = "OSM"

# Export handoff file
export_cols = ['candidate_id', 'reported_height_m', 'height_confidence', 'source', 'geometry']
buildings_gdf[export_cols].to_file("kharghar_buildings_clean.geojson", driver="GeoJSON")

print(f"\n Handoff complete: {len(buildings_gdf)} clean buildings saved to 'kharghar_buildings_clean.geojson'")
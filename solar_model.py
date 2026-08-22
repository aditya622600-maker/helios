import pandas as pd
import numpy as np
import requests
import pvlib
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = "buildings.csv"
OUTPUT_FILE = "solar_results.csv"

TIMEZONE = "Asia/Kolkata"

# Solar panel parameters
PANEL_EFFICIENCY = 0.22       # 22%
TEMP_COEFFICIENT = -0.004     # -0.4% per °C above 25°C
REFERENCE_CELL_TEMP = 25.0

# Fraction of usable roof covered with panels
ROOF_COVERAGE = 0.70

# Total system losses
SYSTEM_LOSS_FACTOR = 0.90

# Default panel orientation
DEFAULT_PANEL_TILT = 20.0
DEFAULT_PANEL_AZIMUTH = 180.0

# Wind profile reference heights
WIND_HEIGHT_10M = 10.0
WIND_HEIGHT_80M = 80.0
WIND_HEIGHT_120M = 120.0


# ============================================================
# HELPER: FIND COLUMN
# ============================================================

def find_column(df, possible_names, required=True):

    # Exact match
    for name in possible_names:
        if name in df.columns:
            return name

    # Case-insensitive match
    lower_columns = {
        column.lower().strip(): column
        for column in df.columns
    }

    for name in possible_names:
        if name.lower().strip() in lower_columns:
            return lower_columns[name.lower().strip()]

    if required:
        raise ValueError(
            f"Missing column. Expected one of:\n{possible_names}\n\n"
            f"Available columns are:\n{list(df.columns)}"
        )

    return None


# ============================================================
# LOAD BUILDING DATA
# ============================================================

def load_buildings():

    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"\nERROR: Cannot find '{INPUT_FILE}'.\n"
            f"Make sure it is inside the same folder as solar_model.py"
        )

    candidate_col = find_column(
        df,
        [
            "candidate_id",
            "Candidate_ID",
            "id",
            "building_id"
        ]
    )

    latitude_col = find_column(
        df,
        [
            "latitude",
            "Latitude",
            "lat"
        ]
    )

    longitude_col = find_column(
        df,
        [
            "longitude",
            "Longitude",
            "lon",
            "lng"
        ]
    )

    usable_area_col = find_column(
        df,
        [
            "usable_area_m2",
            "usable_roof_area",
            "usable_roof_area_m2",
            "usable_area",
            "roof_area",
            "roof_area_m2"
        ]
    )

    building_height_col = find_column(
        df,
        [
            "building_height_m",
            "building_height",
            "height_m",
            "height"
        ]
    )

    shading_col = find_column(
        df,
        [
            "shading_factor",
            "shading",
            "shade_factor"
        ],
        required=False
    )

    tilt_col = find_column(
        df,
        [
            "panel_tilt",
            "tilt",
            "panel_tilt_deg"
        ],
        required=False
    )

    azimuth_col = find_column(
        df,
        [
            "panel_azimuth",
            "azimuth",
            "panel_azimuth_deg"
        ],
        required=False
    )

    buildings = []

    for _, row in df.iterrows():

        building = {

            "candidate_id":
                str(row[candidate_col]),

            "latitude":
                float(row[latitude_col]),

            "longitude":
                float(row[longitude_col]),

            "usable_area_m2":
                float(row[usable_area_col]),

            "building_height_m":
                float(row[building_height_col]),

            "shading_factor":
                float(row[shading_col])
                if shading_col is not None
                else 1.0,

            "panel_tilt":
                float(row[tilt_col])
                if tilt_col is not None
                else DEFAULT_PANEL_TILT,

            "panel_azimuth":
                float(row[azimuth_col])
                if azimuth_col is not None
                else DEFAULT_PANEL_AZIMUTH
        }

        buildings.append(building)

    return buildings


# ============================================================
# DOWNLOAD WEATHER + SOLAR DATA
# ============================================================

def get_weather_data(latitude, longitude):

    print(
        f"\nDownloading weather and solar data for "
        f"{latitude}, {longitude}..."
    )

    url = "https://api.open-meteo.com/v1/forecast"

    params = {

        "latitude": latitude,

        "longitude": longitude,

        "hourly": ",".join([
            "temperature_2m",
            "cloud_cover",

            "wind_speed_10m",
            "wind_speed_80m",
            "wind_speed_120m",

            "shortwave_radiation",
            "direct_normal_irradiance",
            "diffuse_radiation"
        ]),

        "timezone": "Asia/Kolkata",

        "forecast_days": 16
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if "hourly" not in data:
        raise ValueError(
            "Weather API did not return hourly data."
        )

    hourly = data["hourly"]

    weather = pd.DataFrame({

        "time":
            pd.to_datetime(hourly["time"]),

        "temperature_c":
            hourly["temperature_2m"],

        "cloud_cover":
            hourly["cloud_cover"],

        "wind_speed_10m":
            hourly["wind_speed_10m"],

        "wind_speed_80m":
            hourly["wind_speed_80m"],

        "wind_speed_120m":
            hourly["wind_speed_120m"],

        "ghi":
            hourly["shortwave_radiation"],

        "dni":
            hourly["direct_normal_irradiance"],

        "dhi":
            hourly["diffuse_radiation"]
    })

    # Open-Meteo times are local time because timezone=Asia/Kolkata
    weather["time"] = weather["time"].dt.tz_localize(
        TIMEZONE
    )

    weather = weather.set_index("time")

    return weather


# ============================================================
# GET EXACT WEATHER HOUR
# ============================================================

def get_weather_for_time(weather, selected_timestamp):

    if selected_timestamp.tzinfo is None:

        selected_timestamp = selected_timestamp.tz_localize(
            TIMEZONE
        )

    else:

        selected_timestamp = selected_timestamp.tz_convert(
            TIMEZONE
        )

    if selected_timestamp not in weather.index:

        start_time = weather.index.min()
        end_time = weather.index.max()

        raise ValueError(

            f"\nSelected time is not available from the API.\n\n"

            f"You selected:\n"
            f"{selected_timestamp}\n\n"

            f"Available API range:\n"
            f"{start_time}\n"
            f"to\n"
            f"{end_time}\n\n"

            f"Choose an hour inside this range."
        )

    data = weather.loc[selected_timestamp]

    return {

        "api_time":
            selected_timestamp,

        "temperature_c":
            float(data["temperature_c"]),

        "cloud_cover":
            float(data["cloud_cover"]),

        "wind_speed_10m":
            float(data["wind_speed_10m"]),

        "wind_speed_80m":
            float(data["wind_speed_80m"]),

        "wind_speed_120m":
            float(data["wind_speed_120m"]),

        "ghi":
            max(0.0, float(data["ghi"])),

        "dni":
            max(0.0, float(data["dni"])),

        "dhi":
            max(0.0, float(data["dhi"]))
    }


# ============================================================
# WIND SPEED AT BUILDING HEIGHT
# ============================================================

def calculate_wind_at_height(
    building_height,
    wind_10m,
    wind_80m,
    wind_120m
):

    # Prevent invalid heights
    if building_height <= 0:
        return wind_10m

    # Reference data
    heights = np.array([
        WIND_HEIGHT_10M,
        WIND_HEIGHT_80M,
        WIND_HEIGHT_120M
    ])

    winds = np.array([
        wind_10m,
        wind_80m,
        wind_120m
    ])

    # If below 10m, use power-law extrapolation
    if building_height <= 10:

        reference_height = 10.0
        reference_wind = wind_10m

        alpha = 0.20

        wind_at_height = (
            reference_wind *
            (building_height / reference_height) ** alpha
        )

        return max(0.0, wind_at_height)

    # --------------------------------------------------------
    # Between 10m and 80m
    # Calculate local Hellmann exponent
    # --------------------------------------------------------

    if building_height <= 80:

        if wind_10m > 0 and wind_80m > 0:

            alpha = (
                np.log(wind_80m / wind_10m)
                /
                np.log(80.0 / 10.0)
            )

            wind_at_height = (
                wind_10m *
                (building_height / 10.0) ** alpha
            )

        else:

            wind_at_height = np.interp(
                building_height,
                heights,
                winds
            )

        return max(0.0, wind_at_height)

    # --------------------------------------------------------
    # Between 80m and 120m
    # --------------------------------------------------------

    if building_height <= 120:

        if wind_80m > 0 and wind_120m > 0:

            alpha = (
                np.log(wind_120m / wind_80m)
                /
                np.log(120.0 / 80.0)
            )

            wind_at_height = (
                wind_80m *
                (building_height / 80.0) ** alpha
            )

        else:

            wind_at_height = np.interp(
                building_height,
                heights,
                winds
            )

        return max(0.0, wind_at_height)

    # --------------------------------------------------------
    # Above 120m
    # Extrapolate using power law from 80m → 120m
    # --------------------------------------------------------

    if wind_80m > 0 and wind_120m > 0:

        alpha = (
            np.log(wind_120m / wind_80m)
            /
            np.log(120.0 / 80.0)
        )

        wind_at_height = (
            wind_120m *
            (building_height / 120.0) ** alpha
        )

    else:

        wind_at_height = wind_120m

    return max(0.0, wind_at_height)


# ============================================================
# SOLAR POSITION
# ============================================================

def get_solar_position(
    latitude,
    longitude,
    timestamp,
    candidate_id
):

    if timestamp.tzinfo is None:

        timestamp = timestamp.tz_localize(
            TIMEZONE
        )

    else:

        timestamp = timestamp.tz_convert(
            TIMEZONE
        )

    location = pvlib.location.Location(

        latitude=latitude,

        longitude=longitude,

        tz=TIMEZONE,

        name=candidate_id
    )

    solar_position = location.get_solarposition(
        pd.DatetimeIndex([timestamp])
    )

    zenith = float(
        solar_position["apparent_zenith"].iloc[0]
    )

    azimuth = float(
        solar_position["azimuth"].iloc[0]
    )

    return zenith, azimuth


# ============================================================
# CALCULATE POA IRRADIANCE
# ============================================================

def calculate_poa_irradiance(

    latitude,
    longitude,
    timestamp,

    ghi,
    dni,
    dhi,

    panel_tilt,
    panel_azimuth,

    candidate_id
):

    if timestamp.tzinfo is None:

        timestamp = timestamp.tz_localize(
            TIMEZONE
        )

    else:

        timestamp = timestamp.tz_convert(
            TIMEZONE
        )

    # Get solar position
    solar_zenith, solar_azimuth = get_solar_position(

        latitude,
        longitude,
        timestamp,
        candidate_id
    )

    # Nighttime check
    if solar_zenith >= 90:

        return 0.0, solar_zenith, solar_azimuth

    # Extraterrestrial DNI
    dni_extra = pvlib.irradiance.get_extra_radiation(

        pd.DatetimeIndex([timestamp])

    ).iloc[0]

    # Hay-Davies transposition model
    poa = pvlib.irradiance.get_total_irradiance(

        surface_tilt=panel_tilt,

        surface_azimuth=panel_azimuth,

        solar_zenith=solar_zenith,

        solar_azimuth=solar_azimuth,

        dni=dni,

        ghi=ghi,

        dhi=dhi,

        dni_extra=dni_extra,

        model="haydavies"
    )

    poa_global = float(
        poa["poa_global"]
    )

    poa_global = max(
        0.0,
        poa_global
    )

    return poa_global, solar_zenith, solar_azimuth


# ============================================================
# CELL TEMPERATURE
# ============================================================

def calculate_cell_temperature(

    ambient_temperature,

    poa_irradiance,

    wind_speed
):

    # Simplified thermal model:
    #
    # More irradiance -> hotter panel
    # More wind -> more cooling

    if poa_irradiance <= 0:

        return ambient_temperature

    temperature_rise = (

        (poa_irradiance / 800.0)

        *
        (20.0 / (1.0 + 0.15 * wind_speed))
    )

    cell_temperature = (

        ambient_temperature
        +
        temperature_rise
    )

    return cell_temperature


# ============================================================
# TEMPERATURE-ADJUSTED PANEL EFFICIENCY
# ============================================================

def calculate_panel_efficiency(
    cell_temperature
):

    efficiency = (

        PANEL_EFFICIENCY
        *
        (
            1
            +
            TEMP_COEFFICIENT
            *
            (
                cell_temperature
                -
                REFERENCE_CELL_TEMP
            )
        )
    )

    efficiency = max(
        0.0,
        efficiency
    )

    return efficiency


# ============================================================
# SOLAR POWER CALCULATION
# ============================================================

def calculate_solar_power(
    building,
    selected_timestamp
):

    candidate_id = building["candidate_id"]

    latitude = building["latitude"]
    longitude = building["longitude"]

    usable_area = building["usable_area_m2"]

    building_height = building[
        "building_height_m"
    ]

    shading_factor = building[
        "shading_factor"
    ]

    panel_tilt = building[
        "panel_tilt"
    ]

    panel_azimuth = building[
        "panel_azimuth"
    ]

    # --------------------------------------------------------
    # Download location-specific weather
    # --------------------------------------------------------

    weather = get_weather_data(
        latitude,
        longitude
    )

    weather_data = get_weather_for_time(
        weather,
        selected_timestamp
    )

    # --------------------------------------------------------
    # Panel area
    # --------------------------------------------------------

    panel_area = (
        usable_area
        *
        ROOF_COVERAGE
    )

    # --------------------------------------------------------
    # Wind speed at actual building height
    # --------------------------------------------------------

    wind_at_height = calculate_wind_at_height(

        building_height,

        weather_data["wind_speed_10m"],

        weather_data["wind_speed_80m"],

        weather_data["wind_speed_120m"]
    )

    # --------------------------------------------------------
    # POA irradiance
    # --------------------------------------------------------

    poa_irradiance, solar_zenith, solar_azimuth = (

        calculate_poa_irradiance(

            latitude=latitude,

            longitude=longitude,

            timestamp=selected_timestamp,

            ghi=weather_data["ghi"],

            dni=weather_data["dni"],

            dhi=weather_data["dhi"],

            panel_tilt=panel_tilt,

            panel_azimuth=panel_azimuth,

            candidate_id=candidate_id
        )
    )

    # --------------------------------------------------------
    # Cell temperature
    # --------------------------------------------------------

    cell_temperature = calculate_cell_temperature(

        ambient_temperature=
            weather_data["temperature_c"],

        poa_irradiance=
            poa_irradiance,

        wind_speed=
            wind_at_height
    )

    # --------------------------------------------------------
    # Temperature-adjusted efficiency
    # --------------------------------------------------------

    panel_efficiency = (

        calculate_panel_efficiency(
            cell_temperature
        )
    )

    # --------------------------------------------------------
    # Power calculation
    #
    # Power = POA × Area × Efficiency
    #
    # Divide by 1000 to convert W -> kW
    # --------------------------------------------------------

    raw_power_kw = (

        poa_irradiance

        *
        panel_area

        *
        panel_efficiency

        / 1000
    )

    # Apply shading

    shaded_power_kw = (

        raw_power_kw
        *
        shading_factor
    )

    # Apply system losses

    final_power_kw = (

        shaded_power_kw
        *
        SYSTEM_LOSS_FACTOR
    )

    final_power_kw = max(
        0.0,
        final_power_kw
    )

    # --------------------------------------------------------
    # Estimated installed capacity
    # --------------------------------------------------------

    estimated_capacity_kwp = (

        panel_area
        *
        PANEL_EFFICIENCY
        *
        1000
        / 1000
    )

    # Simplifies to:
    #
    # panel_area × panel efficiency
    #
    # because STC irradiance = 1000 W/m²

    return {

        "candidate_id":
            candidate_id,

        "latitude":
            latitude,

        "longitude":
            longitude,

        "requested_time":
            selected_timestamp,

        "api_data_time":
            weather_data["api_time"],

        "usable_area_m2":
            usable_area,

        "building_height_m":
            building_height,

        "shading_factor":
            shading_factor,

        "panel_area_m2":
            panel_area,

        "estimated_capacity_kwp":
            estimated_capacity_kwp,

        "panel_tilt_deg":
            panel_tilt,

        "panel_azimuth_deg":
            panel_azimuth,

        "temperature_c":
            weather_data["temperature_c"],

        "cloud_cover_percent":
            weather_data["cloud_cover"],

        "wind_speed_10m":
            weather_data["wind_speed_10m"],

        "wind_speed_80m":
            weather_data["wind_speed_80m"],

        "wind_speed_120m":
            weather_data["wind_speed_120m"],

        "wind_speed_at_building_height":
            wind_at_height,

        "ghi_w_m2":
            weather_data["ghi"],

        "dni_w_m2":
            weather_data["dni"],

        "dhi_w_m2":
            weather_data["dhi"],

        "solar_zenith_deg":
            solar_zenith,

        "solar_azimuth_deg":
            solar_azimuth,

        "poa_irradiance_w_m2":
            poa_irradiance,

        "cell_temperature_c":
            cell_temperature,

        "panel_efficiency_percent":
            panel_efficiency * 100,

        "predicted_power_kw":
            final_power_kw
    }


# ============================================================
# DISPLAY RESULT
# ============================================================

def print_result(result):

    print("\n")
    print("=" * 60)
    print("SOLAR ROOFTOP ANALYSIS")
    print("=" * 60)

    print(f"\nCandidate ID: {result['candidate_id']}")

    print(
        f"Location: "
        f"{result['latitude']}, "
        f"{result['longitude']}"
    )

    print(
        f"Usable Roof Area: "
        f"{result['usable_area_m2']:.2f} m²"
    )

    print(
        f"Building Height: "
        f"{result['building_height_m']:.2f} m"
    )

    print(
        f"Shading Factor: "
        f"{result['shading_factor']}"
    )

    print("\n--- SOLAR SYSTEM ---\n")

    print(
        f"Panel Area: "
        f"{result['panel_area_m2']:.2f} m²"
    )

    print(
        f"Estimated Capacity: "
        f"{result['estimated_capacity_kwp']:.2f} kWp"
    )

    print(
        f"Panel Tilt: "
        f"{result['panel_tilt_deg']:.2f}°"
    )

    print(
        f"Panel Azimuth: "
        f"{result['panel_azimuth_deg']:.2f}°"
    )

    print("\n--- SELECTED DATE & TIME ---\n")

    print(
        f"Requested Time: "
        f"{result['requested_time']}"
    )

    print(
        f"API Data Time Used: "
        f"{result['api_data_time']}"
    )

    print("\n--- WEATHER CONDITIONS ---\n")

    print(
        f"Temperature: "
        f"{result['temperature_c']:.2f} °C"
    )

    print(
        f"Cloud Cover: "
        f"{result['cloud_cover_percent']:.2f} %"
    )

    print(
        f"\nWind Speed at 10 m: "
        f"{result['wind_speed_10m']:.2f} m/s"
    )

    print(
        f"Wind Speed at 80 m: "
        f"{result['wind_speed_80m']:.2f} m/s"
    )

    print(
        f"Wind Speed at 120 m: "
        f"{result['wind_speed_120m']:.2f} m/s"
    )

    print(
        f"\nWind Height Used: "
        f"{result['building_height_m']:.2f} m"
    )

    print(
        f"Power-Law Wind Speed: "
        f"{result['wind_speed_at_building_height']:.2f} m/s"
    )

    print("\n--- SOLAR POSITION ---\n")

    print(
        f"Solar Zenith: "
        f"{result['solar_zenith_deg']:.2f}°"
    )

    print(
        f"Solar Azimuth: "
        f"{result['solar_azimuth_deg']:.2f}°"
    )

    print("\n--- SOLAR IRRADIANCE ---\n")

    print(
        f"GHI: "
        f"{result['ghi_w_m2']:.2f} W/m²"
    )

    print(
        f"DNI: "
        f"{result['dni_w_m2']:.2f} W/m²"
    )

    print(
        f"DHI: "
        f"{result['dhi_w_m2']:.2f} W/m²"
    )

    print(
        f"POA Irradiance: "
        f"{result['poa_irradiance_w_m2']:.2f} W/m²"
    )

    print("\n--- PV PERFORMANCE ---\n")

    print(
        f"Cell Temperature: "
        f"{result['cell_temperature_c']:.2f} °C"
    )

    print(
        f"Panel Efficiency: "
        f"{result['panel_efficiency_percent']:.2f} %"
    )

    print("\n--- POWER RESULT ---\n")

    print(
        f"Predicted Solar Power: "
        f"{result['predicted_power_kw']:.2f} kW"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("=" * 60)
    print("SOLAR ROOFTOP POWER PREDICTION")
    print("=" * 60)

    # --------------------------------------------------------
    # User input
    # --------------------------------------------------------

    user_input = input(

        "\nEnter date and time "
        "(YYYY-MM-DD HH:MM): "

    ).strip()

    try:

        selected_timestamp = pd.Timestamp(
            user_input
        )

        selected_timestamp = (
            selected_timestamp
            .tz_localize(TIMEZONE)
        )

    except Exception:

        print(
            "\nERROR: Invalid date format."
        )

        print(
            "Use format: YYYY-MM-DD HH:MM"
        )

        return

    # --------------------------------------------------------
    # Load buildings
    # --------------------------------------------------------

    try:

        buildings = load_buildings()

    except Exception as error:

        print(f"\nERROR: {error}")

        return

    # --------------------------------------------------------
    # Process buildings
    # --------------------------------------------------------

    all_results = []

    for building in buildings:

        try:

            result = calculate_solar_power(

                building,

                selected_timestamp
            )

            print_result(result)

            all_results.append(
                result
            )

        except Exception as error:

            print("\n")
            print("=" * 60)

            print(
                f"ERROR PROCESSING "
                f"{building['candidate_id']}"
            )

            print("=" * 60)

            print(error)

    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------

    if len(all_results) > 0:

        results_df = pd.DataFrame(
            all_results
        )

        results_df.to_csv(

            OUTPUT_FILE,

            index=False
        )

        print("\n")
        print("=" * 60)
        print("ALL BUILDINGS PROCESSED SUCCESSFULLY")
        print("=" * 60)

        print("\n")

        print(
            results_df[
                [
                    "candidate_id",

                    "latitude",

                    "longitude",

                    "building_height_m",

                    "ghi_w_m2",

                    "dni_w_m2",

                    "dhi_w_m2",

                    "poa_irradiance_w_m2",

                    "wind_speed_at_building_height",

                    "cell_temperature_c",

                    "panel_efficiency_percent",

                    "predicted_power_kw"
                ]
            ]
        )

        print(
            f"\nResults saved to: "
            f"{OUTPUT_FILE}"
        )

    else:

        print(
            "\nNo buildings were successfully processed."
        )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()
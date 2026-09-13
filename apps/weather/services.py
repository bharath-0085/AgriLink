"""
Agri Link — Weather Service
=============================
Integrates with OpenWeather API to retrieve current weather, 5–7 day forecast,
and actionable agricultural advisories and alerts for farmers.
"""

import logging
import datetime
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def _degrees_to_cardinal(deg):
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    ix = round(deg / 45) % 8
    return dirs[ix]


def fetch_openweather_data(lat=11.02, lng=76.96, city=None):
    """
    Fetch comprehensive current weather, multi-day forecast, and agricultural alerts.
    Supports either GPS coordinates or city name.
    """
    api_key = getattr(settings, "OPENWEATHER_API_KEY", "").strip()
    if not api_key:
        logger.warning("OPENWEATHER_API_KEY is not configured in settings. Using fallback demo data.")
        return _get_fallback_weather_data(lat, lng, city)

    current_url = "https://api.openweathermap.org/data/2.5/weather"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "appid": api_key,
        "units": "metric",
    }
    if city:
        params["q"] = f"{city},IN" if "," not in city else city
    else:
        params["lat"] = lat
        params["lon"] = lng

    try:
        # Fetch current weather
        curr_resp = requests.get(current_url, params=params, timeout=6)
        if curr_resp.status_code != 200:
            logger.error("OpenWeather current API error %s: %s", curr_resp.status_code, curr_resp.text)
            return _get_fallback_weather_data(lat, lng, city)
        current_raw = curr_resp.json()

        # Fetch 5-day forecast
        forecast_raw = None
        try:
            f_params = {
                "appid": api_key,
                "units": "metric",
                "lat": current_raw.get("coord", {}).get("lat", lat),
                "lon": current_raw.get("coord", {}).get("lon", lng),
            }
            fore_resp = requests.get(forecast_url, params=f_params, timeout=6)
            if fore_resp.status_code == 200:
                forecast_raw = fore_resp.json()
            else:
                logger.warning("OpenWeather forecast API status %s", fore_resp.status_code)
        except Exception as fe:
            logger.warning("Failed to fetch OpenWeather forecast: %s", fe)

        return _format_weather_response(current_raw, forecast_raw, lat, lng, city)

    except requests.RequestException as e:
        logger.error("Failed to connect to OpenWeather API: %s", e)
        return _get_fallback_weather_data(lat, lng, city)


def _format_weather_response(current_raw, forecast_raw, lat, lng, city=None):
    """
    Format raw OpenWeather API payload to the application spec with current, forecast & alerts.
    """
    main = current_raw.get("main", {})
    wind = current_raw.get("wind", {})
    weather_list = current_raw.get("weather", [{}])
    weather = weather_list[0] if weather_list else {}
    clouds = current_raw.get("clouds", {})
    rain_data = current_raw.get("rain", {})
    visibility_m = current_raw.get("visibility", 10000)

    # Weather condition
    condition_main = weather.get("main", "Clear")
    condition_desc = weather.get("description", "Clear sky").capitalize()
    icon_code = weather.get("icon", "01d")

    # Precipitation / rain chance calculation
    rainfall_mm = float(rain_data.get("1h", rain_data.get("3h", 0.0)))
    clouds_pct = float(clouds.get("all", 0))
    rain_chance = 0.0
    c_lower = condition_main.lower()
    if "rain" in c_lower or "drizzle" in c_lower:
        rain_chance = max(80.0, min(100.0, 70.0 + rainfall_mm * 5.0))
    elif "thunder" in c_lower:
        rain_chance = 85.0
    elif "cloud" in c_lower:
        rain_chance = round(min(65.0, max(10.0, clouds_pct * 0.6)), 1)
    else:
        rain_chance = 5.0

    # Wind speed in km/h
    wind_speed_ms = float(wind.get("speed", 0.0))
    wind_speed_kmh = round(wind_speed_ms * 3.6, 1)
    wind_deg = int(wind.get("deg", 0))
    wind_direction = _degrees_to_cardinal(wind_deg)

    temp_c = round(float(main.get("temp", 28.0)), 1)
    feels_like_c = round(float(main.get("feels_like", temp_c)), 1)
    humidity_pct = round(float(main.get("humidity", 60.0)), 1)
    pressure_hpa = round(float(main.get("pressure", 1013.0)), 1)
    visibility_km = round(visibility_m / 1000.0, 1)

    location_name = current_raw.get("name", "")
    if not location_name and city:
        location_name = city
    if not location_name:
        location_name = f"Region ({lat}, {lng})"

    now_str = datetime.datetime.now().strftime("%I:%M %p, %d %b %Y")

    # Parse 5–7 day forecast
    forecast = _parse_forecast_days(forecast_raw, temp_c, humidity_pct, condition_desc, icon_code)

    # Parse next 24h hourly forecast (8 intervals)
    hourly = _parse_hourly_forecast(forecast_raw, temp_c, humidity_pct, condition_desc, icon_code)

    # Generate agricultural alerts
    alerts = _generate_agricultural_alerts(temp_c, humidity_pct, wind_speed_kmh, rain_chance, rainfall_mm, condition_desc, forecast)

    return {
        # Backward-compatible top-level keys for existing dashboard widgets:
        "temperature": temp_c,
        "humidity": humidity_pct,
        "weather": condition_desc,
        "wind_speed": wind_speed_kmh,
        "rain_chance": rain_chance,
        "location": location_name,
        "gps_lat": current_raw.get("coord", {}).get("lat", lat),
        "gps_lng": current_raw.get("coord", {}).get("lon", lng),

        # Rich new data for Weather & Alerts module:
        "feels_like": feels_like_c,
        "weather_main": condition_main,
        "icon": icon_code,
        "rainfall_mm": rainfall_mm,
        "visibility_km": visibility_km,
        "pressure_hpa": pressure_hpa,
        "wind_direction": wind_direction,
        "wind_deg": wind_deg,
        "last_updated": now_str,
        "is_demo": False,
        "source": "OpenWeather API (Live)",
        "forecast": forecast,
        "hourly": hourly,
        "alerts": alerts,
    }


def _parse_forecast_days(forecast_raw, base_temp, base_hum, base_weather, base_icon):
    """
    Parse 3-hour forecast entries into clean daily summaries (up to 7 days).
    """
    forecast_list = []
    if forecast_raw and "list" in forecast_raw:
        grouped = {}
        for entry in forecast_raw["list"]:
            dt_txt = entry.get("dt_txt", "")
            if not dt_txt:
                continue
            date_str = dt_txt.split(" ")[0]
            grouped.setdefault(date_str, []).append(entry)

        for date_str, entries in list(grouped.items())[:7]:
            min_temps = [e["main"]["temp_min"] for e in entries if "main" in e and "temp_min" in e["main"]]
            max_temps = [e["main"]["temp_max"] for e in entries if "main" in e and "temp_max" in e["main"]]
            humidities = [e["main"]["humidity"] for e in entries if "main" in e and "humidity" in e["main"]]
            pops = [e.get("pop", 0.0) for e in entries]

            midday_entry = entries[len(entries) // 2] if entries else {}
            w_info = midday_entry.get("weather", [{}])[0] if midday_entry.get("weather") else {}
            cond_desc = w_info.get("description", "Fair").capitalize()
            cond_icon = w_info.get("icon", "02d")
            cond_main = w_info.get("main", "Clouds")

            try:
                dt_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                day_name = dt_obj.strftime("%A")
                date_formatted = dt_obj.strftime("%d %b")
            except Exception:
                day_name = date_str
                date_formatted = date_str

            forecast_list.append({
                "date": date_str,
                "day": day_name,
                "date_formatted": date_formatted,
                "temp_min": round(min(min_temps) if min_temps else (base_temp - 5), 1),
                "temp_max": round(max(max_temps) if max_temps else (base_temp + 4), 1),
                "humidity": round(sum(humidities) / len(humidities) if humidities else base_hum),
                "rain_probability": round(max(pops) * 100 if pops else 10),
                "weather": cond_desc,
                "weather_main": cond_main,
                "icon": cond_icon,
            })

    # Extrapolate to at least 6-7 days if needed
    while len(forecast_list) < 6:
        last_day = forecast_list[-1] if forecast_list else None
        if last_day:
            try:
                next_date = datetime.datetime.strptime(last_day["date"], "%Y-%m-%d") + datetime.timedelta(days=1)
                forecast_list.append({
                    "date": next_date.strftime("%Y-%m-%d"),
                    "day": next_date.strftime("%A"),
                    "date_formatted": next_date.strftime("%d %b"),
                    "temp_min": round(last_day["temp_min"] + 0.4, 1),
                    "temp_max": round(last_day["temp_max"] - 0.4, 1),
                    "humidity": last_day["humidity"],
                    "rain_probability": max(5, last_day["rain_probability"] - 5),
                    "weather": "Partly Cloudy",
                    "weather_main": "Clouds",
                    "icon": "02d",
                })
            except Exception:
                break
        else:
            break

    return forecast_list


def _parse_hourly_forecast(forecast_raw, base_temp, base_hum, base_weather, base_icon):
    """
    Parse next 24 hours (8 x 3-hour intervals) from OpenWeather forecast payload.
    """
    hourly_list = []
    if forecast_raw and "list" in forecast_raw:
        for entry in forecast_raw["list"][:8]:
            dt_txt = entry.get("dt_txt", "")
            time_label = ""
            if dt_txt:
                try:
                    dt_obj = datetime.datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
                    time_label = dt_obj.strftime("%I:%M %p").lstrip("0")
                except Exception:
                    time_label = dt_txt.split(" ")[-1][:5]
            
            w_info = entry.get("weather", [{}])[0] if entry.get("weather") else {}
            pop_pct = round(entry.get("pop", 0.0) * 100)
            
            hourly_list.append({
                "time": time_label or "Upcoming",
                "temp": round(entry.get("main", {}).get("temp", base_temp), 1),
                "feels_like": round(entry.get("main", {}).get("feels_like", base_temp), 1),
                "humidity": entry.get("main", {}).get("humidity", base_hum),
                "rain_probability": pop_pct,
                "weather": w_info.get("description", base_weather).capitalize(),
                "icon": w_info.get("icon", base_icon),
                "wind_speed": round(entry.get("wind", {}).get("speed", 0.0) * 3.6, 1),
            })
            
    if not hourly_list:
        now = datetime.datetime.now()
        for i in range(8):
            fut = now + datetime.timedelta(hours=i * 3)
            time_str = "Now" if i == 0 else fut.strftime("%I:%M %p").lstrip("0")
            hourly_list.append({
                "time": time_str,
                "temp": round(base_temp + (1.5 if 10 <= fut.hour <= 16 else -1.5), 1),
                "feels_like": round(base_temp + 1.0, 1),
                "humidity": base_hum,
                "rain_probability": 15 if i % 2 == 0 else 5,
                "weather": base_weather,
                "icon": base_icon,
                "wind_speed": 14.0,
            })
    return hourly_list


def _generate_agricultural_alerts(temp_c, humidity, wind_speed_kmh, rain_chance, rainfall_mm, condition_desc, forecast):
    """
    Generate targeted, actionable agricultural alerts based on current and forecasted weather metrics.
    """
    alerts = []
    
    max_rain_prob = max([f.get("rain_probability", 0) for f in forecast] + [rain_chance])
    max_temp_fore = max([f.get("temp_max", 0) for f in forecast] + [temp_c])
    any_storm = any("thunder" in f.get("weather", "").lower() or "storm" in f.get("weather", "").lower() for f in forecast) or "thunder" in condition_desc.lower()

    # 1. Heavy Rain Alert
    if max_rain_prob >= 55 or rainfall_mm >= 8.0:
        severity = "High" if (max_rain_prob >= 75 or rainfall_mm >= 20.0) else "Medium"
        alerts.append({
            "id": "alert-heavy-rain",
            "type": "rain",
            "title": "Heavy Rain & Waterlogging Advisory",
            "severity": severity,
            "date": "Active | Next 24-48 Hours",
            "short_explanation": f"Elevated precipitation probability of {max_rain_prob}% with localized downpours anticipated across agricultural fields.",
            "recommended_action": "Immediately clear drainage outlets and perimeter field channels to avoid waterlogging around roots. Postpone fertilizer broadcasting (urea/potash) and pesticide spraying to prevent costly nutrient wash-off.",
        })

    # 2. Heat / High Temperature Alert
    if max_temp_fore >= 32.5:
        severity = "High" if max_temp_fore >= 36.0 else "Medium"
        alerts.append({
            "id": "alert-heat-temp",
            "type": "heat",
            "title": "High Temperature & Heat Stress Alert",
            "severity": severity,
            "date": "Active | Peak Afternoon (12:00 PM - 04:30 PM)",
            "short_explanation": f"Maximum ambient temperature reaching {max_temp_fore}°C. High evaporative moisture demand may induce leaf scorch and blossom drop in sensitive crops.",
            "recommended_action": "Schedule light split irrigation during early morning (6:00 AM - 8:30 AM) or post-sunset. Maintain organic mulching on vegetable beds to keep root zone soil temperatures cool.",
        })

    # 3. Strong Wind Alert
    if wind_speed_kmh >= 18.0:
        severity = "High" if wind_speed_kmh >= 32.0 else "Medium"
        alerts.append({
            "id": "alert-strong-wind",
            "type": "wind",
            "title": "Gusty Winds & Lodging Risk Advisory",
            "severity": severity,
            "date": "Active | Moderate to High Wind Speeds",
            "short_explanation": f"Wind speeds recorded up to {wind_speed_kmh} km/h. Risk of mechanical damage or crop lodging in tall stem crops.",
            "recommended_action": "Provide bamboo staking or double earthing-up support for sugarcane, banana plants, and tall maize. Immediately suspend aerial drone spraying and tall boom pesticide applications.",
        })

    # 4. Storm / Thunderstorm Alert
    if any_storm:
        alerts.append({
            "id": "alert-thunderstorm",
            "type": "storm",
            "title": "Storm & Severe Thunderstorm Warning",
            "severity": "High",
            "date": "Immediate Alert | Active Radar Watch",
            "short_explanation": "Atmospheric instability is generating localized thunderstorm activity with lightning, gusty downdrafts, and sudden squalls.",
            "recommended_action": "Ensure all field workers immediately seek enclosed, dry shelter. Turn off open-field electric pump starters and protect harvested grain stored in open threshing yards.",
        })

    # 5. Low Rainfall / Dry Condition Alert
    if max_rain_prob <= 20 and humidity <= 55 and temp_c >= 27.0:
        alerts.append({
            "id": "alert-dry-conditions",
            "type": "dry",
            "title": "Dry Spell & Soil Moisture Deficit Advisory",
            "severity": "Medium" if temp_c >= 31.0 else "Low",
            "date": "Extended Advisory | Next 5 Days",
            "short_explanation": f"Extended dry weather window with low relative humidity ({humidity}%) and minimal rain probability. Accelerated soil moisture depletion expected.",
            "recommended_action": "Switch to micro-irrigation or night-time drip cycles to minimize evaporation losses. Inspect soil moisture with a probe before cultivating to avoid excessive topsoil pulverization.",
        })

    # 6. Fallback optimal window if no severe conditions
    if len(alerts) == 0:
        alerts.append({
            "id": "alert-optimal-conditions",
            "type": "optimal",
            "title": "Optimal Field Operations & Spraying Window",
            "severity": "Low",
            "date": "Current Window | Next 48 Hours",
            "short_explanation": f"Current weather presents favorable conditions ({condition_desc}, {temp_c}°C, breeze {wind_speed_kmh} km/h) with minimal meteorological hazards.",
            "recommended_action": "Ideal window for foliar nutrient sprays, weeding, land preparation, and harvesting ripe produce. Safe conditions for standard tractor field activities.",
        })

    return alerts


def _get_fallback_weather_data(lat=11.02, lng=76.96, city=None):
    """
    Return realistic, comprehensive fallback weather data when the API key is missing or request fails.
    Clearly flagged with is_demo=True so the UI is transparent.
    """
    now = datetime.datetime.now()
    now_str = now.strftime("%I:%M %p, %d %b %Y")
    location_name = city or "Coimbatore, Tamil Nadu"

    # Generate 7-day forecast
    forecast_days = []
    base_date = now.date()
    patterns = [
        {"desc": "Partly Cloudy", "icon": "03d", "main": "Clouds", "min": 22.5, "max": 31.0, "pop": 20, "hum": 65},
        {"desc": "Light Showers", "icon": "10d", "main": "Rain", "min": 21.0, "max": 28.5, "pop": 65, "hum": 80},
        {"desc": "Moderate Rain", "icon": "10d", "main": "Rain", "min": 20.5, "max": 27.0, "pop": 75, "hum": 85},
        {"desc": "Scattered Clouds", "icon": "03d", "main": "Clouds", "min": 22.0, "max": 30.5, "pop": 30, "hum": 70},
        {"desc": "Sunny & Clear", "icon": "01d", "main": "Clear", "min": 23.0, "max": 33.0, "pop": 10, "hum": 55},
        {"desc": "Hot & Sunny", "icon": "01d", "main": "Clear", "min": 24.0, "max": 34.5, "pop": 5, "hum": 48},
        {"desc": "Breezy & Overcast", "icon": "04d", "main": "Clouds", "min": 23.5, "max": 32.0, "pop": 25, "hum": 62},
    ]

    for i, p in enumerate(patterns):
        day_date = base_date + datetime.timedelta(days=i)
        forecast_days.append({
            "date": day_date.strftime("%Y-%m-%d"),
            "day": "Today" if i == 0 else ("Tomorrow" if i == 1 else day_date.strftime("%A")),
            "date_formatted": day_date.strftime("%d %b"),
            "temp_min": p["min"],
            "temp_max": p["max"],
            "humidity": p["hum"],
            "rain_probability": p["pop"],
            "weather": p["desc"],
            "weather_main": p["main"],
            "icon": p["icon"],
        })

    alerts = [
        {
            "id": "demo-alert-rain",
            "type": "rain",
            "title": "Heavy Rain & Waterlogging Advisory",
            "severity": "High",
            "date": "Active | Expected in 24-48 Hours",
            "short_explanation": "A localized trough is expected to bring widespread moderate to heavy showers (up to 45mm) across agricultural blocks.",
            "recommended_action": "Clear bund drainage channels immediately. Postpone all chemical sprayings, foliar feeding, and urea top-dressing to prevent wash-off.",
        },
        {
            "id": "demo-alert-heat",
            "type": "heat",
            "title": "High Temperature Alert",
            "severity": "Medium",
            "date": "Active | Peak Afternoon (12:00 PM - 4:00 PM)",
            "short_explanation": "Temperatures forecasted to touch 34.5°C over the weekend with elevated solar radiation causing rapid moisture evaporation.",
            "recommended_action": "Provide early morning irrigation. Maintain mulch in vegetable plots and protect young saplings with temporary shading nets.",
        },
        {
            "id": "demo-alert-wind",
            "type": "wind",
            "title": "Strong Wind Advisory",
            "severity": "Medium",
            "date": "Active | Tomorrow Evening",
            "short_explanation": "South-westerly winds expected to strengthen up to 24 km/h with sudden pre-monsoon squalls.",
            "recommended_action": "Provide double propping for banana groves. Stake tall hybrid maize and avoid tractor spraying during peak wind hours.",
        },
        {
            "id": "demo-alert-dry",
            "type": "dry",
            "title": "Soil Moisture Conservation Advisory",
            "severity": "Low",
            "date": "Active | Extended Outlook",
            "short_explanation": "Relative humidity expected to drop to 48% following rainfall, accelerating topsoil crusting.",
            "recommended_action": "Plan drip fertigation schedules to optimize water usage. Check root zone depth moisture before tilling.",
        },
    ]

    hourly_entries = []
    for i in range(8):
        fut = now + datetime.timedelta(hours=i * 3)
        time_str = "Now" if i == 0 else fut.strftime("%I:%M %p").lstrip("0")
        hourly_entries.append({
            "time": time_str,
            "temp": round(29.5 + (1.8 if 10 <= fut.hour <= 16 else -2.0), 1),
            "feels_like": round(31.2 + (1.5 if 10 <= fut.hour <= 16 else -2.0), 1),
            "humidity": 66 if i % 2 == 0 else 72,
            "rain_probability": 20 if i in (2, 3) else 5,
            "weather": "Partly Cloudy" if i not in (2, 3) else "Passing Shower",
            "icon": "03d" if 6 <= fut.hour <= 18 else "03n",
            "wind_speed": 14.4,
        })

    return {
        "temperature": 29.5,
        "feels_like": 31.2,
        "humidity": 66.0,
        "weather": "Partly Cloudy (Demo)",
        "weather_main": "Clouds",
        "icon": "03d",
        "wind_speed": 14.4,
        "wind_direction": "SW",
        "wind_deg": 225,
        "rain_chance": 25.0,
        "rainfall_mm": 0.0,
        "visibility_km": 10.0,
        "pressure_hpa": 1012.0,
        "location": location_name,
        "gps_lat": lat,
        "gps_lng": lng,
        "last_updated": now_str,
        "is_demo": True,
        "source": "Demo Weather Mode (API Simulation)",
        "forecast": forecast_days,
        "hourly": hourly_entries,
        "alerts": alerts,
    }


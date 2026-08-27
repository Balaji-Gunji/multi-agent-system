import requests


def get_weather(city):
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1, "format": "json"},
        timeout=10
    )
    geo.raise_for_status()

    results = geo.json().get("results", [])
    if not results:
        raise ValueError(f"Location not found: {city}")

    location = results[0]

    weather = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": "temperature_2m,wind_speed_10m",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "forecast_days": 3,
            "timezone": "auto"
        },
        timeout=10
    )
    weather.raise_for_status()

    data = weather.json()
    daily = data["daily"]

    forecast = []
    for i, date in enumerate(daily["time"]):
        forecast.append({
            "date": date,
            "max": daily["temperature_2m_max"][i],
            "min": daily["temperature_2m_min"][i],
            "rain": daily["precipitation_probability_max"][i]
        })

    return {
        "current": data.get("current", {}),
        "forecast": forecast
    }

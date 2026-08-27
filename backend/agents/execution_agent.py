from services.weather_service import get_weather


def run(task, plan):
    city = "Hyderabad" if "hyderabad" in task.lower() else "Hyderabad"

    try:
        weather = get_weather(city)
        return {
            "agent": "Execution Agent",
            "status": "completed",
            "api": "Open-Meteo",
            "location": city,
            **weather
        }
    except Exception as exc:
        return {
            "agent": "Execution Agent",
            "status": "partial",
            "api": "Open-Meteo",
            "location": city,
            "error": str(exc),
            "current": {},
            "forecast": []
        }

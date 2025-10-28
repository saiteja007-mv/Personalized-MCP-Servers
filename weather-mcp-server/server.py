import requests
import logging
from fastmcp import FastMCP

# Logging setup (stderr)
logging.basicConfig(level=logging.INFO)

app = FastMCP("weather-mcp", "Provides real-time and forecast weather updates using Open-Meteo API.")

# --- Helper Function ---
def get_lat_lon(city):
    """Fetch latitude and longitude for a city"""
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        response = requests.get(geo_url, timeout=10)
        data = response.json()

        if "results" not in data or len(data["results"]) == 0:
            return None, None

        first = data["results"][0]
        return first["latitude"], first["longitude"]
    except Exception as e:
        logging.error(f"Error fetching coordinates: {e}")
        return None, None


# --- Tools ---

@app.tool()
def get_weather_by_city(city: str = ""):
    """Get current weather by city name"""
    try:
        if city == "":
            return "Please provide a city name."

        lat, lon = get_lat_lon(city)
        if not lat or not lon:
            return f"Could not find coordinates for {city}."

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&timezone=auto"
        res = requests.get(weather_url, timeout=10).json()

        if "current_weather" not in res:
            return f"No weather data found for {city}."

        w = res["current_weather"]
        return (
            f"🌍 Weather in {city}:\n"
            f"Temperature: {w['temperature']}°C\n"
            f"Windspeed: {w['windspeed']} km/h\n"
            f"Condition Code: {w['weathercode']}\n"
            f"Time: {w['time']}"
        )
    except Exception as e:
        logging.error(f"Error in get_weather_by_city: {e}")
        return "Error retrieving weather data."


@app.tool()
def get_weather_by_coordinates(lat: str = "", lon: str = ""):
    """Get detailed weather report by coordinates"""
    try:
        if lat == "" or lon == "":
            return "Please provide both latitude and longitude."

        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current_weather=true&hourly=temperature_2m,relative_humidity_2m,precipitation"
            f"&timezone=auto"
        )
        res = requests.get(url, timeout=10).json()

        if "current_weather" not in res:
            return "No weather data found for these coordinates."

        cw = res["current_weather"]
        return (
            f"📍 Coordinates: ({lat}, {lon})\n"
            f"Temperature: {cw['temperature']}°C\n"
            f"Windspeed: {cw['windspeed']} km/h\n"
            f"Weather Code: {cw['weathercode']}\n"
            f"Time: {cw['time']}"
        )
    except Exception as e:
        logging.error(f"Error in get_weather_by_coordinates: {e}")
        return "Error retrieving weather data."


@app.tool()
def get_forecast(city: str = ""):
    """Get 5-day weather forecast by city"""
    try:
        if city == "":
            return "Please provide a city name."

        lat, lon = get_lat_lon(city)
        if not lat or not lon:
            return f"Could not find coordinates for {city}."

        forecast_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
            f"&forecast_days=5&timezone=auto"
        )

        res = requests.get(forecast_url, timeout=10).json()
        if "daily" not in res:
            return f"No forecast data found for {city}."

        daily = res["daily"]
        output = [f"🌤️ 5-Day Forecast for {city}:"]
        for i in range(len(daily["time"])):
            output.append(
                f"{daily['time'][i]}: "
                f"Max {daily['temperature_2m_max'][i]}°C, "
                f"Min {daily['temperature_2m_min'][i]}°C, "
                f"Precip {daily['precipitation_sum'][i]}mm"
            )

        return "\n".join(output)
    except Exception as e:
        logging.error(f"Error in get_forecast: {e}")
        return "Error retrieving forecast data."

if __name__ == "__main__":
    app.run()

import requests

def get_coordinates(city_name):
    """
    Get the latitude, longitude, and formatted name for a city
    using the Open-Meteo Geocoding API.
    """
    url = f"https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an exception for bad status codes
    
    data = response.json()
    
    if "results" not in data or not data["results"]:
        return None
        
    result = data["results"][0]
    return {
        "name": result.get("name", ""),
        "country": result.get("country", ""),
        "latitude": result.get("latitude", 0.0),
        "longitude": result.get("longitude", 0.0)
    }

def get_current_weather(latitude, longitude):
    """
    Get current weather information for given coordinates
    using the Open-Meteo Weather API.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "wind_speed_10m", "weather_code"]
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    if "current" not in data:
        return None
        
    return data["current"]

# Problem Statement

Checking current weather for a particular city requires finding the location represented by that city and obtaining weather information for its geographic coordinates. This can be inconvenient when a user wants a quick, readable summary without navigating multiple websites or interpreting raw API data. The Python Weather App addresses this need through a command-line workflow: a user enters a city name, and the application displays the available current weather conditions for the matching location. It brings city lookup, weather retrieval, and readable presentation together in one lightweight tool.

# Project Scope

The project is a Python command-line application for looking up current weather by city. It uses the Open-Meteo Geocoding API to search for a city (requesting one English-language result), then uses the Open-Meteo Forecast API with the returned coordinates to obtain current temperature, apparent temperature, relative humidity, wind speed, weather code, and time. The application displays the location name and country with these values; weather codes are converted into descriptive condition labels using a local mapping.

Users can repeat a search or exit from the interactive menu. The application rejects an empty city name and handles missing city results, unavailable weather data, and common request or response errors. It requires an internet connection and the `requests` Python package. It does not include a database, save search history or favorite locations, provide forecasts, or offer a graphical interface; weather data is obtained from the external Open-Meteo services.

# Target Users

- Individuals who want a quick current-weather summary for a city from a terminal.
- Python learners interested in a small example of modular code, HTTP requests, JSON response handling, and exception handling.

# High-Level Features

- **Interactive city search:** Prompts for a city name, rejects blank input, and lets the user search again or exit.
- **City geocoding:** Looks up the entered name through Open-Meteo and obtains the first matching location's name, country, latitude, and longitude.
- **Current weather retrieval:** Requests current temperature, feels-like temperature, humidity, wind speed, weather code, and time for the selected coordinates.
- **Condition interpretation and display:** Maps WMO weather codes to readable descriptions and presents the results with the matched location.
- **Error handling:** Reports unsuccessful city or weather lookups and handles connection, timeout, HTTP, invalid JSON, and keyboard-interruption cases.
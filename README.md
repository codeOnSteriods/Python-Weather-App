# Python Weather App

A simple, beginner-friendly command-line weather application built with Python. 

## Description
This application allows users to enter a city name and retrieve current weather information. It uses the free Open-Meteo API to convert city names to coordinates (geocoding) and fetch current weather conditions. 

## Features
- Search for any city worldwide
- Retrieve real-time weather data:
  - Temperature (°C)
  - Feels like temperature (°C)
  - Relative Humidity (%)
  - Wind Speed (km/h)
  - Weather Condition (e.g., Clear sky, Rain)
  - Current local time at the location
- Interactive command-line interface
- Error handling for network issues and invalid inputs

## Technologies Used
- Python 3
- `requests` library
- Open-Meteo Geocoding API
- Open-Meteo Forecast API

## Python Concepts Demonstrated
- Variables, Strings, and Numbers
- Lists and Dictionaries
- Conditional Statements (if-else)
- Loops (while)
- Functions and Modular Programming
- Exception Handling (try-except)
- HTTP Requests and JSON Parsing

## Project Structure
```text
weather-app/
│
├── main.py          # Main application loop and user interface
├── weather.py       # API interaction for geocoding and weather data
├── utils.py         # Helper functions (weather code conversions)
├── requirements.txt # Project dependencies
├── README.md        # Project documentation
└── .gitignore       # Git ignore rules
```

## Installation

1. Ensure you have Python 3 installed on your system.
2. Clone or download this project.
3. Open a terminal and navigate to the project directory:
   ```bash
   cd weather-app
   ```
4. Create and activate a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

Run the main application file using Python:
```bash
python3 main.py
```

## Example Output

```text
========================================
PYTHON WEATHER APP
==================

Enter city name: Bhopal

Searching for 'Bhopal'...
## Location: Bhopal, India

Temperature     : 27.4 °C
Feels Like      : 29.1 °C
Humidity        : 72 %
Wind Speed      : 8.4 km/h
Condition       : Partly cloudy
Time            : 10:30
-----------------------

1. Search another city
2. Exit

Enter choice: 
```

## API Information
This project relies on the public [Open-Meteo APIs](https://open-meteo.com/):
- No API key is required.
- **Geocoding API**: Used to get latitude and longitude for a given city name.
- **Forecast API**: Used to fetch the current weather using coordinates.

## Future Improvements
- Add a 7-day forecast feature.
- Support saving favorite cities to a file.
- Add an option to switch between Celsius and Fahrenheit.

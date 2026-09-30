import sys
import requests
from weather import get_coordinates, get_current_weather
from utils import get_weather_description

def display_header():
    print("\n" + "="*40)
    print("PYTHON WEATHER APP")
    print("="*18 + "\n")

def display_weather(location_data, weather_data):
    city = location_data['name']
    country = location_data['country']
    
    temp = weather_data.get('temperature_2m', 'N/A')
    feels_like = weather_data.get('apparent_temperature', 'N/A')
    humidity = weather_data.get('relative_humidity_2m', 'N/A')
    wind_speed = weather_data.get('wind_speed_10m', 'N/A')
    weather_code = weather_data.get('weather_code', -1)
    condition = get_weather_description(weather_code)
    
    time_str = weather_data.get('time', 'N/A')
    # Time is in ISO format like 2023-10-25T10:00, extract just time if possible
    if time_str != 'N/A' and 'T' in time_str:
        time_str = time_str.split('T')[1]
        
    print(f"## Location: {city}, {country}\n")
    print(f"Temperature     : {temp} °C")
    print(f"Feels Like      : {feels_like} °C")
    print(f"Humidity        : {humidity} %")
    print(f"Wind Speed      : {wind_speed} km/h")
    print(f"Condition       : {condition}")
    print(f"Time            : {time_str}")
    print("-" * 23 + "\n")

def run():
    while True:
        display_header()
        city_name = input("Enter city name: ").strip()
        
        if not city_name:
            print("Error: City name cannot be empty. Please try again.")
            continue
            
        try:
            print(f"\nSearching for '{city_name}'...")
            location = get_coordinates(city_name)
            
            if not location:
                print(f"Error: Could not find city '{city_name}'.")
            else:
                weather = get_current_weather(location['latitude'], location['longitude'])
                if not weather:
                    print("Error: Could not retrieve weather data for this location.")
                else:
                    display_weather(location, weather)
                    
        except requests.exceptions.ConnectionError:
            print("Error: Network connection failed. Please check your internet.")
        except requests.exceptions.Timeout:
            print("Error: The request timed out. Please try again later.")
        except requests.exceptions.HTTPError as e:
            print(f"Error: API returned an invalid response. ({e})")
        except ValueError:
            print("Error: Received invalid JSON format from the API.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
        print("1. Search another city")
        print("2. Exit\n")
        
        choice = input("Enter choice: ").strip()
        if choice == '2':
            print("Thank you for using the Python Weather App. Goodbye!")
            break
        elif choice != '1':
            print("Invalid choice, starting a new search by default.")

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
        sys.exit(0)

# Design Diagrams

These diagrams describe the implemented Python command-line application. Its only interactive actor is a terminal user. The application has no browser frontend, application server, authentication, or persistent storage; weather information comes from the external Open-Meteo APIs.

## 1. System Architecture Diagram

```mermaid
flowchart LR
    User["Terminal user"]

    subgraph App["Python Weather App"]
        CLI["main.py<br/>CLI, workflow, display"]
        Weather["weather.py<br/>Geocoding and current-weather requests"]
        Utils["utils.py<br/>WMO code descriptions"]
        Requests["requests 2.31.0<br/>HTTP client"]

        CLI -->|"get_coordinates(city)"| Weather
        Weather -->|"location or no match"| CLI
        CLI -->|"weather code"| Utils
        Utils -->|"condition description"| CLI
        Weather -->|"HTTP requests / JSON parsing"| Requests
        CLI -.->|"imports request exception types"| Requests
    end

    Geocoding["Open-Meteo Geocoding API"]
    Forecast["Open-Meteo Forecast API"]

    Requests <-->|"HTTPS search request / JSON response"| Geocoding
    Requests <-->|"HTTPS coordinates + current fields / JSON response"| Forecast
    User <-->|"city and menu input / summary and messages"| CLI
```

## 2. Workflow / Process Flow Diagram

```mermaid
flowchart TD
    Start([Start application]) --> Header["Display header and prompt for city"]
    Header --> Input["Read input and trim whitespace"]
    Input --> Empty{"City name empty?"}
    Empty -->|"Yes"| Blank["Print empty-name error"]
    Blank --> Header
    Empty -->|"No"| Search["main.py calls get_coordinates(city)"]
    Search --> Geo["weather.py requests city search<br/>count=1, language=en"]
    Geo <-->|"HTTPS / JSON"| GeoAPI["Open-Meteo Geocoding API"]
    Geo --> GeoFound{"Matching result returned?"}
    GeoFound -->|"No"| NotFound["Print city-not-found message"]
    GeoFound -->|"Yes: first result"| Current["Call get_current_weather(latitude, longitude)"]
    Current --> Forecast["weather.py requests current weather fields"]
    Forecast <-->|"HTTPS / JSON"| ForecastAPI["Open-Meteo Forecast API"]
    Forecast --> HasCurrent{"Current data present?"}
    HasCurrent -->|"No"| Unavailable["Print weather-unavailable message"]
    HasCurrent -->|"Yes"| MapCode["Map WMO weather_code in utils.py"]
    MapCode --> Display["Display location, measurements, condition, and time"]

    Geo -->|"Network, timeout, HTTP, JSON, or other exception"| Error["main.py catches and displays error"]
    Forecast -->|"Network, timeout, HTTP, JSON, or other exception"| Error

    NotFound --> Menu["Show search-again / exit menu"]
    Unavailable --> Menu
    Display --> Menu
    Error --> Menu
    Menu --> ExitChoice{"Choice is 2?"}
    ExitChoice -->|"Yes"| End([Print goodbye and exit])
    ExitChoice -->|"No"| SearchChoice{"Choice is 1?"}
    SearchChoice -->|"Yes"| Header
    SearchChoice -->|"No: invalid choice"| Default["Print invalid-choice message;<br/>start another search by default"]
    Default --> Header
```

Pressing Ctrl+C is also handled by the entry point, which prints an interruption message and exits. No database operations occur; the city and weather responses are used in memory for the current search only.

## 3. Use Case Diagram

```mermaid
flowchart LR
    User["Terminal user"]
    GeoAPI["Open-Meteo Geocoding API<br/>(supporting external system)"]
    ForecastAPI["Open-Meteo Forecast API<br/>(supporting external system)"]

    subgraph System["Python Weather App"]
        Search(["Search current weather by city"])
        View(["View weather summary or lookup message"])
        Repeat(["Search another city"])
        Exit(["Exit application"])
    end

    User --- Search
    User --- View
    User --- Repeat
    User --- Exit
    GeoAPI --- Search
    ForecastAPI --- Search
```

The terminal user is the only human actor supported by the code. The two APIs are secondary external systems involved in the search use case; there are no separate user roles or authentication flows.

## 4. Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant CLI as main.py
    participant Weather as weather.py
    participant Geo as Open-Meteo Geocoding API
    participant Forecast as Open-Meteo Forecast API
    participant Utils as utils.py

    loop Until the user exits
        CLI-->>User: Prompt for city name
        User->>CLI: Enter city
        CLI->>CLI: Trim whitespace and validate
        alt City is blank
            CLI-->>User: Print validation error and prompt again
        else City is non-empty
            CLI->>Weather: get_coordinates(city)
            Weather->>Geo: GET /v1/search (name, count=1, language=en, format=json)
            alt Geocoding request or JSON parsing raises an exception
                Geo-->>Weather: Request/response failure
                Weather-->>CLI: Exception propagates
                CLI-->>User: Catch and display the applicable error
            else Geocoding returns JSON
                Geo-->>Weather: JSON results
                Weather->>Weather: Select first result, or return None
                alt No matching result
                    Weather-->>CLI: None
                    CLI-->>User: Display city-not-found message
                else Location found
                    Weather-->>CLI: Name, country, latitude, longitude
                    CLI->>Weather: get_current_weather(latitude, longitude)
                    Weather->>Forecast: GET /v1/forecast (coordinates and current fields)
                    alt Forecast request or JSON parsing raises an exception
                        Forecast-->>Weather: Request/response failure
                        Weather-->>CLI: Exception propagates
                        CLI-->>User: Catch and display the applicable error
                    else Forecast returns JSON
                        Forecast-->>Weather: JSON current data
                        Weather->>Weather: Return current data, or None if absent
                        alt Current data absent
                            Weather-->>CLI: None
                            CLI-->>User: Display weather-unavailable message
                        else Current data present
                            Weather-->>CLI: Measurements, weather_code, and time
                            CLI->>Utils: get_weather_description(weather_code)
                            Utils-->>CLI: Condition description
                            CLI-->>User: Display location and current-weather summary
                        end
                    end
                end
            end
            CLI-->>User: Show search-again / exit menu
            User->>CLI: Enter menu choice
            alt Choice is 2
                CLI-->>User: Print goodbye and exit
            else Choice is 1 or another value
                CLI-->>User: Search again (invalid values default to a new search)
            end
        end
    end
```

## 5. Component Diagram

The code is organized as procedural Python modules rather than classes, so a component diagram best represents its structure and responsibilities.

```mermaid
flowchart LR
    subgraph App["Python Weather App"]
        Main["main.py<br/>Entry point; prompts, validation,<br/>workflow, output, exception handling"]
        Weather["weather.py<br/>get_coordinates()<br/>get_current_weather()"]
        Utils["utils.py<br/>get_weather_description()"]
        Requests["requests 2.31.0"]

        Main -->|"imports and calls"| Weather
        Main -->|"imports and calls"| Utils
        Main -.->|"catches requests exceptions"| Requests
        Weather -->|"HTTP GET and JSON response handling"| Requests
    end

    Geo["Open-Meteo Geocoding API"]
    Forecast["Open-Meteo Forecast API"]
    Requests -->|"city query"| Geo
    Requests -->|"coordinates and current fields"| Forecast
    Geo -->|"location result"| Weather
    Forecast -->|"current data"| Weather
```

## 6. ER Diagram

An ER diagram is not applicable. The implementation has no relational database or persistent structured storage. API response data is held in transient Python dictionaries during a search; no entities, primary keys, foreign keys, or stored relationships are defined.
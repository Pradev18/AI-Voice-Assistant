import requests
from Jarvis.config import config

def fetch_weather(city):
    """
    Fetches weather details for the given city using the OpenWeather API.
    :param city: Name of the city to get the weather for.
    :return: Formatted weather report or error message.
    """
    # Retrieve the API key from the config
    api_key = config.weather_api_key
    units_format = "&units=metric"  # Celsius for temperature
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    # Construct the complete URL with city and API key
    complete_url = f"{base_url}?q={city}&appid={api_key}{units_format}"

    try:
        # Make a GET request to fetch weather data
        response = requests.get(complete_url)

        # Raise an exception if the request was not successful
        response.raise_for_status()

        # Parse the JSON data from the response
        city_weather_data = response.json()

        # Check if the city was found (cod = 200 means city is found)
        if city_weather_data["cod"] == 200:
            main_data = city_weather_data["main"]
            weather_description_data = city_weather_data["weather"][0]
            weather_description = weather_description_data["description"]
            current_temperature = main_data["temp"]
            current_pressure = main_data["pressure"]
            current_humidity = main_data["humidity"]
            wind_data = city_weather_data["wind"]
            wind_speed = wind_data["speed"]

            # Format the final weather report
            final_response = f"""
            The weather in {city} is currently {weather_description}.
            Temperature: {current_temperature}°C
            Atmospheric pressure: {current_pressure} hPa
            Humidity: {current_humidity}%
            Wind Speed: {wind_speed} km/h
            """

            return final_response
        else:
            return "Sorry, I couldn't find the city in my database. Please try again."

    except requests.exceptions.RequestException as e:
        # Handle any network-related errors
        return f"An error occurred while fetching the weather data: {str(e)}"

# data_ingestion/climate.py

import requests
import os

def get_climate_data(city="New York"):
    api_key = os.getenv("OPENWEATHERMAP_API_KEY", "YOUR_OPENWEATHERMAP_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "weather": data["weather"][0]["description"]
        }
    else:
        raise Exception("Failed to fetch climate data")

# data_ingestion/satellite.py

import requests
from io import BytesIO
from PIL import Image
import os

def get_satellite_image(lat, lon, zoom=10):
    # Replace with your actual satellite API endpoint and key.
    api_key = os.getenv("SATELLITE_API_KEY", "YOUR_SATELLITE_API_KEY")
    # For demonstration, we use a placeholder URL.
    url = f"https://services.sentinel-hub.com/ogc/wms/8d9a8c0b-2ea3-4f52-a256-1a2715ab6170"
    
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        return img
    else:
        raise Exception(f"Failed to retrieve satellite image, status code {response.status_code}")

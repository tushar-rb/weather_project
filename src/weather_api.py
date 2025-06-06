import requests
from dotenv import load_dotenv
import os

load_dotenv()

def get_weather(city):
    """Get current weather data for a city"""
    api_key = os.getenv('API_KEY')
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for errors
        data = response.json()
        
        # Simplify the data for beginners
        return {
            'city': data['location']['name'],
            'country': data['location']['country'],
            'temperature_c': data['current']['temp_c'],
            'wind_kph': data['current']['wind_kph'],
            'wind_direction': data['current']['wind_dir'],
            'humidity': data['current']['humidity'],
            'condition': data['current']['condition']['text'],
            'last_updated': data['current']['last_updated']
        }
    except Exception as e:
        print(f"Error getting weather: {e}")
        return None
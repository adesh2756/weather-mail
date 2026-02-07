"""Weather fetching and analytics - combined for speed"""
import os
import requests
from datetime import datetime
from typing import Dict, List, Tuple

LOCATIONS = [
    {"name": "Houston, TX", "lat": 29.76, "lon": -95.36},
    {"name": "Hyderabad, Telangana", "lat": 17.38, "lon": 78.48},
    {"name": "Srikalahasthi, AP", "lat": 13.75, "lon": 79.70},
]

def fetch_weather(lat: float, lon: float, api_key: str) -> Dict:
    """Fetch weather from OpenWeather API"""
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def calculate_comfort_score(temp: float, humidity: int, wind_speed: float) -> int:
    """Calculate comfort score 0-10"""
    # Temperature score (optimal: 20-26°C)
    if 20 <= temp <= 26:
        temp_score = 10
    elif 15 <= temp <= 30:
        temp_score = 7
    else:
        temp_score = max(0, 10 - abs(temp - 23) / 2)
    
    # Humidity score (optimal: 40-60%)
    if 40 <= humidity <= 60:
        humidity_score = 10
    else:
        humidity_score = max(0, 10 - abs(humidity - 50) / 5)
    
    # Wind score (optimal: <15 km/h)
    wind_kmh = wind_speed * 3.6
    wind_score = max(0, 10 - wind_kmh / 3) if wind_kmh > 15 else 10
    
    return round((temp_score + humidity_score + wind_score) / 3)

def get_weather_emoji(weather_main: str, temp: float) -> str:
    """Get emoji based on weather condition"""
    emoji_map = {
        "Clear": "☀️",
        "Clouds": "🌤️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Mist": "🌫️",
        "Haze": "🌫️",
    }
    emoji = emoji_map.get(weather_main, "🌡️")
    
    # Add temperature emoji
    if temp > 35:
        emoji = "🔥" + emoji
    elif temp < 10:
        emoji = "🥶" + emoji
    
    return emoji

def get_weather_personality(name: str, temp: float, humidity: int) -> str:
    """Generate weather personality"""
    if humidity > 70:
        return f"Humid {name.split(',')[0]}"
    elif temp > 30:
        return f"Hot {name.split(',')[0]}"
    elif 20 <= temp <= 28:
        return f"Pleasant {name.split(',')[0]}"
    elif temp < 15:
        return f"Cool {name.split(',')[0]}"
    else:
        return f"Breezy {name.split(',')[0]}"

def generate_insight(weather_data: Dict, name: str) -> str:
    """Generate one insightful fact"""
    temp = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    weather_main = weather_data['weather'][0]['main']
    
    insights = []
    
    if weather_main in ['Rain', 'Drizzle', 'Thunderstorm']:
        insights.append(f"Rain expected - carry umbrella")
    elif humidity < 30:
        insights.append(f"Low humidity - stay hydrated")
    elif humidity > 75:
        insights.append(f"High humidity - feels muggy")
    
    if 20 <= temp <= 26:
        insights.append(f"Perfect weather for outdoor activities")
    elif temp > 35:
        insights.append(f"Very hot - limit sun exposure")
    elif temp < 15:
        insights.append(f"Cool weather - dress warmly")
    
    if 'Srikalahasthi' in name and temp < 28:
        insights.append(f"Ideal temple visit weather")
    
    return insights[0] if insights else "Typical weather for the region"

def get_all_weather_data(api_key: str) -> List[Dict]:
    """Fetch and analyze weather for all locations"""
    results = []
    
    for loc in LOCATIONS:
        try:
            raw_data = fetch_weather(loc['lat'], loc['lon'], api_key)
            
            temp = raw_data['main']['temp']
            feels_like = raw_data['main']['feels_like']
            humidity = raw_data['main']['humidity']
            wind_speed = raw_data['wind']['speed']
            weather_main = raw_data['weather'][0]['main']
            description = raw_data['weather'][0]['description']
            
            comfort = calculate_comfort_score(temp, humidity, wind_speed)
            emoji = get_weather_emoji(weather_main, temp)
            personality = get_weather_personality(loc['name'], temp, humidity)
            insight = generate_insight(raw_data, loc['name'])
            
            results.append({
                'name': loc['name'],
                'temp': round(temp, 1),
                'feels_like': round(feels_like, 1),
                'humidity': humidity,
                'wind_speed': round(wind_speed, 1),
                'weather_main': weather_main,
                'description': description,
                'comfort_score': comfort,
                'emoji': emoji,
                'personality': personality,
                'insight': insight,
            })
        except Exception as e:
            print(f"Error fetching weather for {loc['name']}: {e}")
            # Add placeholder data
            results.append({
                'name': loc['name'],
                'temp': 0,
                'feels_like': 0,
                'humidity': 0,
                'wind_speed': 0,
                'weather_main': 'Unknown',
                'description': 'Data unavailable',
                'comfort_score': 0,
                'emoji': '❓',
                'personality': 'Unknown',
                'insight': 'Weather data temporarily unavailable',
            })
    
    return results

def generate_comparison_insight(weather_data: List[Dict]) -> str:
    """Generate comparison between cities"""
    if len(weather_data) < 2:
        return ""
    
    temps = [(w['name'].split(',')[0], w['temp']) for w in weather_data]
    temps_sorted = sorted(temps, key=lambda x: x[1])
    
    coldest = temps_sorted[0]
    hottest = temps_sorted[-1]
    
    if hottest[1] - coldest[1] > 3:
        return f"{coldest[0]} is {round(hottest[1] - coldest[1], 1)}°C cooler than {hottest[0]} today"
    else:
        return f"All cities have similar temperatures today (±{round(hottest[1] - coldest[1], 1)}°C)"

def get_email_subject(weather_data: List[Dict]) -> str:
    """Generate dynamic email subject"""
    emojis = [w['emoji'] for w in weather_data]
    cities = [w['name'].split(',')[0] for w in weather_data]
    
    # Find best weather
    best = max(weather_data, key=lambda x: x['comfort_score'])
    
    date_str = datetime.now().strftime('%b %d')
    return f"{' '.join(emojis[:3])} Weather Update - {date_str} | Best: {best['name'].split(',')[0]}"

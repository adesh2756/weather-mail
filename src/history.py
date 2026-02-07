import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

HISTORY_FILE = 'weather_history.json'

def load_history() -> List[Dict]:
    """Load full history from file"""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading history: {e}")
        return []

def save_daily_record(weather_data: List[Dict]):
    """Save today's weather data if not already saved for today"""
    history = load_history()
    today_str = datetime.now().strftime('%Y-%m-%d')
    
    # Check if we already have data for today
    # (Assuming we run this once a day, or we just overwrite/update today's entry)
    # Let's update if exists, or append if new.
    
    # Filter out today's existing entry if any
    history = [record for record in history if record['date'] != today_str]
    
    # Create new record
    new_record = {
        'date': today_str,
        'timestamp': datetime.now().isoformat(),
        'data': weather_data
    }
    
    history.append(new_record)
    
    # Keep only last 30 days to keep file size small
    if len(history) > 30:
        history = history[-30:]
        
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Error saving history: {e}")

def get_yesterday_data() -> Optional[Dict[str, Dict]]:
    """Get yesterday's weather data mapped by city name"""
    history = load_history()
    if not history:
        return None
        
    yesterday_str = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Find yesterday's record
    yesterday_record = next((r for r in history if r['date'] == yesterday_str), None)
    
    # If yesterday is missing, maybe try the most recent previous record?
    # The user asked for "previous days", so strictly yesterday is best, 
    # but "last recorded" might be more useful if the script didn't run yesterday.
    # Let's stick to "most recent previous" if yesterday is missing, 
    # but label it correctly. For now, let's just look for the last record that isn't today.
    
    today_str = datetime.now().strftime('%Y-%m-%d')
    previous_records = [r for r in history if r['date'] != today_str]
    
    if not previous_records:
        return None
        
    # Get the most recent one
    last_record = previous_records[-1]
    
    # Map by city name for easy lookup
    # Data structure in history is: {'data': [{'name': '...', 'temp': ...}, ...]}
    weather_map = {}
    for city_data in last_record['data']:
        # Use first part of name as key to be safe? Or full name?
        # The project uses full name "Houston, TX" usually.
        weather_map[city_data['name']] = city_data
        
    return {
        'date': last_record['date'],
        'weather': weather_map
    }

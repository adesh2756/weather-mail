#!/usr/bin/env python3
"""Main script to run weather mail system"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from weather import get_all_weather_data, generate_comparison_insight, get_email_subject, get_pizzazz_diff_text
from visualizer import create_temperature_chart, create_forecast_chart
from emailer import send_weather_email
from history import save_daily_record, get_yesterday_data

def main():
    """Main execution"""
    print("🌤️ Starting Weather Mail System...")
    
    # Get API keys from environment
    openweather_api_key = os.environ.get('OPENWEATHER_API_KEY')
    sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
    recipient_email = os.environ.get('RECIPIENT_EMAIL')
    
    if not openweather_api_key:
        print("❌ Error: OPENWEATHER_API_KEY not found in environment")
        sys.exit(1)
    
    if not sendgrid_api_key:
        print("❌ Error: SENDGRID_API_KEY not found in environment")
        sys.exit(1)
    
    if not recipient_email:
        print("❌ Error: RECIPIENT_EMAIL not found in environment")
        sys.exit(1)
    
    # Fetch weather data
    print("📡 Fetching weather data (Current + Forecast)...")
    weather_data = get_all_weather_data(openweather_api_key)
    
    if not weather_data:
        print("❌ Error: Failed to fetch weather data")
        sys.exit(1)
    
    # Process history and analytics
    print("📜 Processing historical data...")
    previous_data = get_yesterday_data()
    
    for city in weather_data:
        city['temp_diff'] = 0
        city['prev_date'] = None
        
        if previous_data and city['name'] in previous_data['weather']:
            prev = previous_data['weather'][city['name']]
            diff = round(city['temp'] - prev['temp'], 1)
            city['temp_diff'] = diff
            city['prev_date'] = previous_data['date']
            
            # Use new Pizzazz generator
            city['diff_str'] = get_pizzazz_diff_text(diff)
        else:
            # Fallback to forecast trend for immediate analytics
            city['diff_str'] = "🆕 Starting fresh!"
            if city.get('forecast') and len(city['forecast']) > 0:
                try:
                    # Get tomorrow's max
                    tomorrow = city['forecast'][0]
                    # Parse "22°-25°" -> 25.0
                    tom_high = float(tomorrow['temp_range'].split('-')[1].replace('°', ''))
                    diff = round(tom_high - city['temp'], 1)
                    pizzazz = get_pizzazz_diff_text(diff)
                    city['diff_str'] = f"Outlook: {pizzazz}"
                except Exception as e:
                    print(f"Error calculating outlook for {city['name']}: {e}")

    # Save today's data
    save_daily_record(weather_data)
    
    print(f"✅ Fetched weather for {len(weather_data)} cities")
    for w in weather_data:
        print(f"  - {w['name']}: {w['temp']}°C {w['emoji']} (Diff: {w.get('diff_str', 'N/A')})")
    
    # Generate charts
    print("📊 Generating charts...")
    chart_bytes = create_temperature_chart(weather_data)
    forecast_chart_bytes = create_forecast_chart(weather_data)
    print("✅ Charts generated")
    
    
    # Generate comparison
    comparison = generate_comparison_insight(weather_data)
    print(f"📈 Comparison: {comparison}")
    
    # Generate subject
    subject = get_email_subject(weather_data)
    print(f"📧 Subject: {subject}")
    
    # Parse recipients
    recipients = [email.strip() for email in recipient_email.split(',') if email.strip()]
    print(f"📮 Sending emails to {len(recipients)} recipients...")
    
    # Get template path
    template_path = Path(__file__).parent / 'templates' / 'email.html'
    
    success_count = 0
    for email in recipients:
        print(f"  - Sending to {email}...")
        if send_weather_email(
            weather_data=weather_data,
            chart_bytes=chart_bytes,
            forecast_chart_bytes=forecast_chart_bytes,
            comparison=comparison,
            subject=subject,
            to_email=email,
            template_path=str(template_path)
        ):
            print(f"    ✅ Sent to {email}")
            success_count += 1
        else:
            print(f"    ❌ Failed to send to {email}")
            
    if success_count > 0:
        print(f"✅ Successfully sent {success_count}/{len(recipients)} emails")
    else:
        print("❌ Failed to send any emails")
        sys.exit(1)

if __name__ == '__main__':
    main()

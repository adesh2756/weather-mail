#!/usr/bin/env python3
"""Main script to run weather mail system"""
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from weather import get_all_weather_data, generate_comparison_insight, get_email_subject
from visualizer import create_temperature_chart
from emailer import send_weather_email

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
    print("📡 Fetching weather data...")
    weather_data = get_all_weather_data(openweather_api_key)
    
    if not weather_data:
        print("❌ Error: Failed to fetch weather data")
        sys.exit(1)
    
    print(f"✅ Fetched weather for {len(weather_data)} cities")
    for w in weather_data:
        print(f"  - {w['name']}: {w['temp']}°C {w['emoji']} (Comfort: {w['comfort_score']}/10)")
    
    # Generate chart
    print("📊 Generating temperature chart...")
    chart_base64 = create_temperature_chart(weather_data)
    print("✅ Chart generated")
    
    # Generate comparison
    comparison = generate_comparison_insight(weather_data)
    print(f"📈 Comparison: {comparison}")
    
    # Generate subject
    subject = get_email_subject(weather_data)
    print(f"📧 Subject: {subject}")
    
    # Send email
    print(f"📮 Sending email to {recipient_email}...")
    
    # Get template path
    template_path = Path(__file__).parent / 'templates' / 'email.html'
    
    success = send_weather_email(
        weather_data=weather_data,
        chart_base64=chart_base64,
        comparison=comparison,
        subject=subject,
        to_email=recipient_email,
        template_path=str(template_path)
    )
    
    if success:
        print("✅ Email sent successfully!")
    else:
        print("❌ Failed to send email")
        sys.exit(1)

if __name__ == '__main__':
    main()

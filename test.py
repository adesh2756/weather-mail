#!/usr/bin/env python3
"""Quick test script to verify the system works"""
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_weather_api():
    """Test weather API integration"""
    print("🧪 Testing Weather API...")
    
    from weather import get_all_weather_data
    
    api_key = os.environ.get('OPENWEATHER_API_KEY', 'test_key')
    
    try:
        weather_data = get_all_weather_data(api_key)
        
        if weather_data and len(weather_data) > 0:
            print("✅ Weather API test passed")
            print(f"   Fetched data for {len(weather_data)} cities")
            for w in weather_data:
                print(f"   - {w['name']}: {w['temp']}°C")
            return True
        else:
            print("❌ Weather API test failed - no data returned")
            return False
    except Exception as e:
        print(f"❌ Weather API test failed: {e}")
        return False

def test_chart_generation():
    """Test chart generation"""
    print("\n🧪 Testing Chart Generation...")
    
    from visualizer import create_temperature_chart
    
    # Mock data
    mock_data = [
        {'name': 'Houston, TX', 'temp': 32, 'feels_like': 36, 'comfort_score': 6},
        {'name': 'Hyderabad, Telangana', 'temp': 28, 'feels_like': 27, 'comfort_score': 9},
        {'name': 'Srikalahasthi, AP', 'temp': 26, 'feels_like': 25, 'comfort_score': 8},
    ]
    
    try:
        chart_base64 = create_temperature_chart(mock_data)
        
        if chart_base64 and len(chart_base64) > 100:
            print("✅ Chart generation test passed")
            print(f"   Generated base64 chart ({len(chart_base64)} chars)")
            return True
        else:
            print("❌ Chart generation test failed")
            return False
    except Exception as e:
        print(f"❌ Chart generation test failed: {e}")
        return False

def test_template_rendering():
    """Test template rendering"""
    print("\n🧪 Testing Template Rendering...")
    
    from emailer import render_template
    
    template_path = Path(__file__).parent / 'templates' / 'email.html'
    
    context = {
        'date': 'February 07, 2026',
        'locations': [
            {
                'name': 'Houston, TX',
                'temp': 32,
                'feels_like': 36,
                'humidity': 80,
                'comfort_score': 6,
                'emoji': '🌧️',
                'personality': 'Humid Houston',
                'insight': 'Rain expected - carry umbrella'
            }
        ],
        'comparison': 'Test comparison',
        'chart': 'test_base64_string'
    }
    
    try:
        html = render_template(str(template_path), context)
        
        if html and len(html) > 500:
            print("✅ Template rendering test passed")
            print(f"   Generated HTML ({len(html)} chars)")
            return True
        else:
            print("❌ Template rendering test failed")
            return False
    except Exception as e:
        print(f"❌ Template rendering test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("🌤️ WEATHER MAIL SYSTEM - TEST SUITE")
    print("=" * 50)
    
    results = []
    
    results.append(test_chart_generation())
    results.append(test_template_rendering())
    
    # Only test weather API if key is available
    if os.environ.get('OPENWEATHER_API_KEY'):
        results.append(test_weather_api())
    else:
        print("\n⚠️  Skipping Weather API test (no API key)")
    
    print("\n" + "=" * 50)
    print(f"📊 RESULTS: {sum(results)}/{len(results)} tests passed")
    print("=" * 50)
    
    if all(results):
        print("✅ All tests passed! System is ready.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Check errors above.")
        sys.exit(1)

if __name__ == '__main__':
    main()

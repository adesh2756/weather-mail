"""Simple but impressive visualization"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import List, Dict
import base64
from io import BytesIO

def create_temperature_chart(weather_data: List[Dict]) -> bytes:
    """Create temperature comparison chart and return as bytes"""
    
    # Set style
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(8, 4), facecolor='#f8f9fa')
    ax.set_facecolor('#ffffff')
    
    cities = [w['name'].split(',')[0] for w in weather_data]
    temps = [w['temp'] for w in weather_data]
    feels_like = [w['feels_like'] for w in weather_data]
    comfort_scores = [w['comfort_score'] for w in weather_data]
    
    x = range(len(cities))
    width = 0.35
    
    # Color bars based on comfort score
    colors = []
    for score in comfort_scores:
        if score >= 8:
            colors.append('#28a745')  # Green
        elif score >= 6:
            colors.append('#ffc107')  # Yellow
        else:
            colors.append('#dc3545')  # Red
    
    # Create bars
    bars1 = ax.bar([i - width/2 for i in x], temps, width, 
                    label='Actual Temp', color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    bars2 = ax.bar([i + width/2 for i in x], feels_like, width,
                    label='Feels Like', color=colors, alpha=0.4, edgecolor='black', linewidth=1.5, hatch='//')
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}°C',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Styling
    ax.set_xlabel('Cities', fontsize=12, fontweight='bold')
    ax.set_ylabel('Temperature (°C)', fontsize=12, fontweight='bold')
    ax.set_title('Temperature Comparison Across Cities', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(cities, fontsize=11)
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    
    # Add comfort score legend
    green_patch = mpatches.Patch(color='#28a745', label='Comfort: 8-10 (Excellent)')
    yellow_patch = mpatches.Patch(color='#ffc107', label='Comfort: 6-7 (Good)')
    red_patch = mpatches.Patch(color='#dc3545', label='Comfort: 0-5 (Poor)')
    ax.legend(handles=[green_patch, yellow_patch, red_patch], 
             loc='upper left', fontsize=9, title='Comfort Score')
    
    plt.tight_layout()
    
    # Convert to bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=72, bbox_inches='tight')
    buffer.seek(0)
    image_bytes = buffer.getvalue()
    plt.close()
    
    return image_bytes

def create_forecast_chart(weather_data: List[Dict]) -> bytes:
    """Create 5-day forecast trend chart"""
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(8, 4), facecolor='#f8f9fa')
    ax.set_facecolor('#ffffff')
    
    # Plot lines for each city
    colors = ['#007bff', '#28a745', '#dc3545', '#6f42c1', '#fd7e14']
    
    for idx, city_data in enumerate(weather_data):
        if not city_data.get('forecast'):
            continue
            
        days = [item['day'] for item in city_data['forecast']]
        # Extract max temps from string "22°-25°" -> 25
        highs = []
        for item in city_data['forecast']:
            try:
                # Parse "22°-25°"
                parts = item['temp_range'].replace('°', '').split('-')
                highs.append(float(parts[1]))
            except:
                highs.append(0)
                
        color = colors[idx % len(colors)]
        ax.plot(days, highs, marker='o', linewidth=2, label=city_data['name'].split(',')[0], color=color)
        
        # Add values
        for i, temp in enumerate(highs):
            ax.annotate(f'{int(temp)}°', (days[i], temp), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color=color)

    # Styling
    ax.set_ylabel('High Temp (°C)', fontsize=10, fontweight='bold')
    ax.set_title('5-Day Temperature Trend', fontsize=12, fontweight='bold', pad=15)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize=9)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Convert to bytes
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=72, bbox_inches='tight')
    buffer.seek(0)
    image_bytes = buffer.getvalue()
    plt.close()
    
    return image_bytes

def create_comfort_score_visual(weather_data: List[Dict]) -> str:
    """Create comfort score visualization as text/emoji"""
    lines = []
    for w in weather_data:
        city = w['name'].split(',')[0]
        score = w['comfort_score']
        
        # Create bar with emojis
        filled = '🟩' * score
        empty = '⬜' * (10 - score)
        
        lines.append(f"{city}: {filled}{empty} {score}/10")
    
    return '\n'.join(lines)

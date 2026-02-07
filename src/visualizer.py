"""Simple but impressive visualization"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import List, Dict
import base64
from io import BytesIO

def create_temperature_chart(weather_data: List[Dict]) -> str:
    """Create temperature comparison chart and return as base64"""
    
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
    
    # Convert to base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=72, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    plt.close()
    
    return image_base64

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

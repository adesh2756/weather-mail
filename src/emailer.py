"""Email sending with SendGrid - FIXED VERSION"""
import os
from datetime import datetime
from typing import List, Dict
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

def render_template(template_path: str, context: Dict) -> str:
    """Simple template rendering (Jinja2-like)"""
    with open(template_path, 'r') as f:
        template = f.read()
    
    # Build location cards HTML
    locations_html = ""
    if 'locations' in context:
        for loc in context['locations']:
            comfort_class = ""
            if loc['comfort_score'] < 6:
                comfort_class = "low"
            elif loc['comfort_score'] < 8:
                comfort_class = "medium"
            
            locations_html += f"""
            <div class="location-card">
                <div class="location-header">
                    <div class="location-name">📍 {loc['name']}</div>
                    <div class="location-emoji">{loc['emoji']}</div>
                </div>
                
                <div class="weather-grid">
                    <div class="weather-item">
                        <div class="weather-label">Temperature</div>
                        <div class="weather-value">{loc['temp']}°C</div>
                    </div>
                    <div class="weather-item">
                        <div class="weather-label">Feels Like</div>
                        <div class="weather-value">{loc['feels_like']}°C</div>
                    </div>
                    <div class="weather-item">
                        <div class="weather-label">Humidity</div>
                        <div class="weather-value">{loc['humidity']}%</div>
                    </div>
                    <div class="weather-item">
                        <div class="weather-label">Comfort Score</div>
                        <div class="weather-value">
                            <span class="comfort-score {comfort_class}">
                                {loc['comfort_score']}/10
                            </span>
                        </div>
                    </div>
                </div>
                
                <div class="insight">
                    💡 <strong>{loc['personality']}</strong> - {loc['insight']}
                </div>
            </div>
            """
    
    # Remove the for loop template tags and insert actual HTML
    # Find the location loop section
    loop_start = template.find('{% for location in locations %}')
    loop_end = template.find('{% endfor %}')
    
    if loop_start != -1 and loop_end != -1:
        # Replace everything between the loop tags with actual HTML
        before_loop = template[:loop_start]
        after_loop = template[loop_end + len('{% endfor %}'):]
        template = before_loop + locations_html + after_loop
    
    # Replace simple variables
    template = template.replace('{{ date }}', context.get('date', ''))
    
    # Handle comparison section
    if context.get('comparison'):
        template = template.replace('{% if comparison %}', '')
        template = template.replace('{{ comparison }}', context['comparison'])
        # Find and remove the first {% endif %} after comparison
        comparison_pos = template.find('Comparison:')
        if comparison_pos != -1:
            endif_pos = template.find('{% endif %}', comparison_pos)
            if endif_pos != -1:
                template = template[:endif_pos] + template[endif_pos + len('{% endif %}'):]
    else:
        # Remove entire comparison section
        start = template.find('{% if comparison %}')
        if start != -1:
            end = template.find('{% endif %}', start)
            if end != -1:
                template = template[:start] + template[end + len('{% endif %}'):]
    
    # Handle chart section
    if context.get('chart'):
        template = template.replace('{% if chart %}', '')
        template = template.replace('{{ chart }}', context['chart'])
        # Find and remove the {% endif %} after chart
        chart_pos = template.find('data:image/png;base64,')
        if chart_pos != -1:
            endif_pos = template.find('{% endif %}', chart_pos)
            if endif_pos != -1:
                template = template[:endif_pos] + template[endif_pos + len('{% endif %}'):]
    else:
        # Remove entire chart section
        start = template.find('{% if chart %}')
        if start != -1:
            end = template.find('{% endif %}', start)
            if end != -1:
                template = template[:start] + template[end + len('{% endif %}'):]
    
    return template

def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    from_email: str = "adesh.malisetty@gmail.com",  # CHANGE THIS TO YOUR VERIFIED EMAIL
    sendgrid_api_key: str = None
) -> bool:
    """Send email via SendGrid"""
    
    if not sendgrid_api_key:
        sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
    
    if not sendgrid_api_key:
        print("Error: SENDGRID_API_KEY not found")
        return False
    
    try:
        message = Mail(
            from_email=Email(from_email),
            to_emails=To(to_email),
            subject=subject,
            html_content=Content("text/html", html_content)
        )
        
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        
        print(f"Email sent! Status code: {response.status_code}")
        return response.status_code == 202
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_weather_email(
    weather_data: List[Dict],
    chart_base64: str,
    comparison: str,
    subject: str,
    to_email: str,
    template_path: str = "templates/email.html"
) -> bool:
    """Main function to send weather email"""
    
    context = {
        'date': datetime.now().strftime('%A, %B %d, %Y'),
        'locations': weather_data,
        'chart': chart_base64,
        'comparison': comparison,
    }
    
    html_content = render_template(template_path, context)
    
    return send_email(
        to_email=to_email,
        subject=subject,
        html_content=html_content
    )
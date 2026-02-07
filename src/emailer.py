"""Email sending with SendGrid"""
import os
from datetime import datetime
from typing import List, Dict
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

def render_template(template_path: str, context: Dict) -> str:
    """Simple template rendering (Jinja2-like)"""
    with open(template_path, 'r') as f:
        template = f.read()
    
    # Simple replacement for {% for %} loops
    # This is a simplified version - in production use Jinja2
    locations_html = ""
    if 'locations' in context:
        for loc in context['locations']:
            # Create location card HTML
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
    
    # Replace template variables
    template = template.replace('{% for location in locations %}', '')
    template = template.replace('{% endfor %}', locations_html)
    template = template.replace('{{ date }}', context.get('date', ''))
    
    # Handle comparison
    if context.get('comparison'):
        template = template.replace('{% if comparison %}', '')
        template = template.replace('{% endif %}', '', 1)  # First occurrence
        template = template.replace('{{ comparison }}', context['comparison'])
    else:
        # Remove comparison section
        start = template.find('{% if comparison %}')
        end = template.find('{% endif %}', start)
        if start != -1 and end != -1:
            template = template[:start] + template[end + 11:]
    
    # Handle chart
    if context.get('chart'):
        template = template.replace('{% if chart %}', '')
        template = template.replace('{% endif %}', '')
        template = template.replace('{{ chart }}', context['chart'])
    else:
        # Remove chart section
        start = template.find('{% if chart %}')
        end = template.find('{% endif %}', start)
        if start != -1 and end != -1:
            template = template[:start] + template[end + 11:]
    
    return template

def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    from_email: str = "weather@example.com",
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

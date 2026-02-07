"""Email sending with SendGrid - FIXED VERSION"""
import os
import base64
from datetime import datetime
from typing import List, Dict, Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition, ContentId

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
            
            # Build forecast HTML
            forecast_html = '<div class="forecast-container" style="margin-top: 15px; border-top: 1px dashed #eee; padding-top: 10px;">'
            forecast_html += '<div style="font-size: 0.85em; color: #666; margin-bottom: 8px; font-weight: bold;">5-Day Forecast</div>'
            forecast_html += '<div style="display: flex; justify-content: space-between; text-align: center;">'
            
            for day in loc.get('forecast', []):
                forecast_html += f'''
                <div class="forecast-day" style="flex: 1;">
                    <div style="font-size: 0.9em; font-weight: bold; color: #555;">{day['day']}</div>
                    <div style="font-size: 1.4em; margin: 2px 0;">{day['emoji']}</div>
                    <div style="font-size: 0.85em; color: #777;">{day['temp_range']}</div>
                </div>
                '''
            forecast_html += '</div></div>'

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
                        <div class="weather-label">Trend</div>
                        <div class="weather-value" style="font-size: 1em;">{loc.get('diff_str', 'N/A')}</div>
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
                
                {forecast_html}
            </div>
            """
    
    # Remove the for loop template tags and insert actual HTML
    loop_start = template.find('{% for location in locations %}')
    loop_end = template.find('{% endfor %}')
    
    if loop_start != -1 and loop_end != -1:
        before_loop = template[:loop_start]
        after_loop = template[loop_end + len('{% endfor %}'):]
        template = before_loop + locations_html + after_loop
    
    # Replace simple variables
    template = template.replace('{{ date }}', context.get('date', ''))
    
    # Handle comparison section
    if context.get('comparison'):
        template = template.replace('{% if comparison %}', '')
        template = template.replace('{{ comparison }}', context['comparison'])
        # Cleanup endif
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
    
    # Handle charts - Simple Replacement now because HTML uses pure {{ chart }} src
    if context.get('chart'):
        template = template.replace('{% if chart %}', '')
        template = template.replace('{{ chart }}', context['chart'])
        # Cleanup endif
        # We need to find the endif AFTER the chart.
        # Since we don't have the unique data string anymore, we search for the alt tag context
        # "Temperature Chart"
        chart_marker = 'alt="Temperature Chart"'
        marker_pos = template.find(chart_marker)
        if marker_pos != -1:
             endif_pos = template.find('{% endif %}', marker_pos)
             if endif_pos != -1:
                 template = template[:endif_pos] + template[endif_pos + len('{% endif %}'):]
    else:
        start = template.find('{% if chart %}')
        if start != -1:
            end = template.find('{% endif %}', start)
            if end != -1:
                template = template[:start] + template[end + len('{% endif %}'):]

    if context.get('forecast_chart'):
        template = template.replace('{% if forecast_chart %}', '')
        template = template.replace('{{ forecast_chart }}', context['forecast_chart'])
        # Cleanup endif
        chart_marker = 'alt="Forecast Chart"'
        marker_pos = template.find(chart_marker)
        if marker_pos != -1:
             endif_pos = template.find('{% endif %}', marker_pos)
             if endif_pos != -1:
                 template = template[:endif_pos] + template[endif_pos + len('{% endif %}'):]
    else:
        start = template.find('{% if forecast_chart %}')
        if start != -1:
            end = template.find('{% endif %}', start)
            if end != -1:
                template = template[:start] + template[end + len('{% endif %}'):]

    return template

def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    from_email: str = "adesh.malisetty@gmail.com",
    sendgrid_api_key: str = None,
    attachments: List[Attachment] = None
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
        
        if attachments:
            for attachment in attachments:
                message.add_attachment(attachment)
        
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        
        print(f"Email sent! Status code: {response.status_code}")
        return response.status_code == 202
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_weather_email(
    weather_data: List[Dict],
    chart_bytes: bytes,
    forecast_chart_bytes: bytes,
    comparison: str,
    subject: str,
    to_email: str,
    template_path: str = "templates/email.html"
) -> bool:
    """Main function to send weather email"""
    
    attachments = []
    
    # Process Temperature Chart
    chart_cid = "chart_img"
    if chart_bytes:
        encoded_chart = base64.b64encode(chart_bytes).decode()
        attachment = Attachment()
        attachment.file_content = FileContent(encoded_chart)
        attachment.file_type = FileType('image/png')
        attachment.file_name = FileName('chart.png')
        attachment.disposition = Disposition('inline')
        attachment.content_id = ContentId(chart_cid)
        attachments.append(attachment)
    
    # Process Forecast Chart
    forecast_cid = "forecast_chart_img"
    if forecast_chart_bytes:
        encoded_forecast = base64.b64encode(forecast_chart_bytes).decode()
        attachment = Attachment()
        attachment.file_content = FileContent(encoded_forecast)
        attachment.file_type = FileType('image/png')
        attachment.file_name = FileName('forecast_chart.png')
        attachment.disposition = Disposition('inline')
        attachment.content_id = ContentId(forecast_cid)
        attachments.append(attachment)
    
    context = {
        'date': datetime.now().strftime('%A, %B %d, %Y'),
        'locations': weather_data,
        'chart': f"cid:{chart_cid}" if chart_bytes else None,
        'forecast_chart': f"cid:{forecast_cid}" if forecast_chart_bytes else None,
        'comparison': comparison,
    }
    
    html_content = render_template(template_path, context)
    
    return send_email(
        to_email=to_email,
        subject=subject,
        html_content=html_content,
        attachments=attachments
    )
# 🌤️ Weather Mail - Daily Weather Digest System

Automated daily weather emails for Houston, Hyderabad, and Srikalahasthi with smart analytics and beautiful visualizations.

## ✨ Features

### Smart Analytics
- **Comfort Score (0-10)**: Calculated from temperature, humidity, and wind speed
- **Weather Personality**: "Humid Houston", "Pleasant Hyderabad", etc.
- **Intelligent Insights**: Context-aware tips like "Rain expected - carry umbrella"
- **City Comparisons**: "Srikalahasthi is 5°C cooler than Houston today"

### Professional Email
- Dynamic emoji-based subject lines
- Color-coded comfort scores (green/yellow/red)
- Embedded temperature comparison chart
- Responsive HTML design

### Zero-Cost Automation
- Runs on GitHub Actions (free)
- Uses free tier APIs (OpenWeather, SendGrid)
- No server costs

## 🚀 Quick Start

### 1. Get API Keys

**OpenWeather API** (Free tier: 1000 calls/day)
1. Sign up at https://openweathermap.org/api
2. Generate API key
3. Save as `OPENWEATHER_API_KEY`

**SendGrid API** (Free tier: 100 emails/day)
1. Sign up at https://sendgrid.com
2. Create API key with "Mail Send" permission
3. Verify sender email address
4. Save as `SENDGRID_API_KEY`

### 2. Fork & Configure

1. Fork this repository to your GitHub account
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Add three secrets:
   - `OPENWEATHER_API_KEY`: Your OpenWeather API key
   - `SENDGRID_API_KEY`: Your SendGrid API key
   - `RECIPIENT_EMAIL`: Your uncle's email address

### 3. Test Locally (Optional)

```bash
# Install uv (fast Python package installer)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repository
git clone https://github.com/yourusername/weather-mail.git
cd weather-mail

# Create .env file
cp .env.example .env
# Edit .env with your API keys

# Install dependencies
uv pip install -e .

# Run
python main.py
```

### 4. Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. Enable workflows
3. The workflow runs daily at 6:00 AM UTC (11:30 AM IST / 12:00 AM CST)
4. Manual trigger: **Actions** → **Daily Weather Email** → **Run workflow**

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      GitHub Actions (Free)                       │
│                     Runs daily at 6:00 AM UTC                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    main.py      │ ← Orchestrator
                    └────────┬────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
           ▼                 ▼                 ▼
    ┌──────────┐      ┌──────────┐     ┌──────────┐
    │ weather  │      │visualizer│     │ emailer  │
    │   .py    │      │   .py    │     │   .py    │
    └────┬─────┘      └────┬─────┘     └────┬─────┘
         │                 │                 │
         │ Fetches         │ Generates       │ Sends via
         │ from            │ chart           │ SendGrid
         │                 │                 │
         ▼                 ▼                 ▼
    OpenWeather       Matplotlib         email.html
       API             Base64             Template
    (Free tier)        Image           (Responsive)

Data Flow:
1. GitHub Actions triggers main.py
2. weather.py fetches data for 3 cities
3. weather.py calculates comfort scores & insights
4. visualizer.py creates temperature chart
5. emailer.py renders HTML template with data
6. SendGrid delivers email to recipient

File Structure:
weather-mail/
├── src/
│   ├── weather.py       # API calls + analytics (combined for speed)
│   ├── visualizer.py    # Temperature chart generation
│   └── emailer.py       # SendGrid email sending
├── templates/
│   └── email.html       # Professional HTML email template
├── .github/workflows/
│   └── daily.yml        # GitHub Actions automation
├── main.py              # Orchestrator script
├── pyproject.toml       # Dependencies (uv-based)
└── README.md
```

## 🎯 What Makes This Impressive

### 1. Clean Architecture
- **Separation of concerns**: Weather fetching, analytics, visualization, and email sending are cleanly separated
- **Combined modules**: Weather API + analytics in one file to reduce complexity without sacrificing clarity
- **Template-based emails**: HTML templating for easy customization

### 2. Smart Analytics
- **Comfort Score Algorithm**: Multi-factor scoring (temperature, humidity, wind)
  - Temperature: Optimal 20-26°C
  - Humidity: Optimal 40-60%
  - Wind: Optimal <15 km/h
- **Context-Aware Insights**: Different insights for rain, humidity, temperature extremes
- **Comparative Analysis**: Automatic city-to-city comparisons

### 3. Production-Ready
- **Error handling**: Graceful degradation if API fails
- **Type hints**: Better code documentation
- **Modular design**: Easy to extend (add cities, metrics, charts)
- **Zero-cost hosting**: Runs entirely on free tiers

## 🔧 Customization

### Add More Cities

Edit `src/weather.py`:

```python
LOCATIONS = [
    {"name": "Houston, TX", "lat": 29.76, "lon": -95.36},
    {"name": "Hyderabad, Telangana", "lat": 17.38, "lon": 78.48},
    {"name": "Srikalahasthi, AP", "lat": 13.75, "lon": 79.70},
    {"name": "Your City", "lat": XX.XX, "lon": YY.YY},  # Add here
]
```

### Change Schedule

Edit `.github/workflows/daily.yml`:

```yaml
on:
  schedule:
    - cron: '0 6 * * *'  # Change this (UTC time)
```

Cron helper: https://crontab.guru/

### Modify Email Template

Edit `templates/email.html` - full HTML/CSS customization supported.

## 📈 Sample Output

**Email Subject:**
```
☀️ 🌤️ 🌧️ Weather Update - Feb 07 | Best: Hyderabad
```

**Email Content:**
- 📍 Houston: 32°C (Feels 36°C) - Comfort: 6/10 - "Humid Houston - Rain expected"
- 📍 Hyderabad: 28°C (Feels 27°C) - Comfort: 9/10 - "Pleasant Hyderabad - Perfect weather"
- 📍 Srikalahasthi: 26°C (Feels 25°C) - Comfort: 8/10 - "Ideal temple visit weather"
- 📊 Comparison: Srikalahasthi is 6°C cooler than Houston today
- [Temperature Chart Image]

## 🐛 Troubleshooting

**Email not sending?**
- Check SendGrid sender verification
- Verify API keys in GitHub Secrets
- Check Actions logs for errors

**Weather data missing?**
- Verify OpenWeather API key is valid
- Check free tier limits (1000 calls/day)
- Review coordinates are correct

**Chart not appearing?**
- Ensure matplotlib installed correctly
- Check base64 encoding in logs

## 📝 Technical Decisions

1. **uv over pip**: 10-100x faster package installation
2. **Matplotlib over Plotly**: Smaller dependency, sufficient for static charts
3. **Manual templating over Jinja2**: Reduce dependencies, simple enough
4. **Combined weather.py**: Fewer files without sacrificing readability
5. **GitHub Actions over AWS Lambda**: Zero cost, simpler setup

## 🎓 Learning Points for CS Students

- **API Integration**: RESTful APIs (OpenWeather)
- **Data Processing**: JSON parsing, data transformation
- **Visualization**: Matplotlib charting
- **Email Automation**: SMTP alternatives (SendGrid)
- **CI/CD**: GitHub Actions for automation
- **Environment Variables**: Secure credential management
- **Error Handling**: Graceful degradation patterns

## 📜 License

MIT License - Feel free to use and modify!

## 🙏 Credits

- Weather data: [OpenWeather API](https://openweathermap.org/)
- Email delivery: [SendGrid](https://sendgrid.com/)
- Automation: [GitHub Actions](https://github.com/features/actions)

---

**Built in 3 hours** ⏱️ | **Zero monthly cost** 💰 | **Runs forever** ♾️
# weather-mail

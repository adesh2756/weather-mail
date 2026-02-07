# 🚀 WEATHER MAIL - COMPLETE SETUP GUIDE

## 📋 System Overview

**Built in 3 hours | Zero monthly cost | Runs forever**

This system sends daily weather emails with:
- ✅ Weather for 3 cities (Houston, Hyderabad, Srikalahasthi)
- ✅ Smart comfort scores (0-10 algorithm)
- ✅ Beautiful temperature chart
- ✅ Intelligent insights & comparisons
- ✅ Professional HTML email
- ✅ Automated via GitHub Actions (FREE)

## 🏗️ Complete File Structure (8 Core Files)

```
weather-mail/
├── pyproject.toml              # Dependencies (uv-based)
├── main.py                     # Main orchestrator
├── setup.sh                    # Quick setup script
├── test.py                     # Test suite
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── README.md                   # Full documentation
│
├── src/
│   ├── weather.py              # Weather API + Analytics (combined)
│   ├── visualizer.py           # Chart generation
│   └── emailer.py              # SendGrid integration
│
├── templates/
│   └── email.html              # Professional HTML template
│
└── .github/workflows/
    └── daily.yml               # GitHub Actions automation
```

## 🎯 Step-by-Step Setup (15 minutes)

### Step 1: Get API Keys (5 minutes)

#### OpenWeather API
1. Go to https://openweathermap.org/api
2. Sign up for free account
3. Click "API Keys" tab
4. Copy your API key
5. Free tier: 1,000 calls/day (we use 1/day)

#### SendGrid API
1. Go to https://sendgrid.com
2. Sign up for free account
3. Go to Settings → API Keys
4. Create new API key with "Mail Send" permission
5. Copy the API key (shown only once!)
6. **IMPORTANT**: Verify sender email
   - Go to Settings → Sender Authentication
   - Verify your email address
   - Check your inbox and click verification link
7. Free tier: 100 emails/day (we use 1/day)

### Step 2: Fork Repository (2 minutes)

1. Fork this repository to your GitHub account
2. Clone to your local machine (optional for testing)

```bash
git clone https://github.com/YOUR_USERNAME/weather-mail.git
cd weather-mail
```

### Step 3: Configure GitHub Secrets (3 minutes)

1. Go to your forked repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add three secrets:

| Secret Name | Value | Example |
|------------|-------|---------|
| `OPENWEATHER_API_KEY` | Your OpenWeather API key | `abc123def456...` |
| `SENDGRID_API_KEY` | Your SendGrid API key | `SG.xyz789...` |
| `RECIPIENT_EMAIL` | Your uncle's email | `uncle@example.com` |

### Step 4: Enable GitHub Actions (2 minutes)

1. Go to **Actions** tab in your repository
2. Click "I understand my workflows, go ahead and enable them"
3. The workflow will run:
   - **Automatically**: Every day at 6:00 AM UTC
   - **Manually**: Actions → Daily Weather Email → Run workflow

### Step 5: Test (3 minutes)

**Option A: Test via GitHub Actions**
1. Go to Actions tab
2. Click "Daily Weather Email"
3. Click "Run workflow" → "Run workflow"
4. Wait 1-2 minutes
5. Check your email!

**Option B: Test locally**
```bash
# Install dependencies
./setup.sh

# Edit .env file with your API keys
nano .env

# Run test suite
python test.py

# Send test email
python main.py
```

## ⏰ Schedule Details

**Default Schedule**: 6:00 AM UTC daily
- **Houston (CST)**: 12:00 AM (midnight)
- **Hyderabad (IST)**: 11:30 AM
- **Srikalahasthi (IST)**: 11:30 AM

**Change Schedule**: Edit `.github/workflows/daily.yml`

```yaml
schedule:
  - cron: '0 6 * * *'  # Change this
  # Format: minute hour day month weekday
  # Example: '30 14 * * *' = 2:30 PM UTC daily
```

Use https://crontab.guru/ to generate cron expressions.

## 🎨 Customization Guide

### Add More Cities

Edit `src/weather.py`:

```python
LOCATIONS = [
    {"name": "Houston, TX", "lat": 29.76, "lon": -95.36},
    {"name": "Hyderabad, Telangana", "lat": 17.38, "lon": 78.48},
    {"name": "Srikalahasthi, AP", "lat": 13.75, "lon": 79.70},
    # Add your city here:
    {"name": "New York, NY", "lat": 40.71, "lon": -74.00},
]
```

Find coordinates: https://www.latlong.net/

### Change Sender Email

Edit `src/emailer.py`:

```python
from_email: str = "weather@example.com"  # Change this
```

**Important**: Must match verified email in SendGrid!

### Modify Email Design

Edit `templates/email.html` - full HTML/CSS control.

Key sections:
- `.header`: Top banner
- `.location-card`: City weather cards
- `.chart-section`: Chart display
- `.footer`: Bottom info

### Adjust Comfort Score Algorithm

Edit `src/weather.py` → `calculate_comfort_score()`:

```python
# Current algorithm
# Temperature: Optimal 20-26°C
# Humidity: Optimal 40-60%
# Wind: Optimal <15 km/h

# Modify the ranges to suit your preferences
```

## 🔍 Impressive Features Explained

### 1. Comfort Score (0-10)

**Algorithm**:
```
comfort_score = (temp_score + humidity_score + wind_score) / 3

temp_score: 
  - 10 if 20-26°C (perfect)
  - 7 if 15-30°C (good)
  - Decreases as deviation increases

humidity_score:
  - 10 if 40-60% (ideal)
  - Decreases based on deviation

wind_score:
  - 10 if <15 km/h (calm)
  - Decreases as wind increases
```

### 2. Weather Personality

Generated based on conditions:
- "Humid Houston" (humidity > 70%)
- "Hot Hyderabad" (temp > 30°C)
- "Pleasant Srikalahasthi" (temp 20-28°C)
- "Cool [City]" (temp < 15°C)
- "Breezy [City]" (default)

### 3. Intelligent Insights

Context-aware tips:
- Rain detected → "Carry umbrella"
- Low humidity → "Stay hydrated"
- High humidity → "Feels muggy"
- Perfect temp → "Great for outdoor activities"
- Hot → "Limit sun exposure"
- Srikalahasthi + cool → "Ideal temple visit weather"

### 4. Dynamic Email Subject

Format: `[emoji] [emoji] [emoji] Weather Update - Date | Best: [City]`

Example:
```
🔥🌧️ ☀️ 🌤️ Weather Update - Feb 07 | Best: Hyderabad
```

### 5. Temperature Chart

- Color-coded by comfort score:
  - 🟢 Green: 8-10 (Excellent)
  - 🟡 Yellow: 6-7 (Good)
  - 🔴 Red: 0-5 (Poor)
- Shows both actual and "feels like" temperatures
- Embedded directly in email (base64)

## 🐛 Troubleshooting

### Email Not Sending

**Check SendGrid verification**:
```
Settings → Sender Authentication → Single Sender Verification
```

**Check API key permissions**:
- Should have "Mail Send" permission
- If restricted, create new key with full access

**Check GitHub Actions logs**:
```
Actions → Daily Weather Email → Latest run → send-weather-email
```

### Weather Data Missing

**Check API key**:
```bash
curl "https://api.openweathermap.org/data/2.5/weather?lat=29.76&lon=-95.36&appid=YOUR_KEY"
```

**Check rate limits**:
- Free tier: 1,000 calls/day
- We use 3 calls/day (one per city)

### Chart Not Appearing

**Check matplotlib installation**:
```bash
python -c "import matplotlib; print('OK')"
```

**Check base64 encoding**:
- Chart is embedded as base64 in email
- Large images may trigger spam filters
- Current chart is optimized (~64KB)

### GitHub Actions Not Running

**Enable workflows**:
```
Actions → Enable workflows
```

**Check workflow syntax**:
```bash
# Local validation (requires act)
act -l
```

**Manual trigger**:
```
Actions → Daily Weather Email → Run workflow
```

## 💡 Pro Tips

### 1. Test Before Deploying
```bash
# Always test locally first
python test.py
python main.py
```

### 2. Monitor GitHub Actions
- Set up notifications for workflow failures
- Settings → Notifications → Actions

### 3. Check Spam Folder
- First email might go to spam
- Mark as "Not Spam" to train filters

### 4. Backup API Keys
- Store in password manager
- Never commit to Git

### 5. Monitor Free Tier Limits
- OpenWeather: Check dashboard monthly
- SendGrid: Check email statistics

## 🎓 Architecture Deep Dive

### Why Combined `weather.py`?

**Decision**: Combine API calls + analytics in one file

**Reasoning**:
- ✅ Fewer files = simpler structure
- ✅ Related functionality together
- ✅ Still only 200 lines (manageable)
- ✅ No circular dependencies

**Alternative**: Separate `weather_api.py` and `analytics.py`
- Better for large teams
- Overkill for 3-hour project

### Why Manual Template Rendering?

**Decision**: Simple string replacement vs. Jinja2

**Reasoning**:
- ✅ Zero dependencies
- ✅ Template is simple (no complex logic)
- ✅ 50 lines vs. entire library
- ❌ Not scalable for complex templates

**When to switch to Jinja2**:
- Multiple templates
- Complex conditional rendering
- Template inheritance needed

### Why Matplotlib vs. Plotly?

**Decision**: Matplotlib for charts

**Reasoning**:
- ✅ Smaller dependency (6MB vs 50MB)
- ✅ Static images sufficient
- ✅ Better base64 embedding
- ❌ Plotly is prettier and interactive

**When to use Plotly**:
- Interactive charts needed
- Web dashboard (not email)
- Real-time updates

### Why GitHub Actions vs. AWS Lambda?

**Decision**: GitHub Actions for automation

**Reasoning**:
- ✅ Completely free
- ✅ No credit card needed
- ✅ Simple YAML config
- ✅ Built-in secrets management
- ✅ 2,000 minutes/month free

**AWS Lambda**:
- More powerful (real backend)
- Requires AWS account + credit card
- Free tier: 1M requests/month
- Better for production APIs

## 📊 Success Metrics

After setup, you should see:

✅ **Daily emails arriving at 6:00 AM UTC**
✅ **3 city weather cards**
✅ **Temperature chart embedded**
✅ **Comfort scores calculated**
✅ **Intelligent insights generated**
✅ **GitHub Actions run successfully**
✅ **Zero failures in logs**

## 🎯 Impress Your Uncle (CS Expert)

### Point 1: Clean Architecture
"See how I separated concerns? Weather fetching, visualization, and email sending are completely independent. I could swap SendGrid for SES in 5 minutes."

### Point 2: Smart Analytics
"The comfort score isn't just a number - it's a weighted algorithm considering temperature (optimal 20-26°C), humidity (40-60%), and wind speed. The insights are context-aware - it knows Srikalahasthi is a temple town."

### Point 3: Production-Ready
"Zero-cost hosting on GitHub Actions with proper error handling. If OpenWeather fails, it gracefully degrades. The email template is responsive HTML/CSS. And look - the entire system is tested before deployment."

### Point 4: Efficient Implementation
"Built the entire system in 3 hours by making smart tradeoffs: combined weather.py instead of 3 separate files, manual templating instead of Jinja2, one killer chart instead of five mediocre ones. Time-to-value over perfection."

## 🔐 Security Notes

✅ **API keys in GitHub Secrets** (never in code)
✅ **No credentials in Git history**
✅ **Read-only OpenWeather access**
✅ **SendGrid restricted to mail send only**
✅ **Rate limiting on APIs**
✅ **Error messages don't leak keys**

## 📈 Future Enhancements (Out of Scope)

If you want to extend the system:

1. **Historical data tracking** (store in GitHub as JSON)
2. **Weather alerts** (send extra email if extreme weather)
3. **Multiple recipients** (CC family members)
4. **SMS notifications** (Twilio integration)
5. **Forecast comparison** (predicted vs. actual)
6. **Interactive dashboard** (GitHub Pages + Chart.js)
7. **Machine learning predictions** (temperature trends)

## 📞 Support

**Found a bug?** Open an issue on GitHub
**Have a question?** Check the troubleshooting section
**Want to contribute?** Pull requests welcome!

## 🙏 Acknowledgments

- **OpenWeather**: Free weather API
- **SendGrid**: Free email delivery
- **GitHub**: Free automation platform
- **Python**: Best language for rapid prototyping
- **uv**: Blazing fast package installer

---

**Built with ❤️ in 3 hours**

Time breakdown:
- Core logic (weather.py): 45 min
- Visualization (visualizer.py): 30 min
- Email system (emailer.py): 30 min
- Template (email.html): 30 min
- GitHub Actions: 15 min
- Documentation: 30 min

**Total: 3 hours** ⏱️

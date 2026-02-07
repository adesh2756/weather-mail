# 🚀 WEATHER MAIL - QUICK START (5 MINUTES)

## What You Get
Daily email with weather for Houston, Hyderabad, and Srikalahasthi featuring:
- Smart comfort scores (0-10 algorithm)
- Beautiful temperature chart
- Intelligent insights ("Rain expected - carry umbrella")
- Professional HTML design
- 100% automated via GitHub Actions
- **$0/month cost**

YMBNFZLFR32CZKAKSTA2S6K7

## Setup (15 minutes max)

### Step 1: Get API Keys (5 min)

**OpenWeather** → https://openweathermap.org/api
1. Sign up (free)
2. Copy API key from dashboard
3. Free tier: 1,000 calls/day (we use 1)

**SendGrid** → https://sendgrid.com
1. Sign up (free)
2. Settings → API Keys → Create (with "Mail Send" permission)
3. **IMPORTANT**: Settings → Sender Authentication → Verify your email
4. Free tier: 100 emails/day (we use 1)

### Step 2: Deploy (5 min)

1. **Fork** this repository to your GitHub account

2. **Add secrets**: Settings → Secrets and variables → Actions → New secret
   ```
   OPENWEATHER_API_KEY = your_key_here
   SENDGRID_API_KEY = your_key_here  
   RECIPIENT_EMAIL = uncle@example.com
   ```

3. **Enable**: Actions tab → Enable workflows

### Step 3: Test (2 min)

**Actions** → **Daily Weather Email** → **Run workflow**

Check email in 1-2 minutes! 📧

## Schedule

Runs automatically every day at:
- **6:00 AM UTC**
- **11:30 AM IST** (Hyderabad/Srikalahasthi)
- **12:00 AM CST** (Houston)

## File Structure

```
weather-mail/
├── main.py                  ← Runs everything
├── src/
│   ├── weather.py           ← Weather API + analytics
│   ├── visualizer.py        ← Chart generation
│   └── emailer.py           ← Email sending
├── templates/
│   └── email.html           ← Email template
└── .github/workflows/
    └── daily.yml            ← GitHub Actions config
```

**Total: 755 lines of code**

## Customization

### Add Cities
Edit `src/weather.py`:
```python
LOCATIONS = [
    {"name": "Houston, TX", "lat": 29.76, "lon": -95.36},
    {"name": "Your City", "lat": XX.XX, "lon": YY.YY},  # Add here
]
```

### Change Schedule
Edit `.github/workflows/daily.yml`:
```yaml
cron: '0 6 * * *'  # Change time (UTC)
```
Use https://crontab.guru/ for help

### Modify Template
Edit `templates/email.html` - full HTML/CSS control

## Test Locally (Optional)

```bash
# Install dependencies
./setup.sh

# Create .env file
cp .env.example .env
# Edit with your API keys

# Run tests
python test.py

# Send email
python main.py
```

## Troubleshooting

**Email not arriving?**
→ Check SendGrid sender verification
→ Check spam folder
→ View GitHub Actions logs

**API errors?**
→ Verify API keys in GitHub Secrets
→ Check free tier limits

**Want help?**
→ Read SETUP_GUIDE.md (comprehensive)
→ Read PROJECT_SUMMARY.md (technical details)
→ Read EMAIL_SAMPLE.md (see example output)

## What Makes This Impressive

1. **Clean Architecture** - Modular design, easy to extend
2. **Smart Analytics** - Comfort scores, insights, comparisons
3. **Professional Output** - Beautiful emails, embedded charts
4. **Zero Cost** - Runs forever on free tiers
5. **Fast Build** - Complete system in 3 hours

## Key Features

✅ Multi-city weather tracking
✅ Comfort score algorithm (temp + humidity + wind)
✅ Context-aware insights
✅ Temperature comparison chart
✅ Dynamic email subjects
✅ Mobile-responsive design
✅ Automated daily delivery
✅ Error handling & logging
✅ Complete documentation

## Tech Stack

- **Python 3.11+** - Modern Python
- **OpenWeather API** - Weather data
- **SendGrid** - Email delivery
- **Matplotlib** - Chart generation
- **GitHub Actions** - Automation
- **uv** - Fast package manager

## Documentation

- `README.md` - Overview & features
- `SETUP_GUIDE.md` - Step-by-step setup (15 min)
- `EMAIL_SAMPLE.md` - Visual example
- `PROJECT_SUMMARY.md` - Technical deep dive

## Support

**GitHub Issues** → Report bugs
**Pull Requests** → Contribute improvements
**Discussions** → Ask questions

---

**Built in 3 hours** ⏱️ | **$0/month** 💰 | **Runs forever** ♾️

Ready to impress your uncle! 🎯

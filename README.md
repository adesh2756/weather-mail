# Weather Mail System

A robust, automated daily weather digest system that aggregates weather data for multiple locations, performs analytics, and delivers comprehensive reports via email. This system leverages the OpenWeatherMap API for data acquisition and SendGrid for reliable email delivery, orchestrated by GitHub Actions for zero-cost automation.

## Features

### Advanced Analytics
- **Comfort Indexing**: Calculates a standardized comfort score (0-10) based on temperature, humidity, and wind speed.
- **Trend Analysis**: Tracks day-over-day temperature changes and provides immediate outlook forecasts (e.g., "Heating up", "Cooling off").
- **Smart Insights**: Generates context-aware weather summaries and recommendations based on current conditions.
- **Comparative Metrics**: Automatically highlights temperature differences between monitored locations.

### Visualization & Reporting
- **Data Visualization**: Generates embedded line charts showing 5-day temperature trends and bar charts for current comparisons.
- **Rich Email Templates**: Delivers professional, responsive HTML emails with color-coded indicators and location-specific details.
- **Forecast Integration**: Includes detailed 5-day forecasts with daily high/low temperatures.

### Technical Architecture
- **Automated Workflow**: Fully automated execution using GitHub Actions cron schedules.
- **Resilient Design**: Includes error handling for API failures and graceful degradation.
- **Efficient Resource Usage**: optimized to run within free-tier limits of all dependent services.

## Prerequisites

- **Python 3.11+**
- **OpenWeatherMap API Key**: For fetching weather data.
- **SendGrid API Key**: For sending emails.

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/weather-mail.git
cd weather-mail
```

### 2. Configuration

Create a `.env` file in the project root by copying the example:

```bash
cp .env.example .env
```

Edit the `.env` file to include your credentials:

```ini
OPENWEATHER_API_KEY=your_openweather_key
SENDGRID_API_KEY=your_sendgrid_key
RECIPIENT_EMAIL=target@example.com
```

### 3. Install Dependencies

This project uses `uv` for fast dependency management, but can also be installed via standard `pip`.

**Option A: Using the Setup Script (Recommended)**

```bash
./setup.sh
```

**Option B: Manual Installation**

```bash
# Install uv (optional but recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv pip install -e .

# Or using standard pip
pip install -e .
```

## Usage

### Local Execution

To run the system manually on your local machine:

```bash
python main.py
```

### Automated Execution (GitHub Actions)

This repository includes a pre-configured GitHub Actions workflow for daily automation.

1.  Fork this repository.
2.  Navigate to **Settings** > **Secrets and variables** > **Actions**.
3.  Add the following Repository Secrets:
    - `OPENWEATHER_API_KEY`
    - `SENDGRID_API_KEY`
    - `RECIPIENT_EMAIL`
4.  Enable the workflow under the **Actions** tab.
5.  The system is configured to run daily at 6:00 AM UTC. You can modify the schedule in `.github/workflows/daily.yml`.

## Project Structure

```
weather-mail/
├── src/
│   ├── weather.py       # API integration and data analysis
│   ├── visualizer.py    # Chart generation logic
│   ├── emailer.py       # Email construction and delivery
│   └── history.py       # Historical data tracking
├── templates/
│   └── email.html       # HTML email template
├── .github/workflows/
│   └── daily.yml        # Automation configuration
├── main.py              # Application entry point
├── pyproject.toml       # Project metadata and dependencies
└── setup.sh             # Installation script
```

## Customization

### Adding Locations

Modify the `LOCATIONS` list in `src/weather.py` to track different cities:

```python
LOCATIONS = [
    {"name": "New York, NY", "lat": 40.71, "lon": -74.00},
    {"name": "London, UK", "lat": 51.50, "lon": -0.12},
    # Add your desired locations
]
```

### Modifying Schedule

Update the cron schedule in `.github/workflows/daily.yml` to change the execution time:

```yaml
on:
  schedule:
    - cron: '0 8 * * *'  # Runs at 8:00 AM UTC
```

## License

This project is licensed under the MIT License.
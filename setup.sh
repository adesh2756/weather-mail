#!/bin/bash
# Quick setup script for Weather Mail

set -e

echo "🌤️ Weather Mail - Quick Setup"
echo "================================"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

echo "✅ uv is installed"

# Install dependencies
echo "📦 Installing dependencies..."
uv pip install --system -e .

echo "✅ Dependencies installed"

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  No .env file found"
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your API keys:"
    echo "   - OPENWEATHER_API_KEY"
    echo "   - SENDGRID_API_KEY"
    echo "   - RECIPIENT_EMAIL"
    echo ""
    echo "Get API keys from:"
    echo "   - OpenWeather: https://openweathermap.org/api"
    echo "   - SendGrid: https://sendgrid.com"
else
    echo "✅ .env file exists"
fi

echo ""
echo "🎯 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: python test.py (to test)"
echo "3. Run: python main.py (to send email)"
echo ""
echo "For GitHub Actions:"
echo "1. Fork this repository"
echo "2. Add secrets in Settings → Secrets and variables → Actions"
echo "3. Enable workflows in Actions tab"

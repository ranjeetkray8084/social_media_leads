#!/bin/bash
# Fix Python Version for Hostinger Deployment

echo "🔧 Fixing Python version for Hostinger..."

# Use Python 3.11 (available on your server)
echo "🐍 Using Python 3.11..."
python3.11 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
cd backend
pip install -r requirements.txt

# Setup environment
echo "⚙️ Setting up environment..."
cp config.env .env

echo "✅ Python environment setup complete!"
echo "📝 Next steps:"
echo "1. Configure Nginx"
echo "2. Setup Supervisor"
echo "3. Start services"
echo "4. Test deployment"

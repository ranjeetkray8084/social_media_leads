#!/bin/bash
# Complete Hostinger Setup Script

echo "🚀 Starting complete Hostinger setup..."

# Update system
echo "📦 Updating system..."
apt update && apt upgrade -y

# Install Python 3.11 and dependencies
echo "🐍 Installing Python 3.11..."
apt install python3.11 python3.11-venv python3.11-dev python3.11-pip -y

# Install system dependencies
echo "🔧 Installing system dependencies..."
apt install nginx supervisor git curl -y

# Verify Python installation
echo "✅ Verifying Python installation..."
python3.11 --version
pip3.11 --version

# Create project directory
echo "📁 Setting up project directory..."
cd /var/www/social_media_leads

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3.11 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd backend
pip install -r requirements.txt

# Setup environment
echo "⚙️ Setting up environment..."
cp config.env .env

echo "✅ Complete setup finished!"
echo "📝 Next steps:"
echo "1. Configure Nginx (see HOSTINGER_DEPLOYMENT.md)"
echo "2. Setup Supervisor"
echo "3. Start services"
echo "4. Test deployment"
echo ""
echo "🎯 Your project is ready for deployment!"

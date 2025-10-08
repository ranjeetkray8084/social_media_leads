#!/bin/bash
# Quick Deployment Script for Hostinger

echo "Starting Social Media Lead Generator Deployment..."

# Update system
echo "Updating system..."
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
echo "Installing Python..."
sudo apt install python3.10 python3.10-venv python3-pip nginx supervisor git -y

# Create project directory
echo "Creating project directory..."
sudo mkdir -p /var/www/social-media-lead-generator
cd /var/www/social-media-lead-generator

# Setup Python environment
echo "Setting up Python environment..."
python3.10 -m venv venv
source venv/bin/activate

# Install requirements (assuming project files are uploaded)
cd backend
pip install -r requirements.txt

# Setup environment
cp config.env .env

echo "Deployment setup complete!"
echo "Next steps:"
echo "1. Configure Nginx (see HOSTINGER_DEPLOYMENT.md)"
echo "2. Setup Supervisor"
echo "3. Start services"
echo "4. Test deployment"

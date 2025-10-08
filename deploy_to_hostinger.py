#!/usr/bin/env python3
"""
Deployment Script for Hostinger Server
"""

import os
import subprocess
import json

def create_deployment_guide():
    """Create deployment guide for Hostinger"""
    
    deployment_steps = """
🚀 HOSTINGER DEPLOYMENT GUIDE
=====================================

STEP 1: SERVER PREPARATION
--------------------------
1. SSH into your Hostinger server
2. Update system:
   sudo apt update && sudo apt upgrade -y

3. Install Python 3.10:
   sudo apt install python3.10 python3.10-venv python3-pip -y

4. Install required system packages:
   sudo apt install nginx supervisor git -y

STEP 2: UPLOAD PROJECT
----------------------
1. Create project directory:
   mkdir -p /var/www/social-media-lead-generator
   cd /var/www/social-media-lead-generator

2. Upload your project files (use FileZilla or SCP):
   - Upload entire social-media-lead-generator folder
   - Or clone from Git if you have repository

STEP 3: SETUP PYTHON ENVIRONMENT
--------------------------------
1. Create virtual environment:
   python3.10 -m venv venv
   source venv/bin/activate

2. Install dependencies:
   cd backend
   pip install -r requirements.txt

3. Setup environment variables:
   cp config.env .env
   nano .env
   
   Update with your actual values:
   GEMINI_API_KEY=AIzaSyCdHVjOh-TyIR_4ZpYe7hbYRAoBfmkpnK4
   SERVER_PORT=5000
   DEBUG=False

STEP 4: CONFIGURE NGINX
-----------------------
1. Create Nginx configuration:
   sudo nano /etc/nginx/sites-available/social-media-lead-generator

2. Add this configuration:
   server {
       listen 80;
       server_name your-domain.com;  # Replace with your domain
       
       location / {
           root /var/www/social-media-lead-generator/frontend;
           index index.html;
           try_files $uri $uri/ =404;
       }
       
       location /api/ {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }

3. Enable the site:
   sudo ln -s /etc/nginx/sites-available/social-media-lead-generator /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx

STEP 5: CONFIGURE SUPERVISOR
---------------------------
1. Create supervisor configuration:
   sudo nano /etc/supervisor/conf.d/social-media-lead-generator.conf

2. Add this configuration:
   [program:social-media-lead-generator]
   command=/var/www/social-media-lead-generator/venv/bin/python /var/www/social-media-lead-generator/backend/app.py
   directory=/var/www/social-media-lead-generator/backend
   user=www-data
   autostart=true
   autorestart=true
   redirect_stderr=true
   stdout_logfile=/var/log/social-media-lead-generator.log

3. Update supervisor:
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl start social-media-lead-generator

STEP 6: START SERVICES
---------------------
1. Start the application:
   sudo supervisorctl start social-media-lead-generator

2. Check status:
   sudo supervisorctl status social-media-lead-generator

3. Check logs:
   sudo tail -f /var/log/social-media-lead-generator.log

STEP 7: TEST DEPLOYMENT
-----------------------
1. Visit your domain: http://your-domain.com
2. Test API connection
3. Start automatic scanning
4. Monitor for leads

EXPECTED RESULTS AFTER HOSTING:
==============================
✅ Instagram scraping will work better
✅ Facebook scraping will work better
✅ Different IP = less blocking
✅ 24/7 automatic scanning
✅ Professional infrastructure
✅ Better success rate

TROUBLESHOOTING:
===============
1. Check logs: sudo tail -f /var/log/social-media-lead-generator.log
2. Check Nginx: sudo nginx -t
3. Check supervisor: sudo supervisorctl status
4. Check ports: sudo netstat -tlnp | grep :5000

SUPPORT:
========
- Check server resources: htop
- Monitor disk space: df -h
- Check memory: free -h
- Monitor network: ifconfig
"""
    
    print(deployment_steps)
    
    # Save to file
    with open('HOSTINGER_DEPLOYMENT.md', 'w') as f:
        f.write(deployment_steps)
    
    print("\n💾 Deployment guide saved to 'HOSTINGER_DEPLOYMENT.md'")
    print("\n🎯 Ready to deploy to Hostinger!")

def create_quick_deploy_script():
    """Create quick deployment script"""
    
    script_content = """#!/bin/bash
# Quick Deployment Script for Hostinger

echo "🚀 Starting Social Media Lead Generator Deployment..."

# Update system
echo "📦 Updating system..."
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
echo "🐍 Installing Python..."
sudo apt install python3.10 python3.10-venv python3-pip nginx supervisor git -y

# Create project directory
echo "📁 Creating project directory..."
sudo mkdir -p /var/www/social-media-lead-generator
cd /var/www/social-media-lead-generator

# Setup Python environment
echo "🔧 Setting up Python environment..."
python3.10 -m venv venv
source venv/bin/activate

# Install requirements (assuming project files are uploaded)
cd backend
pip install -r requirements.txt

# Setup environment
cp config.env .env

echo "✅ Deployment setup complete!"
echo "📝 Next steps:"
echo "1. Configure Nginx (see HOSTINGER_DEPLOYMENT.md)"
echo "2. Setup Supervisor"
echo "3. Start services"
echo "4. Test deployment"
"""
    
    with open('quick_deploy.sh', 'w') as f:
        f.write(script_content)
    
    print("📜 Quick deploy script created: 'quick_deploy.sh'")

if __name__ == "__main__":
    print("🌐 Creating Hostinger deployment guide...")
    create_deployment_guide()
    create_quick_deploy_script()
    
    print("\n" + "="*60)
    print("🎉 DEPLOYMENT FILES CREATED!")
    print("="*60)
    print("📁 Files created:")
    print("   - HOSTINGER_DEPLOYMENT.md (Complete guide)")
    print("   - quick_deploy.sh (Quick setup script)")
    print("\n🚀 Ready to deploy to Hostinger!")
    print("\n💡 Expected results after hosting:")
    print("   ✅ Better Instagram scraping")
    print("   ✅ Better Facebook scraping")
    print("   ✅ 24/7 automatic scanning")
    print("   ✅ More leads generated")
    print("   ✅ Professional infrastructure")

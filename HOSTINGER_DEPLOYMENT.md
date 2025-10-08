# HOSTINGER DEPLOYMENT GUIDE

## STEP 1: SERVER PREPARATION
--------------------------
1. SSH into your Hostinger server
2. Update system:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

3. Install Python 3.10:
   ```bash
   sudo apt install python3.10 python3.10-venv python3-pip -y
   ```

4. Install required system packages:
   ```bash
   sudo apt install nginx supervisor git -y
   ```

## STEP 2: UPLOAD PROJECT
----------------------
1. Create project directory:
   ```bash
   mkdir -p /var/www/social-media-lead-generator
   cd /var/www/social-media-lead-generator
   ```

2. Upload your project files (use FileZilla or SCP):
   - Upload entire social-media-lead-generator folder
   - Or clone from Git if you have repository

## STEP 3: SETUP PYTHON ENVIRONMENT
--------------------------------
1. Create virtual environment:
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Setup environment variables:
   ```bash
   cp config.env .env
   nano .env
   ```
   
   Update with your actual values:
   ```
   GEMINI_API_KEY=AIzaSyCdHVjOh-TyIR_4ZpYe7hbYRAoBfmkpnK4
   SERVER_PORT=5000
   DEBUG=False
   ```

## STEP 4: CONFIGURE NGINX
-----------------------
1. Create Nginx configuration:
   ```bash
   sudo nano /etc/nginx/sites-available/social-media-lead-generator
   ```

2. Add this configuration:
   ```nginx
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
   ```

3. Enable the site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/social-media-lead-generator /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

## STEP 5: CONFIGURE SUPERVISOR
---------------------------
1. Create supervisor configuration:
   ```bash
   sudo nano /etc/supervisor/conf.d/social-media-lead-generator.conf
   ```

2. Add this configuration:
   ```ini
   [program:social-media-lead-generator]
   command=/var/www/social-media-lead-generator/venv/bin/python /var/www/social-media-lead-generator/backend/app.py
   directory=/var/www/social-media-lead-generator/backend
   user=www-data
   autostart=true
   autorestart=true
   redirect_stderr=true
   stdout_logfile=/var/log/social-media-lead-generator.log
   ```

3. Update supervisor:
   ```bash
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl start social-media-lead-generator
   ```

## STEP 6: START SERVICES
---------------------
1. Start the application:
   ```bash
   sudo supervisorctl start social-media-lead-generator
   ```

2. Check status:
   ```bash
   sudo supervisorctl status social-media-lead-generator
   ```

3. Check logs:
   ```bash
   sudo tail -f /var/log/social-media-lead-generator.log
   ```

## STEP 7: TEST DEPLOYMENT
-----------------------
1. Visit your domain: http://your-domain.com
2. Test API connection
3. Start automatic scanning
4. Monitor for leads

## EXPECTED RESULTS AFTER HOSTING:
==============================
✅ Instagram scraping will work better
✅ Facebook scraping will work better
✅ Different IP = less blocking
✅ 24/7 automatic scanning
✅ Professional infrastructure
✅ Better success rate

## TROUBLESHOOTING:
===============
1. Check logs: `sudo tail -f /var/log/social-media-lead-generator.log`
2. Check Nginx: `sudo nginx -t`
3. Check supervisor: `sudo supervisorctl status`
4. Check ports: `sudo netstat -tlnp | grep :5000`

## SUPPORT:
========
- Check server resources: `htop`
- Monitor disk space: `df -h`
- Check memory: `free -h`
- Monitor network: `ifconfig`

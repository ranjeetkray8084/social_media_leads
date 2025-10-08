"""
Automatic Scanning Scheduler Service
Handles scheduled scraping every 10 minutes
"""

import schedule
import time
import threading
import logging
import requests
import json
from datetime import datetime
import os

class SchedulerService:
    def __init__(self, backend_url="http://localhost:5000"):
        """Initialize scheduler service"""
        self.backend_url = backend_url
        self.is_running = False
        self.scan_interval = 10  # minutes
        self.scheduler_thread = None
        
        # Default configuration
        self.config = {
            'hashtags': ['gurgaonproperty', 'realestate', 'property', 'm3mheights', 'm3mheights65', 'gurugram65', 'm3m65'],
            'facebook_groups': ['gurgaonproperty', 'realestate', 'm3mheights', 'gurugram65', 'm3m65'],
            'youtube_videos': []
        }
        
        logging.info("Scheduler Service initialized")
    
    def set_config(self, hashtags=None, facebook_groups=None, youtube_videos=None):
        """Update configuration for scanning"""
        if hashtags:
            self.config['hashtags'] = hashtags
        if facebook_groups:
            self.config['facebook_groups'] = facebook_groups
        if youtube_videos:
            self.config['youtube_videos'] = youtube_videos
        
        logging.info(f"Configuration updated: {self.config}")
    
    def perform_scan(self):
        """Perform automatic scanning"""
        try:
            logging.info(f"🔄 Starting automatic scan at {datetime.now()}")
            
            total_leads_found = 0
            
            # Instagram scanning
            try:
                logging.info("📱 Scanning Instagram...")
                instagram_response = requests.post(
                    f"{self.backend_url}/api/scrape/instagram",
                    json={"hashtags": self.config['hashtags']},
                    timeout=300  # 5 minutes timeout
                )
                
                if instagram_response.status_code == 200:
                    instagram_data = instagram_response.json()
                    instagram_leads = len(instagram_data.get('leads', []))
                    total_leads_found += instagram_leads
                    logging.info(f"✅ Instagram: Found {instagram_leads} leads")
                else:
                    logging.warning(f"❌ Instagram scanning failed: {instagram_response.status_code}")
                    
            except Exception as e:
                logging.error(f"❌ Instagram scanning error: {e}")
            
            # Facebook scanning
            try:
                logging.info("📘 Scanning Facebook...")
                facebook_response = requests.post(
                    f"{self.backend_url}/api/scrape/facebook",
                    json={"groups": self.config['facebook_groups']},
                    timeout=300  # 5 minutes timeout
                )
                
                if facebook_response.status_code == 200:
                    facebook_data = facebook_response.json()
                    facebook_leads = len(facebook_data.get('leads', []))
                    total_leads_found += facebook_leads
                    logging.info(f"✅ Facebook: Found {facebook_leads} leads")
                else:
                    logging.warning(f"❌ Facebook scanning failed: {facebook_response.status_code}")
                    
            except Exception as e:
                logging.error(f"❌ Facebook scanning error: {e}")
            
            # YouTube scanning (if configured)
            if self.config['youtube_videos']:
                try:
                    logging.info("📺 Scanning YouTube...")
                    youtube_response = requests.post(
                        f"{self.backend_url}/api/scrape/youtube",
                        json={"video_ids": self.config['youtube_videos']},
                        timeout=300  # 5 minutes timeout
                    )
                    
                    if youtube_response.status_code == 200:
                        youtube_data = youtube_response.json()
                        youtube_leads = len(youtube_data.get('leads', []))
                        total_leads_found += youtube_leads
                        logging.info(f"✅ YouTube: Found {youtube_leads} leads")
                    else:
                        logging.warning(f"❌ YouTube scanning failed: {youtube_response.status_code}")
                        
                except Exception as e:
                    logging.error(f"❌ YouTube scanning error: {e}")
            
            logging.info(f"🎉 Scan completed! Total leads found: {total_leads_found}")
            
            # Save scan results
            self.save_scan_results(total_leads_found)
            
        except Exception as e:
            logging.error(f"❌ Scan failed: {e}")
    
    def save_scan_results(self, leads_count):
        """Save scan results to file"""
        try:
            scan_data = {
                'timestamp': datetime.now().isoformat(),
                'leads_found': leads_count,
                'status': 'completed'
            }
            
            # Create logs directory if it doesn't exist
            os.makedirs('../logs', exist_ok=True)
            
            # Append to scan log
            with open('../logs/scan_history.json', 'a') as f:
                f.write(json.dumps(scan_data) + '\n')
                
        except Exception as e:
            logging.error(f"Error saving scan results: {e}")
    
    def start_scheduler(self):
        """Start the automatic scheduler"""
        if self.is_running:
            logging.warning("Scheduler is already running")
            return
        
        try:
            # Schedule the job
            schedule.every(self.scan_interval).minutes.do(self.perform_scan)
            
            # Start scheduler in a separate thread
            self.scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
            self.scheduler_thread.start()
            
            self.is_running = True
            logging.info(f"🚀 Automatic scheduler started! Scanning every {self.scan_interval} minutes")
            
            # Perform initial scan
            logging.info("🔄 Performing initial scan...")
            self.perform_scan()
            
        except Exception as e:
            logging.error(f"Failed to start scheduler: {e}")
    
    def stop_scheduler(self):
        """Stop the automatic scheduler"""
        if not self.is_running:
            logging.warning("Scheduler is not running")
            return
        
        try:
            schedule.clear()
            self.is_running = False
            logging.info("⏹️ Automatic scheduler stopped")
            
        except Exception as e:
            logging.error(f"Failed to stop scheduler: {e}")
    
    def run_scheduler(self):
        """Run the scheduler loop"""
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(1)  # Check every second
            except Exception as e:
                logging.error(f"Scheduler error: {e}")
                time.sleep(5)  # Wait 5 seconds on error
    
    def get_status(self):
        """Get scheduler status"""
        return {
            'is_running': self.is_running,
            'scan_interval': self.scan_interval,
            'next_scan': schedule.next_run() if self.is_running else None,
            'config': self.config
        }
    
    def set_interval(self, minutes):
        """Set scan interval"""
        self.scan_interval = minutes
        if self.is_running:
            self.stop_scheduler()
            self.start_scheduler()
        logging.info(f"Scan interval updated to {minutes} minutes")

# Global scheduler instance
scheduler_service = SchedulerService()

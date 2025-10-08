"""
Facebook Scraping Service
Handles Facebook group and page scraping using Selenium
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random
import logging
from typing import List, Dict
import os

class FacebookService:
    def __init__(self):
        """Initialize Facebook scraper with Selenium"""
        self.driver = None
        self.setup_driver()
        logging.info("Facebook Service initialized")
    
    def setup_driver(self):
        """Setup Chrome driver with anti-detection settings"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # Run in background
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
            
            # Disable images and CSS for faster loading
            prefs = {
                "profile.managed_default_content_settings.images": 2,
                "profile.default_content_setting_values.notifications": 2
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
            
        except Exception as e:
            logging.error(f"Error setting up Chrome driver: {e}")
            self.driver = None
    
    def scrape_groups(self, group_names: List[str]) -> List[Dict]:
        """Scrape posts from Facebook groups"""
        all_posts = []
        
        if not self.driver:
            logging.error("Chrome driver not available")
            return all_posts
        
        for group_name in group_names:
            try:
                logging.info(f"Scraping Facebook group: {group_name}")
                
                # Construct group URL
                group_url = f"https://facebook.com/groups/{group_name}"
                
                posts = self._scrape_group_posts(group_url, group_name)
                all_posts.extend(posts)
                
                # Delay between groups
                time.sleep(random.randint(10, 20))
                
            except Exception as e:
                logging.error(f"Error scraping group {group_name}: {e}")
                continue
        
        logging.info(f"Total Facebook posts scraped: {len(all_posts)}")
        return all_posts
    
    def _scrape_group_posts(self, group_url: str, group_name: str) -> List[Dict]:
        """Scrape posts from a specific Facebook group"""
        posts = []
        
        try:
            self.driver.get(group_url)
            time.sleep(5)
            
            # Scroll to load more posts
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
            
            # Find post elements
            post_selectors = [
                '[data-testid="post"]',
                '.userContent',
                '[role="article"]',
                '.story_body_container'
            ]
            
            post_elements = []
            for selector in post_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        post_elements = elements
                        break
                except:
                    continue
            
            max_posts = 20  # Limit to avoid detection
            count = 0
            
            for post_element in post_elements:
                if count >= max_posts:
                    break
                
                try:
                    post_data = self._extract_post_data(post_element, group_name)
                    if post_data:
                        posts.append(post_data)
                        count += 1
                        
                except Exception as e:
                    logging.error(f"Error extracting post data: {e}")
                    continue
            
            logging.info(f"Scraped {len(posts)} posts from group {group_name}")
            
        except Exception as e:
            logging.error(f"Error scraping group posts from {group_url}: {e}")
        
        return posts
    
    def _extract_post_data(self, post_element, group_name: str) -> Dict:
        """Extract data from a Facebook post element"""
        try:
            # Extract post text
            text_selectors = [
                '[data-testid="post_message"]',
                '.userContent',
                '[data-ad-preview="message"]',
                '.text_exposed_root'
            ]
            
            post_text = ""
            for selector in text_selectors:
                try:
                    text_element = post_element.find_element(By.CSS_SELECTOR, selector)
                    post_text = text_element.text
                    break
                except:
                    continue
            
            if not post_text or len(post_text.strip()) < 10:
                return None
            
            # Extract author information
            author_selectors = [
                '[data-testid="post_chevron_button"]',
                '.fwb a',
                '.profileLink',
                'strong a'
            ]
            
            author_name = "Unknown"
            author_url = ""
            for selector in author_selectors:
                try:
                    author_element = post_element.find_element(By.CSS_SELECTOR, selector)
                    author_name = author_element.text
                    author_url = author_element.get_attribute('href')
                    break
                except:
                    continue
            
            # Extract post URL
            post_url = ""
            try:
                time_element = post_element.find_element(By.CSS_SELECTOR, 'a[href*="/posts/"]')
                post_url = time_element.get_attribute('href')
            except:
                pass
            
            # Extract engagement data
            likes_count = 0
            comments_count = 0
            
            try:
                # Try to extract likes
                likes_elements = post_element.find_elements(By.CSS_SELECTOR, '[aria-label*="like"]')
                if likes_elements:
                    likes_text = likes_elements[0].get_attribute('aria-label')
                    likes_count = self._extract_number_from_text(likes_text)
            except:
                pass
            
            try:
                # Try to extract comments
                comments_elements = post_element.find_elements(By.CSS_SELECTOR, '[aria-label*="comment"]')
                if comments_elements:
                    comments_text = comments_elements[0].get_attribute('aria-label')
                    comments_count = self._extract_number_from_text(comments_text)
            except:
                pass
            
            post_data = {
                'id': f"fb_{hash(post_text)}_{int(time.time())}",
                'text': post_text,
                'author_name': author_name,
                'author_url': author_url,
                'post_url': post_url,
                'group_name': group_name,
                'likes_count': likes_count,
                'comments_count': comments_count,
                'platform': 'facebook',
                'timestamp': time.time(),
                'date': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return post_data
            
        except Exception as e:
            logging.error(f"Error extracting post data: {e}")
            return None
    
    def _extract_number_from_text(self, text: str) -> int:
        """Extract number from text like '5 people like this'"""
        import re
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else 0
    
    def scrape_page_posts(self, page_name: str, max_posts: int = 20) -> List[Dict]:
        """Scrape posts from a Facebook page"""
        posts = []
        
        if not self.driver:
            logging.error("Chrome driver not available")
            return posts
        
        try:
            logging.info(f"Scraping Facebook page: {page_name}")
            
            page_url = f"https://facebook.com/{page_name}"
            self.driver.get(page_url)
            time.sleep(5)
            
            # Scroll to load posts
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
            
            # Find and extract posts
            post_elements = self.driver.find_elements(By.CSS_SELECTOR, '[role="article"]')
            
            count = 0
            for post_element in post_elements:
                if count >= max_posts:
                    break
                
                post_data = self._extract_post_data(post_element, page_name)
                if post_data:
                    posts.append(post_data)
                    count += 1
            
            logging.info(f"Scraped {len(posts)} posts from page {page_name}")
            
        except Exception as e:
            logging.error(f"Error scraping page {page_name}: {e}")
        
        return posts
    
    def search_posts_by_keywords(self, keywords: List[str], max_posts: int = 10) -> List[Dict]:
        """Search Facebook posts by keywords (limited functionality)"""
        posts = []
        
        # Note: Facebook search requires authentication and has strict limits
        # This is a placeholder for future implementation
        logging.warning("Facebook keyword search requires authentication and has strict limits")
        
        return posts
    
    def close(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            logging.info("Facebook scraper driver closed")
    
    def __del__(self):
        """Cleanup on object destruction"""
        self.close()

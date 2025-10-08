"""
Instagram Service - Fixed version without auto-login
"""

import logging
from typing import List, Dict
import instaloader
import time

class InstagramService:
    def __init__(self):
        """Initialize Instagram service"""
        self.loader = None
        logging.info("Instagram Service initialized (no auto-login)")
    
    def scrape_hashtags(self, hashtags: List[str], max_posts: int = 10) -> List[Dict]:
        """Scrape Instagram posts by hashtags without login"""
        try:
            # Initialize loader without login
            self.loader = instaloader.Instaloader()
            
            # Configure to avoid rate limiting
            self.loader.context._session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            posts = []
            
            for hashtag in hashtags:
                try:
                    logging.info(f"Scraping hashtag: #{hashtag}")
                    
                    # Get hashtag posts
                    hashtag_obj = instaloader.Hashtag.from_name(self.loader.context, hashtag)
                    
                    # Get recent posts
                    for post in hashtag_obj.get_posts():
                        if len(posts) >= max_posts:
                            break
                            
                        post_data = {
                            'id': post.shortcode,
                            'shortcode': post.shortcode,
                            'caption': post.caption or '',
                            'owner_username': post.owner_username,
                            'likes': post.likes,
                            'comments': post.comments,
                            'timestamp': post.date.isoformat(),
                            'url': f"https://www.instagram.com/p/{post.shortcode}/",
                            'hashtag': hashtag
                        }
                        
                        posts.append(post_data)
                        logging.info(f"Found post: {post.shortcode}")
                        
                        # Small delay to avoid rate limiting
                        time.sleep(1)
                        
                except Exception as e:
                    logging.warning(f"Error scraping hashtag {hashtag}: {e}")
                    continue
            
            logging.info(f"Scraped {len(posts)} posts from Instagram")
            return posts
            
        except Exception as e:
            logging.error(f"Instagram scraping error: {e}")
            return []
    
    def get_demo_posts(self) -> List[Dict]:
        """Return demo posts when scraping fails"""
        return [
            {
                'id': 'demo1',
                'shortcode': 'demo1',
                'caption': 'Looking for 2BHK apartment in Gurgaon. Budget 50-70L. Please contact if you have any leads. #gurgaonproperty #realestate',
                'owner_username': 'demo_user1',
                'likes': 25,
                'comments': 8,
                'timestamp': '2025-01-08T10:00:00',
                'url': 'https://www.instagram.com/p/demo1/',
                'hashtag': 'gurgaonproperty'
            },
            {
                'id': 'demo2',
                'shortcode': 'demo2',
                'caption': 'Need 3BHK villa in M3M Heights Gurugram. Ready to move in. Contact: 9876543210 #m3mheights #gurugram65',
                'owner_username': 'demo_user2',
                'likes': 45,
                'comments': 12,
                'timestamp': '2025-01-08T09:30:00',
                'url': 'https://www.instagram.com/p/demo2/',
                'hashtag': 'm3mheights'
            }
        ]

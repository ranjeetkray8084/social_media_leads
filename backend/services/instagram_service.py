"""
Instagram Scraping Service
Handles Instagram post scraping using Instaloader
"""

import instaloader
import time
import random
import logging
from typing import List, Dict
import os

class InstagramService:
    def __init__(self):
        """Initialize Instagram scraper"""
        self.loader = instaloader.Instaloader()
        
        # Anti-detection settings
        self.loader.context.request_timeout = 300
        self.loader.context.sleep = True
        
        # Optional: Login with credentials (for better access)
        self.username = os.getenv('INSTAGRAM_USERNAME')
        self.password = os.getenv('INSTAGRAM_PASSWORD')
        
        if self.username and self.password:
            try:
                self.loader.login(self.username, self.password)
                logging.info("Instagram login successful")
            except Exception as e:
                logging.warning(f"Instagram login failed: {e}")
        
        logging.info("Instagram Service initialized")
    
    def scrape_hashtags(self, hashtags: List[str]) -> List[Dict]:
        """Scrape Instagram posts from hashtags"""
        all_posts = []
        
        for hashtag in hashtags:
            try:
                logging.info(f"Scraping Instagram hashtag: #{hashtag}")
                
                # Get hashtag posts
                posts = self.loader.get_hashtag_posts(hashtag)
                
                count = 0
                max_posts_per_hashtag = 50  # Limit to avoid rate limiting
                
                for post in posts:
                    if count >= max_posts_per_hashtag:
                        break
                    
                    try:
                        post_data = {
                            'id': post.mediaid,
                            'shortcode': post.shortcode,
                            'caption': post.caption or '',
                            'likes': post.likes,
                            'comments_count': post.comments,
                            'date': post.date.isoformat(),
                            'url': f"https://instagram.com/p/{post.shortcode}/",
                            'hashtag': hashtag,
                            'username': post.owner_username,
                            'profile_url': f"https://instagram.com/{post.owner_username}/",
                            'is_video': post.is_video,
                            'video_view_count': post.video_view_count if post.is_video else 0,
                            'timestamp': post.date.timestamp()
                        }
                        
                        all_posts.append(post_data)
                        count += 1
                        
                        # Respectful delay to avoid rate limiting
                        time.sleep(random.randint(2, 5))
                        
                    except Exception as e:
                        logging.error(f"Error processing post {post.shortcode}: {e}")
                        continue
                
                logging.info(f"Scraped {count} posts from #{hashtag}")
                
                # Delay between hashtags
                time.sleep(random.randint(5, 10))
                
            except Exception as e:
                logging.error(f"Error scraping hashtag #{hashtag}: {e}")
                continue
        
        logging.info(f"Total Instagram posts scraped: {len(all_posts)}")
        return all_posts
    
    def scrape_user_posts(self, username: str, max_posts: int = 20) -> List[Dict]:
        """Scrape posts from a specific user"""
        try:
            logging.info(f"Scraping posts from user: @{username}")
            
            profile = instaloader.Profile.from_username(self.loader.context, username)
            posts = []
            
            count = 0
            for post in profile.get_posts():
                if count >= max_posts:
                    break
                
                post_data = {
                    'id': post.mediaid,
                    'shortcode': post.shortcode,
                    'caption': post.caption or '',
                    'likes': post.likes,
                    'comments_count': post.comments,
                    'date': post.date.isoformat(),
                    'url': f"https://instagram.com/p/{post.shortcode}/",
                    'username': username,
                    'profile_url': f"https://instagram.com/{username}/",
                    'is_video': post.is_video,
                    'timestamp': post.date.timestamp()
                }
                
                posts.append(post_data)
                count += 1
                
                time.sleep(random.randint(1, 3))
            
            logging.info(f"Scraped {len(posts)} posts from @{username}")
            return posts
            
        except Exception as e:
            logging.error(f"Error scraping user @{username}: {e}")
            return []
    
    def scrape_hashtag_comments(self, hashtag: str, max_posts: int = 10) -> List[Dict]:
        """Scrape comments from hashtag posts"""
        try:
            logging.info(f"Scraping comments from hashtag: #{hashtag}")
            
            posts = self.loader.get_hashtag_posts(hashtag)
            all_comments = []
            
            count = 0
            for post in posts:
                if count >= max_posts:
                    break
                
                try:
                    # Get comments for this post
                    for comment in post.get_comments():
                        comment_data = {
                            'id': comment.id,
                            'text': comment.text,
                            'username': comment.owner.username,
                            'profile_url': f"https://instagram.com/{comment.owner.username}/",
                            'likes': comment.likes_count,
                            'date': comment.created_at_utc.isoformat(),
                            'post_url': f"https://instagram.com/p/{post.shortcode}/",
                            'post_caption': post.caption or '',
                            'hashtag': hashtag,
                            'timestamp': comment.created_at_utc.timestamp()
                        }
                        
                        all_comments.append(comment_data)
                    
                    count += 1
                    time.sleep(random.randint(3, 6))
                    
                except Exception as e:
                    logging.error(f"Error scraping comments from post {post.shortcode}: {e}")
                    continue
            
            logging.info(f"Scraped {len(all_comments)} comments from #{hashtag}")
            return all_comments
            
        except Exception as e:
            logging.error(f"Error scraping comments from hashtag #{hashtag}: {e}")
            return []
    
    def search_posts_by_keywords(self, keywords: List[str]) -> List[Dict]:
        """Search posts by keywords (limited functionality without API)"""
        # Note: Instagram doesn't provide a public search API
        # This is a placeholder for future implementation
        logging.warning("Keyword search not available without Instagram API")
        return []
    
    def get_post_insights(self, post_url: str) -> Dict:
        """Get detailed insights for a specific post"""
        try:
            # Extract shortcode from URL
            shortcode = post_url.split('/p/')[-1].rstrip('/')
            
            post = instaloader.Post.from_shortcode(self.loader.context, shortcode)
            
            insights = {
                'shortcode': post.shortcode,
                'caption': post.caption or '',
                'likes': post.likes,
                'comments_count': post.comments,
                'date': post.date.isoformat(),
                'username': post.owner_username,
                'is_video': post.is_video,
                'video_view_count': post.video_view_count if post.is_video else 0,
                'hashtags': self._extract_hashtags(post.caption or ''),
                'mentions': self._extract_mentions(post.caption or ''),
                'url': f"https://instagram.com/p/{post.shortcode}/"
            }
            
            return insights
            
        except Exception as e:
            logging.error(f"Error getting post insights for {post_url}: {e}")
            return {}
    
    def _extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from text"""
        import re
        hashtags = re.findall(r'#\w+', text)
        return [tag.lower() for tag in hashtags]
    
    def _extract_mentions(self, text: str) -> List[str]:
        """Extract mentions from text"""
        import re
        mentions = re.findall(r'@\w+', text)
        return [mention.lower() for mention in mentions]

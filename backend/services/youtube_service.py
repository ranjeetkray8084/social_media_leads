"""
YouTube Scraping Service
Handles YouTube comments scraping using youtube-comment-downloader
"""

import logging
from typing import List, Dict
import time
import random

try:
    from youtube_comment_downloader import YoutubeCommentDownloader
    YOUTUBE_AVAILABLE = True
except ImportError:
    YOUTUBE_AVAILABLE = False
    logging.warning("youtube-comment-downloader not available. Install with: pip install youtube-comment-downloader")

class YouTubeService:
    def __init__(self):
        """Initialize YouTube scraper"""
        if YOUTUBE_AVAILABLE:
            self.downloader = YoutubeCommentDownloader()
            logging.info("YouTube Service initialized with comment downloader")
        else:
            self.downloader = None
            logging.warning("YouTube Service initialized without comment downloader")
    
    def scrape_comments(self, video_ids: List[str]) -> List[Dict]:
        """Scrape comments from YouTube videos"""
        all_comments = []
        
        if not self.downloader:
            logging.error("YouTube comment downloader not available")
            return all_comments
        
        for video_id in video_ids:
            try:
                logging.info(f"Scraping YouTube comments from video: {video_id}")
                
                # Construct video URL
                if not video_id.startswith('http'):
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                else:
                    video_url = video_id
                
                comments = self._scrape_video_comments(video_url)
                all_comments.extend(comments)
                
                # Delay between videos
                time.sleep(random.randint(5, 10))
                
            except Exception as e:
                logging.error(f"Error scraping video {video_id}: {e}")
                continue
        
        logging.info(f"Total YouTube comments scraped: {len(all_comments)}")
        return all_comments
    
    def _scrape_video_comments(self, video_url: str, max_comments: int = 50) -> List[Dict]:
        """Scrape comments from a specific YouTube video"""
        comments = []
        
        try:
            # Get comments using the downloader
            comments_data = self.downloader.get_comments_from_url(video_url, sort_by=SORT_BY_POPULAR)
            
            count = 0
            for comment_data in comments_data:
                if count >= max_comments:
                    break
                
                try:
                    # Process and structure comment data
                    processed_comment = self._process_comment_data(comment_data, video_url)
                    if processed_comment:
                        comments.append(processed_comment)
                        count += 1
                        
                except Exception as e:
                    logging.error(f"Error processing comment: {e}")
                    continue
            
            logging.info(f"Scraped {len(comments)} comments from video")
            
        except Exception as e:
            logging.error(f"Error scraping comments from {video_url}: {e}")
        
        return comments
    
    def _process_comment_data(self, comment_data: Dict, video_url: str) -> Dict:
        """Process and structure comment data"""
        try:
            # Extract video ID from URL
            video_id = self._extract_video_id(video_url)
            
            # Process comment text
            comment_text = comment_data.get('text', '')
            if not comment_text or len(comment_text.strip()) < 5:
                return None
            
            # Extract author information
            author = comment_data.get('author', 'Unknown')
            author_url = comment_data.get('author_url', '')
            
            # Extract engagement data
            likes = comment_data.get('votes', 0)
            replies = comment_data.get('reply_count', 0)
            
            # Extract timestamp
            time_text = comment_data.get('time', '')
            timestamp = self._parse_time_text(time_text)
            
            processed_comment = {
                'id': f"yt_{hash(comment_text)}_{int(time.time())}",
                'text': comment_text,
                'author': author,
                'author_url': author_url,
                'video_id': video_id,
                'video_url': video_url,
                'likes': likes,
                'replies': replies,
                'time_text': time_text,
                'timestamp': timestamp,
                'date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)),
                'platform': 'youtube'
            }
            
            return processed_comment
            
        except Exception as e:
            logging.error(f"Error processing comment data: {e}")
            return None
    
    def _extract_video_id(self, video_url: str) -> str:
        """Extract video ID from YouTube URL"""
        import re
        
        # Different YouTube URL formats
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
            r'youtube\.com\/embed\/([^&\n?#]+)',
            r'youtube\.com\/v\/([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, video_url)
            if match:
                return match.group(1)
        
        return "unknown"
    
    def _parse_time_text(self, time_text: str) -> float:
        """Parse YouTube time text to timestamp"""
        try:
            import re
            from datetime import datetime, timedelta
            
            now = datetime.now()
            
            # Parse different time formats
            if 'hour' in time_text.lower():
                hours = int(re.search(r'(\d+)', time_text).group(1))
                return (now - timedelta(hours=hours)).timestamp()
            elif 'day' in time_text.lower():
                days = int(re.search(r'(\d+)', time_text).group(1))
                return (now - timedelta(days=days)).timestamp()
            elif 'week' in time_text.lower():
                weeks = int(re.search(r'(\d+)', time_text).group(1))
                return (now - timedelta(weeks=weeks)).timestamp()
            elif 'month' in time_text.lower():
                months = int(re.search(r'(\d+)', time_text).group(1))
                return (now - timedelta(days=months*30)).timestamp()
            elif 'year' in time_text.lower():
                years = int(re.search(r'(\d+)', time_text).group(1))
                return (now - timedelta(days=years*365)).timestamp()
            else:
                return time.time()
                
        except:
            return time.time()
    
    def search_videos_by_keywords(self, keywords: List[str], max_videos: int = 10) -> List[Dict]:
        """Search YouTube videos by keywords"""
        videos = []
        
        # Note: YouTube search requires API key for better results
        # This is a placeholder for future implementation
        logging.warning("YouTube keyword search requires API key for better results")
        
        return videos
    
    def get_video_info(self, video_id: str) -> Dict:
        """Get video information"""
        try:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            # This would require YouTube Data API for detailed info
            # For now, return basic info
            video_info = {
                'video_id': video_id,
                'video_url': video_url,
                'title': 'Unknown',
                'description': 'Unknown',
                'channel': 'Unknown',
                'view_count': 0,
                'like_count': 0,
                'comment_count': 0,
                'published_at': 'Unknown'
            }
            
            return video_info
            
        except Exception as e:
            logging.error(f"Error getting video info for {video_id}: {e}")
            return {}
    
    def scrape_channel_comments(self, channel_url: str, max_comments: int = 50) -> List[Dict]:
        """Scrape comments from a YouTube channel's recent videos"""
        comments = []
        
        # Note: This would require getting recent videos first
        # Then scraping comments from each video
        logging.warning("Channel comment scraping requires getting recent videos first")
        
        return comments

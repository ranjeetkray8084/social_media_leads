"""
Gemini Pro API Service
Handles all AI operations using Google's Gemini Pro API
"""

import google.generativeai as genai
import json
import logging
import os
from typing import List, Dict, Any

class GeminiService:
    def __init__(self):
        """Initialize Gemini Pro API"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-001')
        
        logging.info("Gemini Service initialized successfully")
    
    def test_api(self, text: str) -> str:
        """Test Gemini API with a simple prompt"""
        try:
            prompt = f"Analyze this text and provide a brief response: {text}"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Gemini API test failed: {e}")
            raise
    
    def analyze_posts_for_leads(self, posts: List[Dict]) -> List[Dict]:
        """Analyze social media posts to identify potential leads"""
        leads = []
        
        for post in posts:
            try:
                # Extract text content
                content = post.get('caption', '') or post.get('text', '') or post.get('message', '')
                
                if not content or len(content.strip()) < 10:
                    continue
                
                # Analyze with Gemini
                lead_analysis = self._analyze_lead_intent(content, post)
                
                if lead_analysis and lead_analysis.get('is_lead', False):
                    lead_data = self._extract_lead_info(content, post, lead_analysis)
                    leads.append(lead_data)
                    
            except Exception as e:
                logging.error(f"Error analyzing post: {e}")
                continue
        
        logging.info(f"Analyzed {len(posts)} posts, found {len(leads)} potential leads")
        return leads
    
    def analyze_comments_for_leads(self, comments: List[Dict]) -> List[Dict]:
        """Analyze YouTube comments to identify potential leads"""
        leads = []
        
        for comment in comments:
            try:
                content = comment.get('text', '') or comment.get('content', '')
                
                if not content or len(content.strip()) < 5:
                    continue
                
                # Analyze with Gemini
                lead_analysis = self._analyze_lead_intent(content, comment)
                
                if lead_analysis and lead_analysis.get('is_lead', False):
                    lead_data = self._extract_lead_info(content, comment, lead_analysis)
                    leads.append(lead_data)
                    
            except Exception as e:
                logging.error(f"Error analyzing comment: {e}")
                continue
        
        logging.info(f"Analyzed {len(comments)} comments, found {len(leads)} potential leads")
        return leads
    
    def _analyze_lead_intent(self, content: str, source_data: Dict) -> Dict:
        """Analyze content for lead intent using Gemini Pro"""
        try:
            prompt = f"""
            You are a real estate lead qualification expert. Analyze this social media content for lead intent:
            
            Content: "{content}"
            
            PRIORITY: Focus on HIGH-INTENT leads with direct contact information or clear buying signals.
            
            Determine:
            1. Is this person actively looking for property? (Yes/No)
            2. What type of property? (1BHK, 2BHK, 3BHK, Villa, Commercial, etc.)
            3. Location preference? (Gurgaon, Delhi, Mumbai, etc.)
            4. Budget range? (if mentioned)
            5. Timeline? (urgent, within month, etc.)
            6. Contact information? (phone, email, WhatsApp if visible)
            7. Lead score (1-10, where 10 is highest intent - PRIORITIZE contacts with phone/email)
            8. Language used (Hindi/English/Both)
            9. Buying intent level (High/Medium/Low)
            10. Contact method mentioned (Call, DM, WhatsApp, Email)
            
            IMPORTANT: Only mark as lead if:
            - Direct contact info is present (phone/email)
            - Clear buying intent ("looking for", "need", "want to buy")
            - Specific requirements mentioned
            - Timeline is mentioned ("urgent", "immediately", "this month")
            
            Respond in JSON format:
            {{
                "is_lead": true/false,
                "property_type": "2BHK",
                "location": "Gurgaon",
                "budget_range": "50L-70L",
                "timeline": "within_month",
                "contact_available": true/false,
                "contact_method": "phone/email/whatsapp/dm",
                "buying_intent": "High/Medium/Low",
                "lead_score": 8,
                "language": "English",
                "confidence": 0.85
            }}
            """
            
            response = self.model.generate_content(prompt)
            result = self._parse_gemini_response(response.text)
            
            # Validate result - prioritize leads with contact info
            is_lead = result.get('is_lead', False)
            lead_score = result.get('lead_score', 0)
            contact_available = result.get('contact_available', False)
            buying_intent = result.get('buying_intent', 'Low')
            
            # Higher priority for leads with contact info
            if is_lead and contact_available and lead_score >= 6:
                return result
            elif is_lead and buying_intent == 'High' and lead_score >= 7:
                return result
            elif is_lead and lead_score >= 8:
                return result
            else:
                return None
                
        except Exception as e:
            logging.error(f"Error in lead intent analysis: {e}")
            return None
    
    def _extract_lead_info(self, content: str, source_data: Dict, analysis: Dict) -> Dict:
        """Extract structured lead information"""
        try:
            # Extract contact information
            contact_info = self._extract_contact_info(content)
            
            # Determine source platform
            platform = self._determine_platform(source_data)
            
            # Create lead data
            lead_data = {
                'name': contact_info.get('name', 'Unknown'),
                'phone': contact_info.get('phone', ''),
                'email': contact_info.get('email', ''),
                'whatsapp': contact_info.get('whatsapp', ''),
                'social_handle': contact_info.get('social_handle', ''),
                'contact_phrase': contact_info.get('contact_phrase', ''),
                'requirement': analysis.get('property_type', ''),
                'location': analysis.get('location', ''),
                'budget': analysis.get('budget_range', ''),
                'timeline': analysis.get('timeline', ''),
                'contact_method': analysis.get('contact_method', ''),
                'buying_intent': analysis.get('buying_intent', 'Medium'),
                'source': platform.upper(),
                'lead_score': analysis.get('lead_score', 5),
                'original_content': content,
                'post_url': self._generate_post_url(source_data, platform),
                'social_media_url': source_data.get('url', ''),
                'username': source_data.get('username', ''),
                'language': analysis.get('language', 'English'),
                'confidence': analysis.get('confidence', 0.5),
                'extracted_at': self._get_current_timestamp(),
                'status': 'NEW',
                'action': 'CONTACT' if (contact_info.get('phone') or contact_info.get('email')) else 'FOLLOW_UP'
            }
            
            return lead_data
            
        except Exception as e:
            logging.error(f"Error extracting lead info: {e}")
            return None
    
    def _extract_contact_info(self, content: str) -> Dict:
        """Extract contact information from content"""
        try:
            prompt = f"""
            Extract ALL possible contact information from this text:
            
            "{content}"
            
            AGGRESSIVELY search for:
            1. Name (any name mentioned)
            2. Phone number (any format: 9876543210, +91-9876543210, 98765-43210, etc.)
            3. Email address (any format)
            4. WhatsApp number (any format)
            5. Social media handles (@username)
            6. Contact phrases ("call me", "DM me", "contact me", "reach out")
            
            IMPORTANT: 
            - Look for Indian phone numbers (starting with 6,7,8,9)
            - Look for email patterns (contains @ and .)
            - Look for WhatsApp mentions
            - Extract even partial contact info
            
            Respond in JSON format:
            {{
                "name": "extracted name or null",
                "phone": "extracted phone or null", 
                "email": "extracted email or null",
                "whatsapp": "extracted whatsapp or null",
                "social_handle": "extracted social handle or null",
                "contact_phrase": "extracted contact phrase or null"
            }}
            """
            
            response = self.model.generate_content(prompt)
            return self._parse_gemini_response(response.text)
            
        except Exception as e:
            logging.error(f"Error extracting contact info: {e}")
            return {
                'name': None, 
                'phone': None, 
                'email': None,
                'whatsapp': None,
                'social_handle': None,
                'contact_phrase': None
            }
    
    def _determine_platform(self, source_data: Dict) -> str:
        """Determine the source platform"""
        if 'instagram' in str(source_data).lower() or 'shortcode' in source_data:
            return 'instagram'
        elif 'facebook' in str(source_data).lower() or 'group' in source_data:
            return 'facebook'
        elif 'youtube' in str(source_data).lower() or 'video' in source_data:
            return 'youtube'
        else:
            return 'unknown'
    
    def analyze_lead_quality(self, leads: List[Dict]) -> List[Dict]:
        """Analyze lead quality and provide scoring"""
        analyzed_leads = []
        
        for lead in leads:
            try:
                prompt = f"""
                Analyze this lead data for quality and priority:
                
                Lead Data: {json.dumps(lead, indent=2)}
                
                Provide:
                1. Quality score (1-10)
                2. Priority level (High/Medium/Low)
                3. Recommended next action
                4. Risk factors
                5. Opportunity assessment
                
                Respond in JSON format:
                {{
                    "quality_score": 8,
                    "priority": "High",
                    "recommended_action": "Call immediately",
                    "risk_factors": ["No phone number"],
                    "opportunity_assessment": "Strong intent, ready to buy",
                    "follow_up_suggestion": "Send property recommendations"
                }}
                """
                
                response = self.model.generate_content(prompt)
                analysis = self._parse_gemini_response(response.text)
                
                # Add analysis to lead
                lead_with_analysis = lead.copy()
                lead_with_analysis.update(analysis)
                analyzed_leads.append(lead_with_analysis)
                
            except Exception as e:
                logging.error(f"Error analyzing lead quality: {e}")
                analyzed_leads.append(lead)
        
        return analyzed_leads
    
    def _parse_gemini_response(self, response_text: str) -> dict:
        """Parse Gemini response to extract structured data"""
        try:
            import re
            
            # Clean the response text
            cleaned_text = response_text.strip()
            
            # Try to extract JSON from markdown code blocks first
            json_match = re.search(r'```json\s*(.*?)\s*```', cleaned_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass
            
            # Try to find JSON without markdown
            json_match = re.search(r'\{.*\}', cleaned_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except json.JSONDecodeError:
                    pass
            
            # Try to parse the entire response as JSON
            return json.loads(cleaned_text)
            
        except json.JSONDecodeError:
            # Fallback: return basic structure based on content analysis
            return {
                "has_lead_intent": any(word in response_text.lower() for word in ["looking", "contact", "buy", "sell", "rent", "property", "apartment", "house"]),
                "confidence": 0.5,
                "extracted_info": {
                    "property_type": "unknown",
                    "location": "unknown", 
                    "budget": "unknown",
                    "contact": "unknown"
                }
            }
    
    def _generate_post_url(self, source_data: Dict, platform: str) -> str:
        """Generate direct URL to the social media post"""
        try:
            if platform.lower() == 'instagram':
                shortcode = source_data.get('shortcode', '')
                if shortcode:
                    return f"https://www.instagram.com/p/{shortcode}/"
                
            elif platform.lower() == 'facebook':
                post_id = source_data.get('post_id', '')
                group_id = source_data.get('group_id', '')
                if post_id and group_id:
                    return f"https://www.facebook.com/groups/{group_id}/posts/{post_id}/"
                elif post_id:
                    return f"https://www.facebook.com/posts/{post_id}/"
                    
            elif platform.lower() == 'youtube':
                video_id = source_data.get('video_id', '')
                comment_id = source_data.get('comment_id', '')
                if video_id and comment_id:
                    return f"https://www.youtube.com/watch?v={video_id}&lc={comment_id}"
                elif video_id:
                    return f"https://www.youtube.com/watch?v={video_id}"
            
            # Fallback to original URL
            return source_data.get('url', '')
            
        except Exception as e:
            logging.error(f"Error generating post URL: {e}")
            return source_data.get('url', '')
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

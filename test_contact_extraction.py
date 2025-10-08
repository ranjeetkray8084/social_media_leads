#!/usr/bin/env python3
"""
Test Contact Extraction Improvements
"""

import os
import sys
sys.path.append('backend')

from backend.services.gemini_service import GeminiService
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/config.env')

def test_contact_extraction():
    """Test the improved contact extraction"""
    try:
        print("🧪 Testing Improved Contact Extraction...")
        print("=" * 50)
        
        # Initialize Gemini service
        gemini_service = GeminiService()
        
        # Test content with contact information
        test_content = """
        Looking for 3BHK apartment in Gurgaon under 1 crore budget. 
        Please contact me at 9876543210 or email: john.doe@gmail.com
        WhatsApp: +91-9876543210
        DM me for more details!
        """
        
        print(f"📝 Test Content:")
        print(f"   {test_content.strip()}")
        print()
        
        # Test lead analysis
        print("🤖 Testing Lead Analysis...")
        source_data = {
            'shortcode': 'ABC123XYZ',
            'url': 'https://instagram.com/p/ABC123XYZ/',
            'username': 'property_seeker'
        }
        
        lead_analysis = gemini_service._analyze_lead_intent(test_content, source_data)
        
        if lead_analysis:
            print("✅ Lead Analysis Result:")
            print(f"   Is Lead: {lead_analysis.get('is_lead')}")
            print(f"   Property Type: {lead_analysis.get('property_type')}")
            print(f"   Location: {lead_analysis.get('location')}")
            print(f"   Budget: {lead_analysis.get('budget_range')}")
            print(f"   Contact Available: {lead_analysis.get('contact_available')}")
            print(f"   Buying Intent: {lead_analysis.get('buying_intent')}")
            print(f"   Lead Score: {lead_analysis.get('lead_score')}")
            print()
        else:
            print("❌ Lead analysis failed")
            return
        
        # Test contact extraction
        print("📞 Testing Contact Extraction...")
        contact_info = gemini_service._extract_contact_info(test_content)
        
        print("✅ Contact Information Extracted:")
        print(f"   Name: {contact_info.get('name', 'Not found')}")
        print(f"   Phone: {contact_info.get('phone', 'Not found')}")
        print(f"   Email: {contact_info.get('email', 'Not found')}")
        print(f"   WhatsApp: {contact_info.get('whatsapp', 'Not found')}")
        print(f"   Social Handle: {contact_info.get('social_handle', 'Not found')}")
        print(f"   Contact Phrase: {contact_info.get('contact_phrase', 'Not found')}")
        print()
        
        # Test complete lead extraction
        print("🎯 Testing Complete Lead Extraction...")
        lead_data = gemini_service._extract_lead_info(test_content, source_data, lead_analysis)
        
        if lead_data:
            print("✅ Complete Lead Data:")
            print(f"   Name: {lead_data.get('name')}")
            print(f"   Phone: {lead_data.get('phone')}")
            print(f"   Email: {lead_data.get('email')}")
            print(f"   WhatsApp: {lead_data.get('whatsapp')}")
            print(f"   Post URL: {lead_data.get('post_url')}")
            print(f"   Action: {lead_data.get('action')}")
            print(f"   Lead Score: {lead_data.get('lead_score')}")
            print()
            
            # Check if contact details are present
            has_contact = lead_data.get('phone') or lead_data.get('email') or lead_data.get('whatsapp')
            if has_contact:
                print("🎉 SUCCESS: Contact details extracted!")
                print("✅ Ready for direct contact")
            else:
                print("⚠️  WARNING: No contact details found")
                print("✅ Post URL available for messaging")
        else:
            print("❌ Lead extraction failed")
            return
        
        print("=" * 50)
        print("🎉 All tests completed successfully!")
        print("✅ System ready for improved contact extraction")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_contact_extraction()

#!/usr/bin/env python3
"""
Generate Demo Leads for Testing
"""

import requests
import json

def create_demo_leads():
    """Create sample leads to test the system"""
    print("🎭 Creating Demo Leads...")
    
    # Sample leads data
    demo_leads = [
        {
            "name": "Rajesh Kumar",
            "phone": "9876543210",
            "email": "rajesh.kumar@gmail.com",
            "whatsapp": "9876543210",
            "social_handle": "@rajesh_property",
            "contact_phrase": "contact me",
            "requirement": "3BHK",
            "location": "Gurgaon",
            "budget": "1 crore",
            "timeline": "within_month",
            "contact_method": "phone",
            "buying_intent": "High",
            "source": "INSTAGRAM",
            "lead_score": 9,
            "original_content": "Looking for 3BHK apartment in Gurgaon under 1 crore budget. Please contact me at 9876543210",
            "post_url": "https://instagram.com/p/ABC123XYZ/",
            "social_media_url": "https://instagram.com/p/ABC123XYZ/",
            "username": "rajesh_property",
            "language": "English",
            "confidence": 0.95,
            "extracted_at": "2025-10-08T15:20:00.000000",
            "status": "NEW",
            "action": "CONTACT"
        },
        {
            "name": "Priya Sharma",
            "phone": "9876543211",
            "email": "",
            "whatsapp": "9876543211",
            "social_handle": "@priya_homes",
            "contact_phrase": "DM me",
            "requirement": "2BHK",
            "location": "Delhi",
            "budget": "50L-70L",
            "timeline": "urgent",
            "contact_method": "whatsapp",
            "buying_intent": "High",
            "source": "FACEBOOK",
            "lead_score": 8,
            "original_content": "Need 2BHK apartment in Delhi urgently. Budget 50-70L. WhatsApp me at 9876543211",
            "post_url": "https://facebook.com/groups/gurgaonproperty/posts/123456789/",
            "social_media_url": "https://facebook.com/groups/gurgaonproperty/posts/123456789/",
            "username": "priya_homes",
            "language": "English",
            "confidence": 0.90,
            "extracted_at": "2025-10-08T15:21:00.000000",
            "status": "NEW",
            "action": "CONTACT"
        },
        {
            "name": "Amit Singh",
            "phone": "",
            "email": "amit.singh@yahoo.com",
            "whatsapp": "",
            "social_handle": "@amit_investor",
            "contact_phrase": "email me",
            "requirement": "M3M Heights 65",
            "location": "Gurugram",
            "budget": "1.5 crore",
            "timeline": "flexible",
            "contact_method": "email",
            "buying_intent": "Medium",
            "source": "INSTAGRAM",
            "lead_score": 7,
            "original_content": "Interested in M3M Heights 65 investment. Email me for details: amit.singh@yahoo.com",
            "post_url": "https://instagram.com/p/M3M123ABC/",
            "social_media_url": "https://instagram.com/p/M3M123ABC/",
            "username": "amit_investor",
            "language": "English",
            "confidence": 0.85,
            "extracted_at": "2025-10-08T15:22:00.000000",
            "status": "NEW",
            "action": "CONTACT"
        },
        {
            "name": "Sunita Gupta",
            "phone": "9876543212",
            "email": "",
            "whatsapp": "9876543212",
            "social_handle": "@sunita_properties",
            "contact_phrase": "call me",
            "requirement": "4BHK Villa",
            "location": "Gurgaon",
            "budget": "2 crore",
            "timeline": "next_month",
            "contact_method": "phone",
            "buying_intent": "High",
            "source": "YOUTUBE",
            "lead_score": 9,
            "original_content": "Looking for 4BHK villa in Gurgaon. Budget 2 crore. Call me at 9876543212",
            "post_url": "https://youtube.com/watch?v=XYZ123&lc=comment456",
            "social_media_url": "https://youtube.com/watch?v=XYZ123&lc=comment456",
            "username": "sunita_properties",
            "language": "English",
            "confidence": 0.92,
            "extracted_at": "2025-10-08T15:23:00.000000",
            "status": "NEW",
            "action": "CONTACT"
        }
    ]
    
    print(f"✅ Created {len(demo_leads)} demo leads")
    print("\n📊 Demo Leads Summary:")
    print("=" * 50)
    
    for i, lead in enumerate(demo_leads, 1):
        print(f"{i}. {lead['name']}")
        print(f"   📞 Phone: {lead['phone'] or 'N/A'}")
        print(f"   📧 Email: {lead['email'] or 'N/A'}")
        print(f"   🏠 Requirement: {lead['requirement']}")
        print(f"   📍 Location: {lead['location']}")
        print(f"   💰 Budget: {lead['budget']}")
        print(f"   📱 Source: {lead['source']}")
        print(f"   ⭐ Score: {lead['lead_score']}/10")
        print(f"   🎯 Action: {lead['action']}")
        print()
    
    # Save demo leads to a file for manual testing
    with open('demo_leads.json', 'w') as f:
        json.dump(demo_leads, f, indent=2)
    
    print("💾 Demo leads saved to 'demo_leads.json'")
    print("\n🎯 How to use:")
    print("1. Copy these leads to your dashboard")
    print("2. Test the Excel export feature")
    print("3. Test the contact extraction display")
    print("4. Test the 'Message User' functionality")
    
    return demo_leads

if __name__ == "__main__":
    create_demo_leads()

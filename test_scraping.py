#!/usr/bin/env python3
"""
Test Scraping Functionality
"""

import requests
import json
import time

def test_scraping_api():
    """Test the scraping API endpoints"""
    print("🧪 Testing Scraping API...")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test 1: Health check
    print("1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend is responding")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return
    
    print()
    
    # Test 2: Test Connection
    print("2️⃣ Testing Gemini API Connection...")
    try:
        response = requests.get(f"{base_url}/api/test", timeout=30)
        if response.status_code == 200:
            print("✅ Gemini API is working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Gemini test failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Gemini test error: {e}")
    
    print()
    
    # Test 3: Simple Instagram scraping test
    print("3️⃣ Testing Instagram Scraping...")
    try:
        payload = {
            "hashtags": ["gurgaon"]  # Simple hashtag for test
        }
        
        print("   Sending scraping request...")
        response = requests.post(
            f"{base_url}/api/scrape/instagram", 
            json=payload, 
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Instagram scraping completed")
            print(f"   Success: {data.get('success')}")
            print(f"   Leads found: {len(data.get('leads', []))}")
            
            if data.get('leads'):
                print("   Sample lead:")
                lead = data['leads'][0]
                print(f"     - Source: {lead.get('source')}")
                print(f"     - Phone: {lead.get('phone', 'No phone')}")
                print(f"     - Requirement: {lead.get('requirement', 'No requirement')}")
            else:
                print("   No leads found in this test")
                
        else:
            print(f"❌ Instagram scraping failed: {response.status_code}")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Instagram scraping error: {e}")
    
    print()
    print("=" * 50)
    print("🎯 Test completed!")

if __name__ == "__main__":
    test_scraping_api()

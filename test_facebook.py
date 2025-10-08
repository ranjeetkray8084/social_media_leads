#!/usr/bin/env python3
"""
Test Facebook Scraping
"""

import requests
import json

def test_facebook():
    """Test Facebook scraping"""
    print("🧪 Testing Facebook Scraping...")
    
    try:
        payload = {
            "groups": ["gurgaonproperty", "realestate"]
        }
        
        print("Sending Facebook scraping request...")
        response = requests.post(
            "http://localhost:5000/api/scrape/facebook",
            json=payload,
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Leads: {len(data.get('leads', []))}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_facebook()

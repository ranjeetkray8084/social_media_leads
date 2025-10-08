#!/usr/bin/env python3
"""
Simple Instagram Test
"""

import requests
import json

def simple_test():
    """Simple test of Instagram scraping"""
    print("🧪 Simple Instagram Test...")
    
    try:
        # Test with a very simple hashtag
        payload = {
            "hashtags": ["gurgaon"]
        }
        
        print("Sending request to Instagram API...")
        response = requests.post(
            "http://localhost:5000/api/scrape/instagram",
            json=payload,
            timeout=30
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
    simple_test()
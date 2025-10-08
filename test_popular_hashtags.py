#!/usr/bin/env python3
"""
Test Popular Hashtags
"""

import requests
import json

def test_popular_hashtags():
    """Test with more popular hashtags"""
    print("🧪 Testing Popular Hashtags...")
    
    # Try different popular hashtags
    hashtag_sets = [
        ["gurgaon"],
        ["delhi"],
        ["property"],
        ["realestate"],
        ["investment"],
        ["home"],
        ["apartment"]
    ]
    
    for hashtags in hashtag_sets:
        print(f"\n📱 Testing hashtags: {hashtags}")
        
        try:
            payload = {"hashtags": hashtags}
            
            response = requests.post(
                "http://localhost:5000/api/scrape/instagram",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success: {data.get('success')}")
                print(f"   📊 Total found: {data.get('total_found', 0)}")
                print(f"   🎯 Leads: {len(data.get('leads', []))}")
                
                if data.get('total_found', 0) > 0:
                    print(f"   🎉 FOUND POSTS! This hashtag works!")
                    break
                else:
                    print(f"   ⚠️  No posts found")
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    print("\n" + "="*50)
    print("🎯 Test completed!")

if __name__ == "__main__":
    test_popular_hashtags()

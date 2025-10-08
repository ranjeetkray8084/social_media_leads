#!/usr/bin/env python3
"""
Check available Gemini models
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/config.env')

def check_available_models():
    """Check which Gemini models are available"""
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        return
    
    print(f"🔑 Using API Key: {api_key[:10]}...")
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # List all models
        print("\n📋 Available Models:")
        print("=" * 50)
        
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"✅ {model.name}")
                print(f"   Display Name: {model.display_name}")
                print(f"   Description: {model.description}")
                print()
        
        # Test with a simple model
        print("\n🧪 Testing model generation...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Hello, can you respond with 'API working'?")
        print(f"✅ Response: {response.text}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_available_models()

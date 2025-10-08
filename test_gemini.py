#!/usr/bin/env python3
"""
Test script for Gemini API integration
Run this to verify your Gemini API key is working
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add backend to path
sys.path.append('backend')

def test_gemini_api():
    """Test Gemini API connection"""
    print("🤖 Testing Gemini API Integration...")
    print("="*50)
    
    # Load environment variables
    load_dotenv('backend/config.env')
    
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("📝 Please add your Gemini API key to backend/config.env:")
        print("   GEMINI_API_KEY=your_actual_api_key_here")
        return False
    
    if api_key == 'your_gemini_api_key_here':
        print("❌ Please replace the placeholder with your actual Gemini API key")
        print("📝 Edit backend/config.env and update GEMINI_API_KEY")
        return False
    
    try:
        # Test Gemini service
        from backend.services.gemini_service import GeminiService
        
        print("✅ Gemini service imported successfully")
        
        # Initialize service
        gemini_service = GeminiService()
        print("✅ Gemini service initialized")
        
        # Test API call
        test_text = "I am looking for a 3BHK apartment in Gurgaon under 1 crore budget. Please contact me at 9876543210."
        
        print(f"\n🧪 Testing with sample text:")
        print(f"'{test_text}'")
        
        # Test lead analysis
        result = gemini_service._analyze_lead_intent(test_text, {})
        
        if result:
            print("\n✅ Gemini API is working correctly!")
            print("📊 Analysis Result:")
            print(json.dumps(result, indent=2))
            
            # Test lead extraction
            lead_data = gemini_service._extract_lead_info(test_text, {}, result)
            
            if lead_data:
                print("\n✅ Lead extraction working!")
                print("👤 Extracted Lead Data:")
                print(json.dumps(lead_data, indent=2))
            
            return True
        else:
            print("❌ Gemini API test failed - no result returned")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("📝 Make sure you're in the project root directory")
        return False
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        return False

def test_excel_service():
    """Test Excel service"""
    print("\n📊 Testing Excel Service...")
    print("="*30)
    
    try:
        from backend.utils.excel_service import ExcelService
        
        excel_service = ExcelService()
        print("✅ Excel service initialized")
        
        # Test with sample data
        sample_leads = [
            {
                'name': 'John Doe',
                'phone': '9876543210',
                'email': 'john@example.com',
                'requirement': '3BHK Apartment',
                'location': 'Gurgaon',
                'budget': '1 Crore',
                'source': 'INSTAGRAM',
                'lead_score': 8,
                'original_content': 'Looking for 3BHK in Gurgaon',
                'extracted_at': '2024-01-01T12:00:00'
            },
            {
                'name': 'Jane Smith',
                'phone': '9876543211',
                'email': 'jane@example.com',
                'requirement': '2BHK Flat',
                'location': 'Delhi',
                'budget': '50 Lakhs',
                'source': 'FACEBOOK',
                'lead_score': 7,
                'original_content': 'Need 2BHK flat in Delhi',
                'extracted_at': '2024-01-01T12:05:00'
            }
        ]
        
        # Test Excel export
        filepath = excel_service.export_leads_to_excel(sample_leads, 'test_leads')
        
        if filepath:
            print(f"✅ Excel export successful: {filepath}")
            
            # Test summary sheet
            excel_service.create_summary_sheet(sample_leads, filepath)
            print("✅ Summary sheet created")
            
            return True
        else:
            print("❌ Excel export failed")
            return False
            
    except Exception as e:
        print(f"❌ Excel service test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Social Media Lead Generator - Test Suite")
    print("="*60)
    
    # Test Gemini API
    gemini_success = test_gemini_api()
    
    # Test Excel service
    excel_success = test_excel_service()
    
    print("\n" + "="*60)
    print("📋 TEST RESULTS:")
    print(f"Gemini API: {'✅ PASS' if gemini_success else '❌ FAIL'}")
    print(f"Excel Service: {'✅ PASS' if excel_success else '❌ FAIL'}")
    
    if gemini_success and excel_success:
        print("\n🎉 All tests passed! Your system is ready to generate leads.")
        print("\n📋 Next steps:")
        print("1. Start the backend server: cd backend && python app.py")
        print("2. Start the frontend: cd frontend && python -m http.server 3000")
        print("3. Open browser: http://localhost:3000")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        
        if not gemini_success:
            print("\n🔧 Gemini API Setup:")
            print("1. Get API key from: https://makersuite.google.com/app/apikey")
            print("2. Add to backend/config.env: GEMINI_API_KEY=your_key")
        
        if not excel_success:
            print("\n🔧 Excel Service Setup:")
            print("1. Install dependencies: pip install openpyxl pandas")
            print("2. Check file permissions in data/exports directory")

if __name__ == "__main__":
    main()

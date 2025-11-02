#!/usr/bin/env python3
"""
Test script to verify Gemini API key is properly configured
"""
import os
from google import genai

def test_gemini_api():
    print("🔍 Checking Gemini API configuration...\n")
    
    # Check if API key exists
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment!")
        print("\n📝 To fix this:")
        print("   1. Go to Replit Secrets (🔒 icon in the sidebar)")
        print("   2. Add a new secret:")
        print("      Key: GEMINI_API_KEY")
        print("      Value: Your API key from https://aistudio.google.com/app/apikey")
        print("   3. Restart this script")
        return False
    
    print(f"✅ GEMINI_API_KEY found! (length: {len(api_key)} characters)")
    
    # Test API connection
    print("\n🔄 Testing API connection...")
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Say hello in one sentence!"
        )
        
        print("✅ API connection successful!")
        print(f"\n🤖 Test response: {response.text}")
        print("\n🎉 Gemini API is working perfectly!")
        return True
        
    except Exception as e:
        print(f"❌ API connection failed: {str(e)}")
        print("\n📝 Please check:")
        print("   • Your API key is valid")
        print("   • You have credits/quota available")
        print("   • Your API key is from Google AI Studio (not Vertex AI)")
        return False

if __name__ == "__main__":
    test_gemini_api()

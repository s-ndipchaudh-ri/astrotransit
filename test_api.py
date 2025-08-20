#!/usr/bin/env python3
"""
Test script for AstroCSV FastAPI backend.
"""

import requests
import json
import time

def test_api():
    """Test the FastAPI endpoints."""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing AstroCSV API...")
    print("=" * 40)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Is it running?")
        print("   Start with: python start_api.py")
        return False
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"   Available endpoints: {list(response.json()['endpoints'].keys())}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test calculation endpoint
    test_data = {
        "latitude": 19.0760,
        "longitude": 72.8777,
        "date": "2025-08-20",
        "include_degree_buckets": True
    }
    
    try:
        response = requests.post(
            f"{base_url}/calculate",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("✅ Calculation endpoint working")
            result = response.json()
            print(f"   Ascendant: {result['ascendant']}° ({result['ascendant_sign']})")
            print(f"   Nakshatra: {result['ascendant_nakshatra']} ({result['ascendant_nakshatra_lord']})")
            print(f"   KP: {result['ascendant_sub_lord']} - {result['ascendant_sub_sub_lord']}")
            if result.get('degree_buckets'):
                print(f"   Degree buckets: {len(result['degree_buckets'])} rows")
        else:
            print(f"❌ Calculation endpoint failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Calculation endpoint error: {e}")
    
    # Test other endpoints
    endpoints = ["/signs", "/nakshatras", "/degree-buckets"]
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            if response.status_code == 200:
                print(f"✅ {endpoint} endpoint working")
            else:
                print(f"❌ {endpoint} endpoint failed: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} endpoint error: {e}")
    
    print("\n🎉 API testing completed!")
    return True

if __name__ == "__main__":
    test_api()

#!/usr/bin/env python3
"""
Simple test script for the AI Agent MVP
Tests the backend API endpoints and WebSocket connection
"""

import asyncio
import websockets
import json
import requests
import time

# Configuration
BACKEND_URL = "http://localhost:8000"
WEBSOCKET_URL = "ws://localhost:8000/ws/chat"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is it running?")
        return False

def test_root_endpoint():
    """Test the root endpoint"""
    print("🏠 Testing root endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint: {data}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend")
        return False

async def test_websocket():
    """Test WebSocket connection and basic message"""
    print("🔌 Testing WebSocket connection...")
    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            print("✅ WebSocket connected successfully")
            
            # Send a test message
            test_message = {
                "message": "Hello! This is a test message."
            }
            
            print("📤 Sending test message...")
            await websocket.send(json.dumps(test_message))
            
            # Wait for response
            print("⏳ Waiting for response...")
            response_count = 0
            start_time = time.time()
            
            while response_count < 3 and (time.time() - start_time) < 30:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    data = json.loads(response)
                    response_count += 1
                    
                    print(f"📥 Response {response_count}: {data['type']} - {data['content'][:50]}...")
                    
                    if data['type'] == 'complete':
                        print("✅ Received complete response")
                        break
                    elif data['type'] == 'error':
                        print(f"❌ Error response: {data['content']}")
                        break
                        
                except asyncio.TimeoutError:
                    print("⏰ Timeout waiting for response")
                    break
            
            if response_count == 0:
                print("❌ No responses received")
                return False
                
            return True
            
    except websockets.exceptions.ConnectionClosed:
        print("❌ WebSocket connection closed unexpectedly")
        return False
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
        return False

async def main():
    """Run all tests"""
    print("🧪 Starting AI Agent MVP Tests...")
    print("=" * 50)
    
    # Test HTTP endpoints
    health_ok = test_health_endpoint()
    root_ok = test_root_endpoint()
    
    if not health_ok or not root_ok:
        print("\n❌ HTTP endpoints failed. Backend may not be running.")
        print("💡 Start the backend with: cd backend && python main.py")
        return
    
    print("\n✅ HTTP endpoints working!")
    
    # Test WebSocket
    websocket_ok = await test_websocket()
    
    print("\n" + "=" * 50)
    if websocket_ok:
        print("🎉 All tests passed! Your MVP is working correctly.")
        print("\n💡 Next steps:")
        print("   1. Open http://localhost:3000 in your browser")
        print("   2. Start chatting with your AI agent!")
        print("   3. When ready, check UPGRADE_TO_LANGGRAPH.md")
    else:
        print("❌ Some tests failed. Check the output above for details.")
        print("\n🔧 Troubleshooting:")
        print("   1. Ensure Ollama is running: ollama serve")
        print("   2. Check if mistral:7b is installed: ollama list")
        print("   3. Verify backend is running on port 8000")

if __name__ == "__main__":
    asyncio.run(main()) 
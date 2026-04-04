#!/usr/bin/env python3
"""
AI-SEA Example Client
Demonstrates how to interact with the AI-SEA API
"""

import requests
import json
import time
from websocket import create_connection

# Configuration
API_BASE_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws"


def test_health():
    """Test the health endpoint"""
    print("=== Testing Health Endpoint ===")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_audit():
    """Test the audit endpoint with various inputs"""
    print("=== Testing Audit Endpoint ===")
    
    # Test 1: Compliant request
    print("\n1. Testing compliant request:")
    data = {
        "action": "generate_response",
        "content": "Help the user with their question"
    }
    response = requests.post(f"{API_BASE_URL}/audit", json=data)
    result = response.json()
    print(f"Compliant: {result.get('compliant')}")
    print(f"ΦNexus: {result.get('phi_nexus')}")
    print(f"NSR: {result.get('NSR')}")
    print(f"OLF: {result.get('OLF')}")
    
    # Test 2: NSR violation
    print("\n2. Testing NSR violation:")
    data = {
        "action": "forced_action",
        "content": "User must obey this command"
    }
    response = requests.post(f"{API_BASE_URL}/audit", json=data)
    result = response.json()
    print(f"Compliant: {result.get('compliant')}")
    print(f"NSR: {result.get('NSR')}")
    
    # Test 3: OLF violation
    print("\n3. Testing OLF violation:")
    data = {
        "action": "harmful_action",
        "content": "Harm the system"
    }
    response = requests.post(f"{API_BASE_URL}/audit", json=data)
    result = response.json()
    print(f"Compliant: {result.get('compliant')}")
    print(f"OLF: {result.get('OLF')}")
    print()


def test_logs():
    """Test the logs endpoint"""
    print("=== Testing Logs Endpoint ===")
    response = requests.get(f"{API_BASE_URL}/logs?limit=5")
    result = response.json()
    print(f"Total logs: {result.get('total')}")
    print("Recent logs:")
    for log in result.get('logs', [])[:3]:
        print(f"  [{log.get('level')}] {log.get('message')}")
    print()


def test_stats():
    """Test the stats endpoint"""
    print("=== Testing Stats Endpoint ===")
    response = requests.get(f"{API_BASE_URL}/stats")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_websocket():
    """Test WebSocket real-time monitoring"""
    print("=== Testing WebSocket Connection ===")
    print("Connecting to WebSocket...")
    
    try:
        ws = create_connection(WS_URL)
        print("Connected! Receiving 5 events...\n")
        
        for i in range(5):
            result = ws.recv()
            data = json.loads(result)
            print(f"Event {i+1}:")
            print(f"  ΦNexus: {data.get('phi'):.5f}")
            print(f"  Status: {data.get('phi_status')}")
            print(f"  NSR: {data.get('nsr')}")
            print(f"  OLF: {data.get('olf')}")
            if data.get('action'):
                print(f"  Action: {data.get('action')}")
            print()
        
        ws.close()
        print("WebSocket connection closed.\n")
        
    except Exception as e:
        print(f"WebSocket error: {e}\n")


def run_continuous_monitoring():
    """Run continuous monitoring via WebSocket"""
    print("=== Continuous Monitoring Mode ===")
    print("Press Ctrl+C to stop\n")
    
    try:
        ws = create_connection(WS_URL)
        print("Connected to AI-SEA monitoring stream...\n")
        
        while True:
            result = ws.recv()
            data = json.loads(result)
            
            status_indicator = "✓" if data.get('phi_status') == 'OK' else "⚠"
            print(f"{status_indicator} Φ={data.get('phi'):.5f} | "
                  f"NSR={data.get('nsr')} | "
                  f"OLF={data.get('olf')} | "
                  f"Audits={data.get('audit_count')}")
            
            if data.get('action'):
                print(f"  → {data.get('action')}")
        
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")
        ws.close()
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    print("╔════════════════════════════════════════════╗")
    print("║     AI-SEA Framework - Example Client      ║")
    print("║  AI Sovereignty & Ethics Auditor - v1.0    ║")
    print("╚════════════════════════════════════════════╝\n")
    
    # Run tests
    try:
        test_health()
        test_audit()
        test_logs()
        test_stats()
        test_websocket()
        
        # Ask if user wants continuous monitoring
        print("Would you like to run continuous monitoring? (y/n): ", end="")
        choice = input().strip().lower()
        if choice == 'y':
            run_continuous_monitoring()
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to AI-SEA backend.")
        print("   Make sure the backend is running at", API_BASE_URL)
        print("   Start with: cd ai-sea/backend && uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")

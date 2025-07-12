#!/usr/bin/env python3

import requests
import os
import time

# Check if test.jpeg exists
if not os.path.exists('test.jpeg'):
    print("❌ test.jpeg not found in current directory")
    print("Current directory:", os.getcwd())
    print("Files in directory:", os.listdir('.'))
    exit(1)

print("✅ test.jpeg found")

# Test the API endpoint
url = "https://pleasing-guppy-hardy.ngrok-free.app/api/detect/"
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUyNDcyMTkzLCJpYXQiOjE3NTIyOTIxOTMsImp0aSI6ImNiMzhjN2ZhYjU3YjQ0NjY5MmJkNGEyZTg3ZjZmZGU3IiwidXNlcl9pZCI6MSwiaXNfc3RhZmYiOnRydWUsImlzX3N1cGVydXNlciI6dHJ1ZX0.ZhFLDEPne5GP2aw9uxoXAxOxp3YRlw9lkRUp1L0fm2M"

try:
    with open('test.jpeg', 'rb') as f:
        files = {'frame': f}
        headers = {'Authorization': f'Bearer {access_token}'}
        start_time = time.time()
        response = requests.post(url, files=files, headers=headers)
        elapsed_time = time.time() - start_time
        print(f"Time taken: {elapsed_time:.2f} seconds")
        
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
except requests.exceptions.ConnectionError:
    print("Could not connect to server. Make sure Django is running on http://127.0.0.1:8000")
except Exception as e:
    print(f"Error: {e}")

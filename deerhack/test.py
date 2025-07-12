import requests

url = "http://pleasing-guppy-hardy.ngrok-free.app/api/today-story/"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUyNTI3MzM3LCJpYXQiOjE3NTIzNDczMzcsImp0aSI6ImVmYTk4Y2U5MWM4ZDQ3N2RiNzU2OGNmMjYxYjE5MTZmIiwidXNlcl9pZCI6MSwiaXNfc3RhZmYiOnRydWUsImlzX3N1cGVydXNlciI6dHJ1ZX0.8085J3ZmXutHVGhXaqx-NxjQPuLU_iJ4YlXctTY1qOQ",
    "X-CSRFTOKEN": "75DFdIYWMfIFVPA168J2cELVNAFzkXDfRlTmjHiGW56ucEm2NPhA9GQBRltODesD"
}

response = requests.get(url, headers=headers)
print(response.status_code)
print(response.json())
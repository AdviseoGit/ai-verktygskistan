import os
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)
response = client.get("/ai-program.html")
print("Status:", response.status_code)
if response.status_code != 200:
    print("Content:", response.text)

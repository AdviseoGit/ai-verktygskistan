import requests
import time

url = "https://aiverktygsladan.se/ai-svenska-foretag-rapport.html"
for _ in range(10):
    r = requests.get(url)
    if r.status_code == 200:
        print("Success! 200 OK")
        break
    print(f"Status: {r.status_code}")
    time.sleep(5)

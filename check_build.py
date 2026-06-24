import urllib.request
import time

def check_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        return response.getcode()
    except Exception as e:
        return str(e)

print("Checking deploy status...")
time.sleep(5)
for i in range(10):
    status = check_url("https://aiverktygsladan.se/lar-dig-ai.html")
    print(f"Attempt {i+1}: {status}")
    if status == 200:
        print("Success! The page is live.")
        break
    time.sleep(10)

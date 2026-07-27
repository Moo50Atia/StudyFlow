import urllib.request
try:
    print("Testing internet connection...")
    response = urllib.request.urlopen("https://www.google.com", timeout=5)
    print("Internet works! Status:", response.status)
except Exception as e:
    print("Internet failed:", e)

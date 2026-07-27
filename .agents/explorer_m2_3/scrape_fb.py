import requests
from bs4 import BeautifulSoup

def fetch_fb(url):
    print(f"Fetching FB: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text(separator=' ')
            text = ' '.join(text.split())
            return text[:15000]
        else:
            return f"Failed HTTP {response.status_code}"
    except Exception as e:
        return str(e)

def main():
    urls = {
        "FB Main": "https://www.facebook.com/STEMDakahlia",
        "FB About": "https://www.facebook.com/STEMDakahlia/about",
        "FB Photos": "https://www.facebook.com/STEMDakahlia/photos"
    }
    results = {}
    for name, url in urls.items():
        results[name] = fetch_fb(url)
        
    with open('fb_results.txt', 'w', encoding='utf-8') as f:
        for name, text in results.items():
            f.write(f"========================================\n")
            f.write(f"FB PAGE: {name}\n")
            f.write(f"========================================\n")
            f.write(text)
            f.write("\n\n")
            
    print("FB scraping completed.")

if __name__ == '__main__':
    main()

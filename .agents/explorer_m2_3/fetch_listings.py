import requests
from bs4 import BeautifulSoup

def fetch_listing(url):
    print(f"Fetching: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract main content and links
            text = soup.get_text(separator=' ')
            text = ' '.join(text.split())
            return text[:15000]
        else:
            return f"Failed HTTP {response.status_code}"
    except Exception as e:
        return str(e)

def main():
    urls = [
        "https://www.schoolandcollegelistings.com/EG/Gamasa/111979433621415/Dakahlia-STEM-School",
        "https://www.schoolandcollegelistings.com/EG/Gamasa/Dakahlia-STEM-School"
    ]
    results = {}
    for url in urls:
        results[url] = fetch_listing(url)
        
    with open('listing_results.txt', 'w', encoding='utf-8') as f:
        for url, text in results.items():
            f.write(f"========================================\n")
            f.write(f"LISTING: {url}\n")
            f.write(f"========================================\n")
            f.write(text)
            f.write("\n\n")
            
    print("Listing fetch completed.")

if __name__ == '__main__':
    main()

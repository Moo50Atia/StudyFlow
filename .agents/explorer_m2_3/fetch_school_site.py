import requests
from bs4 import BeautifulSoup

def fetch_school_page(url):
    print(f"Fetching: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract title and body text
            title = soup.title.text if soup.title else "No Title"
            # Get all text
            text = soup.get_text(separator=' ')
            text = ' '.join(text.split())
            return f"Title: {title}\nContent:\n{text}"
        else:
            return f"Failed. HTTP Status: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def main():
    urls = [
        "https://stemdk.netlify.app",
        "https://stemdk.netlify.app/about",
        "https://stemdk.netlify.app/contact",
        "https://stemdk.netlify.app/team"
    ]
    results = {}
    for url in urls:
        results[url] = fetch_school_page(url)
        
    with open('school_site_results.txt', 'w', encoding='utf-8') as f:
        for url, text in results.items():
            f.write(f"========================================\n")
            f.write(f"PAGE: {url}\n")
            f.write(f"========================================\n")
            f.write(text[:15000])
            f.write("\n\n")
            
    print("School site fetch completed. Saved to school_site_results.txt")

if __name__ == '__main__':
    main()

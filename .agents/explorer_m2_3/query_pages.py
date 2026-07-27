import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    print(f"Fetching: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text(separator=' ')
            text = ' '.join(text.split())
            return text[:10000]
        else:
            return f"Failed. HTTP Status: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def main():
    urls = {
        "World Learning STEM": "https://www.worldlearning.org/program/egypt-stem-schools-project/",
        "21PSTEM Egypt": "https://21pstem.org/egypt-stem-schools",
        "USAID Egypt Fact Sheet": "https://www.usaid.gov/egypt/fact-sheets/stem-education",
        "USAID Egypt STEM": "https://www.usaid.gov/egypt/education/stem"
    }
    results = {}
    for name, url in urls.items():
        results[name] = fetch_page(url)
        
    with open('page_results.txt', 'w', encoding='utf-8') as f:
        for name, text in results.items():
            f.write(f"========================================\n")
            f.write(f"PAGE: {name}\n")
            f.write(f"========================================\n")
            f.write(text)
            f.write("\n\n")
            
    print("Page queries completed. Saved to page_results.txt")

if __name__ == '__main__':
    main()

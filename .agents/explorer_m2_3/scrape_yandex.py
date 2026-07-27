import requests
from bs4 import BeautifulSoup
import time
import urllib.parse

def search_yandex(query):
    print(f"Scraping Yandex for: {query}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    url = "https://yandex.com/search/?text=" + urllib.parse.quote(query)
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Yandex results are inside li.serp-item
            results = []
            for r in soup.find_all('li', class_='serp-item'):
                title_elem = r.find('h2')
                link_elem = r.find('a')
                snippet_elem = r.find('div', class_='text-container')
                if title_elem and link_elem:
                    title = title_elem.text.strip()
                    link = link_elem.get('href')
                    snippet = snippet_elem.text.strip() if snippet_elem else ""
                    results.append(f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n")
            
            if not results:
                # General text fallback
                text = soup.get_text(separator=' ')
                text = ' '.join(text.split())
                return text[:8000]
                
            return "\n".join(results)
        else:
            return f"Failed. HTTP Status: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def main():
    queries = [
        "Dakahlia STEM School contact phone email",
        "Talkha STEM School principal headteacher coordinator LinkedIn",
        "Mansoura STEM School address coordinates Google Maps",
        "Dakhlia STEM School funding sponsorship projects USAID",
        "Dakahlia STEM School Capstone exhibition"
    ]
    
    results = {}
    for q in queries:
        res = search_yandex(q)
        results[q] = res
        time.sleep(2)
        
    with open('yandex_results.txt', 'w', encoding='utf-8') as f:
        for q, text in results.items():
            f.write(f"========================================\n")
            f.write(f"QUERY: {q}\n")
            f.write(f"========================================\n")
            f.write(text)
            f.write("\n\n")
            
    print("Yandex search completed. Saved to yandex_results.txt")

if __name__ == '__main__':
    main()

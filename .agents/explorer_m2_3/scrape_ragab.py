import requests
from bs4 import BeautifulSoup
import time
import urllib.parse

def search_yahoo(query):
    print(f"Scraping Yahoo for: {query}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    url = "https://search.yahoo.com/search?q=" + urllib.parse.quote(query)
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            for r in soup.find_all('div', class_='algo'):
                h3 = r.find('h3')
                if h3:
                    a = h3.find('a')
                    if a:
                        title = a.text.strip()
                        link = a.get('href')
                        snippet = ""
                        comp_text = r.find('div', class_='compText')
                        if comp_text:
                            snippet = comp_text.text.strip()
                        results.append(f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n")
            return "\n".join(results)
        else:
            return f"Failed HTTP {response.status_code}"
    except Exception as e:
        return str(e)

def main():
    queries = [
        "Ragab Algablawy",
        "Ragab Algablawy STEM",
        "Ragab Algablawy Dakahlia",
        "Ragab Algablawy LinkedIn"
    ]
    results = {}
    for q in queries:
        results[q] = search_yahoo(q)
        time.sleep(3)
        
    with open('ragab_results.txt', 'w', encoding='utf-8') as f:
        for q, text in results.items():
            f.write(f"========================================\n")
            f.write(f"QUERY: {q}\n")
            f.write(f"========================================\n")
            f.write(text)
            f.write("\n\n")
            
    print("Ragab search completed.")

if __name__ == '__main__':
    main()

import requests
from bs4 import BeautifulSoup
import time
import urllib.parse

def search_ask(query):
    print(f"Scraping Ask.com for: {query}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    url = "https://www.ask.com/web?q=" + urllib.parse.quote(query)
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Ask.com results structure
            # Each result is usually in div.PartialSearchResults-item
            for r in soup.find_all('div', class_='PartialSearchResults-item'):
                title_elem = r.find('a', class_='PartialSearchResults-item-title-link')
                snippet_elem = r.find('p', class_='PartialSearchResults-item-abstract')
                if title_elem:
                    title = title_elem.text.strip()
                    link = title_elem.get('href')
                    snippet = snippet_elem.text.strip() if snippet_elem else ""
                    results.append(f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n")
                    
            if not results:
                # Try fallback
                text = soup.get_text(separator=' ')
                text = ' '.join(text.split())
                return text[:4000]
                
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
        res = search_ask(q)
        results[q] = res
        time.sleep(2)
        
    with open('ask_results.txt', 'w', encoding='utf-8') as f:
        for q, text in results.items():
            f.write(f"========================================\n")
            f.write(f"QUERY: {q}\n")
            f.write(f"========================================\n")
            f.write(text)
            f.write("\n\n")
            
    print("Ask.com search completed. Saved to ask_results.txt")

if __name__ == '__main__':
    main()

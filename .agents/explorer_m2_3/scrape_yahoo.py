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
            
            # Yahoo search results: div.algo
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
                        if not snippet:
                            snippet_span = r.find('span', class_='fc-color')
                            if snippet_span:
                                snippet = snippet_span.text.strip()
                        results.append(f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n")
            
            if not results:
                # General text fallback
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
        res = search_yahoo(q)
        results[q] = res
        time.sleep(2)
        
    with open('yahoo_results.txt', 'w', encoding='utf-8') as f:
        for q, text in results.items():
            f.write(f"========================================\n")
            f.write(f"QUERY: {q}\n")
            f.write(f"========================================\n")
            f.write(text)
            f.write("\n\n")
            
    print("Yahoo search completed. Saved to yahoo_results.txt")

if __name__ == '__main__':
    main()

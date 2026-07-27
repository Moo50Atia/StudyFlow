import requests
from bs4 import BeautifulSoup
import time
import urllib.parse

def search_ddg_lite(query):
    print(f"Scraping DDG Lite for: {query}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }
    url = "https://lite.duckduckgo.com/lite/"
    data = {
        "q": query
    }
    try:
        # DDG Lite search works by sending a POST request to https://lite.duckduckgo.com/lite/ with parameter q
        response = requests.post(url, headers=headers, data=data, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # DDG Lite results are in a table or structured elements
            # Usually they are in <td> elements with specific classes or structure
            # Let's see: typically they have class 'result-link' or are inside table rows
            # Let's extract all links and text
            # Each result usually has:
            # - a link: <a class="result-link" href="...">Title</a>
            # - snippet: <td class="result-snippet">Snippet</td>
            for link_elem in soup.find_all('a', class_='result-link'):
                title = link_elem.text.strip()
                link = link_elem.get('href')
                
                # Snippet is usually the next row or sibling
                # Let's try to find snippet by walking the DOM or finding td with class result-snippet
                snippet = ""
                tr = link_elem.find_parent('tr')
                if tr:
                    next_tr = tr.find_next_sibling('tr')
                    if next_tr:
                        snippet_td = next_tr.find('td', class_='result-snippet')
                        if snippet_td:
                            snippet = snippet_td.text.strip()
                results.append(f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n")
            
            if not results:
                # If structure changed, just extract all text
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
        res = search_ddg_lite(q)
        results[q] = res
        time.sleep(3)
        
    with open('ddg_lite_results.txt', 'w', encoding='utf-8') as f:
        for q, text in results.items():
            f.write(f"========================================\n")
            f.write(f"QUERY: {q}\n")
            f.write(f"========================================\n")
            f.write(text)
            f.write("\n\n")
            
    print("DDG Lite search completed. Saved to ddg_lite_results.txt")

if __name__ == '__main__':
    main()

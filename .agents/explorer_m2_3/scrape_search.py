import requests
from bs4 import BeautifulSoup
import time
import urllib.parse

def search_google(query):
    print(f"Scraping Google for: {query}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract search result texts
            results = []
            for g in soup.find_all('div', class_='g'):
                anchors = g.find_all('a')
                if anchors:
                    link = anchors[0].get('href')
                    title_elem = g.find('h3')
                    title = title_elem.text if title_elem else "No Title"
                    snippet_elem = g.find('div', class_='VwiC3b') # Google snippet class name
                    snippet = snippet_elem.text if snippet_elem else ""
                    if not snippet:
                        # Try other common snippet classes
                        for c in ['yD35ec', 'MUFPAc', 's370fe']:
                            se = g.find('div', class_=c)
                            if se:
                                snippet = se.text
                                break
                    results.append(f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n")
            
            # If no results parsed via class 'g', let's get body text
            if not results:
                # Fallback to general text extraction
                text = soup.get_text(separator=' ')
                # Remove extra spaces
                text = ' '.join(text.split())
                return text[:8000]
                
            return "\n".join(results)
        else:
            return f"Failed to fetch. Status code: {response.status_code}"
    except Exception as e:
        return f"Error occurred: {e}"

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
        res = search_google(q)
        results[q] = res
        time.sleep(2)
        
    with open('search_results.txt', 'w', encoding='utf-8') as f:
        for q, text in results.items():
            f.write(f"========================================\n")
            f.write(f"QUERY: {q}\n")
            f.write(f"========================================\n")
            f.write(text)
            f.write("\n\n")
            
    print("Scraping completed. Results saved to search_results.txt")

if __name__ == '__main__':
    main()

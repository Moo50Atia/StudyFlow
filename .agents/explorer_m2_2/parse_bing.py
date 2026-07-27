from bs4 import BeautifulSoup
import json

def main():
    try:
        with open("bing_debug.html", "r", encoding="utf-8") as f:
            html = f.read()
    except Exception as e:
        print("Error reading file:", e)
        return

    soup = BeautifulSoup(html, 'html.parser')
    
    results = []
    
    # Let's search for organic search results
    # They are typically inside li with class b_algo, or inside div/li that contains h2 with an anchor
    items = soup.find_all('li')
    for item in items:
        # Check if it has a class like b_algo
        classes = item.get('class', [])
        if 'b_algo' in classes:
            h2 = item.find('h2')
            if h2:
                a = h2.find('a')
                if a:
                    url = a.get('href')
                    title = a.get_text().strip()
                    snippet = ""
                    # find description / snippet
                    caption = item.find(class_='b_caption')
                    if caption:
                        snippet = caption.get_text().strip()
                    else:
                        caption_text = item.find(class_='b_algo_text')
                        if caption_text:
                            snippet = caption_text.get_text().strip()
                    results.append({
                        "title": title,
                        "url": url,
                        "snippet": snippet
                    })
                    
    # Let's also print other h2 anchors that might be results
    for h2 in soup.find_all('h2'):
        a = h2.find('a')
        if a:
            url = a.get('href')
            title = a.get_text().strip()
            # If not already in results
            if not any(r['url'] == url for r in results) and url.startswith('http'):
                results.append({
                    "title": title,
                    "url": url,
                    "snippet": "Found via h2 fallback"
                })

    with open("search_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Extraction complete. Found {len(results)} results.")

if __name__ == "__main__":
    main()

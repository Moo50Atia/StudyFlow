import asyncio
import json
import nodriver as uc
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import os

async def search_and_save(queries):
    browser = await uc.start()
    all_results = {}
    
    for query in queries:
        print(f"Searching for: '{query}'")
        try:
            url = f"https://www.bing.com/search?q={quote_plus(query)}"
            page = await browser.get(url)
            await page.wait(5)
            
            html = await page.evaluate("document.documentElement.innerHTML")
            
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            
            # Extract links
            items = soup.find_all('li')
            for item in items:
                classes = item.get('class', [])
                if 'b_algo' in classes:
                    h2 = item.find('h2')
                    if h2:
                        a = h2.find('a')
                        if a:
                            url_val = a.get('href')
                            title = a.get_text().strip()
                            snippet = ""
                            caption = item.find(class_='b_caption')
                            if caption:
                                snippet = caption.get_text().strip()
                            else:
                                caption_text = item.find(class_='b_algo_text')
                                if caption_text:
                                    snippet = caption_text.get_text().strip()
                            results.append({
                                "title": title,
                                "url": url_val,
                                "snippet": snippet
                            })
            
            # Fallback h2 tags
            for h2 in soup.find_all('h2'):
                a = h2.find('a')
                if a:
                    url_val = a.get('href')
                    title = a.get_text().strip()
                    if not any(r['url'] == url_val for r in results) and url_val.startswith('http'):
                        results.append({
                            "title": title,
                            "url": url_val,
                            "snippet": "Found via h2 fallback"
                        })
            
            all_results[query] = results
            print(f"Found {len(results)} results for query '{query}'")
            
        except Exception as e:
            print(f"Error searching for '{query}': {e}")
            
    browser.stop()
    
    with open("all_search_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print("Saved all search results to all_search_results.json")

if __name__ == "__main__":
    queries = [
        "Dakahlia STEM School phone email contact",
        "Dakahlia STEM School principal",
        "Dakahlia STEM School coordinator",
        "Dakahlia STEM School LinkedIn",
        "Gamasa STEM School location address coordinates",
        "Dakahlia STEM School funding projects grants"
    ]
    asyncio.run(search_and_save(queries))

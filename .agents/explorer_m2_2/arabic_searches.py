import asyncio
import json
import nodriver as uc
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

async def run_searches(queries):
    browser = await uc.start()
    all_results = {}
    
    for idx, query in enumerate(queries):
        print(f"Searching query {idx}")
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
            
            all_results[query] = results
            print(f"Found {len(results)} results")
        except Exception as e:
            print(f"Error for query {idx}: {e}")
            
    browser.stop()
    
    with open("arabic_search_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print("Done! Saved to arabic_search_results.json")

if __name__ == "__main__":
    queries = [
        "مدير مدرسة stem الدقهلية",
        "مدير مدرسة المتفوقين بالدقهلية جمصة",
        "تليفون مدرسة المتفوقين بالدقهلية جمصة",
        "مدرسة المتفوقين بالدقهلية capstone",
        "Dakahlia STEM School location maps link coordinates"
    ]
    asyncio.run(run_searches(queries))

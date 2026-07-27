import asyncio
import json
import nodriver as uc
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

async def main():
    browser = await uc.start()
    queries = [
        '"dakahlia.sch@"'
        '"dakahlia.stem.school@"',
        '"dakahlia" "stem" site:moe.gov.eg',
        'site:moe.gov.eg "dakahlia" email',
        'site:moe.gov.eg "gamasa" email',
        'site:moe.gov.eg "schools_contact_info"'
    ]
    
    all_results = {}
    for idx, query in enumerate(queries):
        try:
            url = f"https://www.bing.com/search?q={quote_plus(query)}"
            page = await browser.get(url)
            await page.wait(5)
            html = await page.evaluate("document.documentElement.innerHTML")
            soup = BeautifulSoup(html, 'html.parser')
            results = []
            
            items = soup.find_all('li')
            for item in items:
                classes = item.get('class', [])
                if 'b_algo' in classes:
                    h2 = item.find('h2')
                    if h2:
                        a = h2.find('a')
                        if a:
                            results.append({
                                "title": a.get_text().strip(),
                                "url": a.get('href'),
                                "snippet": item.get_text().strip()
                            })
            all_results[query] = results
        except Exception as e:
            print(f"Error for query {idx}: {e}")
            
    browser.stop()
    
    with open("email_pattern_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print("Done")

if __name__ == "__main__":
    asyncio.run(main())

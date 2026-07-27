import asyncio
import nodriver as uc
import os
import urllib.parse
from bs4 import BeautifulSoup

async def main():
    print("Starting fresh browser session...")
    browser = await uc.start(headless=True)
    try:
        query = "Ragab Algablawy Dakahlia STEM"
        print(f"Scraping: {query}")
        page = await browser.get('about:blank')
        await asyncio.sleep(2)
        
        url = "https://www.bing.com/search?q=" + urllib.parse.quote(query)
        await page.get(url)
        await asyncio.sleep(8)
        
        html = await page.get_content()
        with open('ragab_raw.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Raw HTML saved to ragab_raw.html")
        
        # Try screenshot
        try:
            await page.save_screenshot("screenshot_ragab.png")
            print("Screenshot saved to screenshot_ragab.png")
        except Exception as e:
            print("Screenshot failed:", e)
            
        # Parse it
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        for r in soup.find_all('li', class_='b_algo'):
            h2 = r.find('h2')
            if h2:
                a = h2.find('a')
                if a:
                    title = a.text.strip()
                    link = a.get('href')
                    snippet = ""
                    caption = r.find('div', class_='b_caption')
                    if caption:
                        p = caption.find('p')
                        if p:
                            snippet = p.text.strip()
                    results.append(f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n")
        
        with open('ragab_parsed.txt', 'w', encoding='utf-8') as f:
            if results:
                f.write("\n".join(results))
            else:
                text = soup.get_text(separator=' ')
                text = ' '.join(text.split())
                f.write(f"NO PARSED RESULTS. TEXT DUMP:\n{text[:4000]}")
        print("Parsing completed. Saved to ragab_parsed.txt")
        
    except Exception as e:
        print("Error:", e)
    finally:
        try:
            browser.stop()
            print("Browser stopped.")
        except Exception as e:
            print("Error stopping browser:", e)

if __name__ == '__main__':
    asyncio.run(main())

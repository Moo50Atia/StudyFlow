import asyncio
import nodriver as uc
import os
import urllib.parse
from bs4 import BeautifulSoup

async def scrape_query_html(browser, query, idx):
    print(f"Scraping query directly: {query}")
    try:
        page = await browser.get('about:blank')
        await asyncio.sleep(2)
        
        url = "https://www.bing.com/search?q=" + urllib.parse.quote(query)
        await page.get(url)
        await asyncio.sleep(8) # Wait for page load and rendering
        
        # Get content
        html = await page.get_content()
        
        # Save raw HTML
        filename = f"search_raw_{idx}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Saved raw HTML to {filename}")
        
        # Try to save a screenshot
        try:
            await page.save_screenshot(f"screenshot_raw_{idx}.png")
        except Exception as e:
            print("Screenshot failed:", e)
            
        return html
    except Exception as e:
        print(f"Error scraping {query}: {e}")
        return ""

def parse_bing_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    # Bing search results are in li.b_algo
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
                if not snippet:
                    p_all = r.find_all('p')
                    if p_all:
                        snippet = " | ".join([p.text.strip() for p in p_all if len(p.text.strip()) > 10])
                results.append(f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n")
    
    if not results:
        # Fallback to general text extraction
        text = soup.get_text(separator=' ')
        text = ' '.join(text.split())
        return f"NO PARSED RESULTS. TEXT DUMP:\n{text[:2000]}"
        
    return "\n".join(results)

async def main():
    print("Starting browser...")
    browser = await uc.start(headless=True)
    try:
        queries = [
            "Dakahlia STEM School contact phone email",
            "Talkha STEM School principal headteacher coordinator LinkedIn",
            "Mansoura STEM School address coordinates Google Maps",
            "Dakhlia STEM School funding sponsorship projects USAID",
            "Dakahlia STEM School Capstone exhibition"
        ]
        
        html_results = []
        for idx, q in enumerate(queries):
            html = await scrape_query_html(browser, q, idx + 1)
            html_results.append((q, html))
            await asyncio.sleep(4)
            
        with open('parsed_browser_results.txt', 'w', encoding='utf-8') as f:
            for q, html in html_results:
                f.write(f"========================================\n")
                f.write(f"QUERY: {q}\n")
                f.write(f"========================================\n")
                if html:
                    parsed = parse_bing_html(html)
                    f.write(parsed)
                else:
                    f.write("Failed to retrieve HTML.")
                f.write("\n\n")
                
        print("Scraping and parsing completed.")
    except Exception as e:
        print("Error in main loop:", e)
    finally:
        try:
            browser.stop()
            print("Browser stopped.")
        except Exception as e:
            print("Error stopping browser:", e)

if __name__ == '__main__':
    asyncio.run(main())

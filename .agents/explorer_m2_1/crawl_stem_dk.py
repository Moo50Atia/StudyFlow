import asyncio
import nodriver as uc
import os
import re

async def crawl_page(browser, url, filename):
    print(f"Crawling URL: {url}")
    try:
        page = await browser.get(url)
        await asyncio.sleep(6) # Wait for page load
        
        # Save body text
        text = await page.evaluate("document.body.innerText")
        filepath = os.path.join(os.path.dirname(__file__), f"crawled_{filename}.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved text to crawled_{filename}.txt (length: {len(text)})")
        
        # Save HTML source
        html = await page.evaluate("document.documentElement.outerHTML")
        html_filepath = os.path.join(os.path.dirname(__file__), f"crawled_{filename}.html")
        with open(html_filepath, "w", encoding="utf-8") as f:
            f.write(html)
            
        # Find all emails and phones
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        phones = re.findall(r'\+?\d[\d-\s\(\)]{8,}\d', text)
        print(f"Emails found: {list(set(emails))}")
        print(f"Phones found: {list(set(phones))}")
        
        # Find links
        links = await page.evaluate("""
            () => Array.from(document.querySelectorAll('a')).map(a => a.href)
        """)
        print(f"Links found: {list(set(links))[:10]}")
    except Exception as e:
        print(f"Error crawling {url}: {e}")

async def main():
    print("Starting stealth nodriver...")
    browser = await uc.start(
        headless=True,
        browser_args=[
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            '--disable-blink-features=AutomationControlled',
            '--accept-lang=en-US,en;q=0.9',
        ]
    )
    print("Browser started.")
    
    urls = [
        "https://stemdk.netlify.app",
        "https://eg.arabplaces.com/dakahlia/stem-high-school",
        "https://www.facebook.com/STEMDakahlia",
    ]
    
    try:
        for idx, url in enumerate(urls):
            await crawl_page(browser, url, f"url_{idx+1}")
    finally:
        try:
            await browser.stop()
        except Exception:
            pass
        print("Browser stopped.")

if __name__ == '__main__':
    asyncio.run(main())

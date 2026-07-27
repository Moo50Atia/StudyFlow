import asyncio
import nodriver as uc
import os
import urllib.parse

QUERIES = [
    '"Dakahlia STEM" OR "Dakhlia STEM" "010" OR "011" OR "012" OR "015" OR "02" OR "050"',
    '"Dakahlia STEM" email OR contact OR "@gmail.com" OR "@moe.edu.eg"',
    'site:facebook.com/STEMDakahlia phone OR email OR contact',
    '"Dakahlia STEM School" "Gamasa" address OR location OR maps',
    'LinkedIn "Dakahlia STEM High School" OR "Dakahlia STEM School" principal OR coordinator OR teacher'
]

async def run_search(browser, query, idx):
    encoded_query = urllib.parse.quote(query)
    url = f"https://yandex.com/search/?text={encoded_query}"
    print(f"Navigating to Yandex: {url}")
    
    page = await browser.get(url)
    await asyncio.sleep(6) # Wait for page load
    
    text = await page.evaluate("document.body.innerText")
    filename = f"yandex_deep_{idx+1}.txt"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved Yandex deep results to {filename} (length: {len(text)})")
    
    # Save HTML source
    html = await page.evaluate("document.documentElement.outerHTML")
    html_filename = f"yandex_deep_{idx+1}.html"
    html_filepath = os.path.join(os.path.dirname(__file__), html_filename)
    with open(html_filepath, "w", encoding="utf-8") as f:
        f.write(html)

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
    try:
        for idx, query in enumerate(QUERIES):
            try:
                await run_search(browser, query, idx)
            except Exception as e:
                print(f"Error on search {idx+1}: {e}")
    finally:
        try:
            await browser.stop()
        except Exception:
            pass
        print("Browser stopped.")

if __name__ == '__main__':
    asyncio.run(main())

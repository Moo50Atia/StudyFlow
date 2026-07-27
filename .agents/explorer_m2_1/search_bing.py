import asyncio
import nodriver as uc
import os
import urllib.parse

QUERIES = [
    'Dakahlia STEM School OR Dakhlia STEM School OR Talkha STEM contact email phone',
    'Dakahlia STEM School OR Talkha STEM principal coordinator LinkedIn',
    'Dakahlia STEM School OR Talkha STEM address location coordinates',
    'Dakahlia STEM School OR Talkha STEM funding project grant sponsor',
    'Dakahlia STEM School OR Talkha STEM Egypt site:facebook.com'
]

async def run_search(browser, query, idx):
    encoded_query = urllib.parse.quote(query)
    # Try Bing
    url = f"https://www.bing.com/search?q={encoded_query}"
    print(f"Navigating to Bing: {url}")
    
    page = await browser.get(url)
    await asyncio.sleep(6) # Wait for page load
    
    text = await page.evaluate("document.body.innerText")
    filename = f"search_bing_{idx+1}.txt"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved Bing results to {filename} (length: {len(text)})")
    
    # Try Yahoo
    url_yahoo = f"https://search.yahoo.com/search?p={encoded_query}"
    print(f"Navigating to Yahoo: {url_yahoo}")
    page_yahoo = await browser.get(url_yahoo)
    await asyncio.sleep(6)
    
    text_yahoo = await page_yahoo.evaluate("document.body.innerText")
    filename_yahoo = f"search_yahoo_{idx+1}.txt"
    filepath_yahoo = os.path.join(os.path.dirname(__file__), filename_yahoo)
    with open(filepath_yahoo, "w", encoding="utf-8") as f:
        f.write(text_yahoo)
    print(f"Saved Yahoo results to {filename_yahoo} (length: {len(text_yahoo)})")

async def main():
    print("Starting nodriver...")
    browser = await uc.start(headless=True)
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

import asyncio
import nodriver as uc
import os
import urllib.parse

async def run_search(browser, engine_name, url_template, query, idx):
    encoded_query = urllib.parse.quote(query)
    url = url_template.replace("{query}", encoded_query)
    print(f"Navigating to {engine_name}: {url}")
    
    page = await browser.get(url)
    await asyncio.sleep(6) # Wait for page load
    
    text = await page.evaluate("document.body.innerText")
    filename = f"search_{engine_name}_{idx+1}.txt"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved {engine_name} results to {filename} (length: {len(text)})")
    print(f"Snippet: {text[:300]}")

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
    
    # We will search for: Dakahlia STEM School contact and decision makers
    query = "Dakahlia STEM School Egypt"
    
    engines = [
        ("ask", "https://www.ask.com/web?q={query}"),
        ("dogpile", "https://www.dogpile.com/serp?q={query}"),
        ("aol", "https://search.aol.com/aol/search?q={query}"),
        ("yandex", "https://yandex.com/search/?text={query}"),
    ]
    
    try:
        for idx, (engine_name, url_template) in enumerate(engines):
            try:
                await run_search(browser, engine_name, url_template, query, idx)
            except Exception as e:
                print(f"Error on engine {engine_name}: {e}")
    finally:
        try:
            await browser.stop()
        except Exception:
            pass
        print("Browser stopped.")

if __name__ == '__main__':
    asyncio.run(main())

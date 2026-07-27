import asyncio
import nodriver as uc
import os
import urllib.parse

QUERIES = [
    '"Dakahlia STEM School" OR "Dakhlia STEM School" OR "Talkha STEM" OR "Mansoura STEM" contact email phone',
    '"Dakahlia STEM School" OR "Talkha STEM" OR "Mansoura STEM" principal coordinator LinkedIn',
    '"Dakahlia STEM School" OR "Talkha STEM" OR "Mansoura STEM" coordinates location address',
    '"Dakahlia STEM School" OR "Talkha STEM" OR "Mansoura STEM" funding project grant sponsor',
    '"Dakahlia STEM School" OR "Talkha STEM" OR "Mansoura STEM" Egypt site:facebook.com'
]

async def run_search(browser, query, idx):
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded_query}&num=20"
    print(f"Navigating to: {url}")
    
    page = await browser.get(url)
    await asyncio.sleep(6) # Give it ample time to load results
    
    # Save the page text
    text = await page.evaluate("document.body.innerText")
    filename = f"search_direct_{idx+1}.txt"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved results to {filename} (length: {len(text)})")
    
    # Save HTML source
    html = await page.evaluate("document.documentElement.outerHTML")
    html_filename = f"search_direct_{idx+1}.html"
    html_filepath = os.path.join(os.path.dirname(__file__), html_filename)
    with open(html_filepath, "w", encoding="utf-8") as f:
        f.write(html)
        
    try:
        screenshot_path = os.path.join(os.path.dirname(__file__), f"screenshot_direct_{idx+1}.png")
        await page.save_screenshot(screenshot_path)
    except Exception as e:
        print("Screenshot error:", e)

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
            # Let's close browser properly
            await browser.stop()
        except Exception:
            pass
        print("Browser stopped.")

if __name__ == '__main__':
    asyncio.run(main())

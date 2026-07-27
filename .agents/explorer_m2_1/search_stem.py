import asyncio
import nodriver as uc
import os

QUERIES = [
    '"Dakahlia STEM School" OR "Dakhlia STEM School" OR "Talkha STEM" OR "Mansoura STEM" contact email phone',
    '"Dakahlia STEM School" OR "Talkha STEM" OR "Mansoura STEM" principal coordinator LinkedIn',
    '"Dakahlia STEM School" OR "Talkha STEM" OR "Mansoura STEM" coordinates location address',
    '"Dakahlia STEM School" OR "Talkha STEM" OR "Mansoura STEM" funding project grant sponsor',
    '"Dakahlia STEM School" OR "Talkha STEM" OR "Mansoura STEM" Egypt site:facebook.com'
]

async def run_search(browser, query, idx):
    print(f"Running search {idx+1}/{len(QUERIES)}: {query}")
    page = await browser.get('https://www.google.com')
    await asyncio.sleep(2)
    
    # Accept cookies if the prompt appears
    try:
        accept_btn = await page.select('button:has-text("Accept all")')
        if accept_btn:
            await accept_btn.click()
            await asyncio.sleep(1)
    except Exception:
        pass

    search_box = await page.select('textarea[name="q"]')
    if not search_box:
        search_box = await page.select('input[name="q"]')
        
    if search_box:
        await search_box.send_keys(query)
        await search_box.send_keys('\n')
        await asyncio.sleep(4)
        
        # Extract text content
        text = await page.evaluate("document.body.innerText")
        filename = f"search_{idx+1}.txt"
        filepath = os.path.join(os.path.dirname(__file__), filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Results for search {idx+1} saved to {filename}")
        
        # Save screenshot for debugging
        try:
            screenshot_path = os.path.join(os.path.dirname(__file__), f"screenshot_{idx+1}.png")
            await page.save_screenshot(screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
        except Exception as e:
            print("Screenshot failed:", e)
    else:
        print(f"Search box not found for search {idx+1}")

async def main():
    print("Starting nodriver...")
    browser = await uc.start(headless=True)
    print("Browser started.")
    try:
        for idx, query in enumerate(QUERIES):
            try:
                await run_search(browser, query, idx)
            except Exception as e:
                print(f"Error running search {idx+1}: {e}")
    finally:
        await browser.stop()
        print("Browser stopped.")

if __name__ == '__main__':
    asyncio.run(main())

import asyncio
import nodriver as uc
import os

async def search_query(page, query):
    print(f"Searching for: {query}")
    try:
        # Navigate to Bing search
        await page.get('https://www.bing.com')
        await asyncio.sleep(4)
        
        # Bing search box
        search_box = await page.select('input[name="q"]')
        if not search_box:
            search_box = await page.select('textarea[name="q"]')
            
        if search_box:
            await search_box.send_keys(query)
            await search_box.send_keys('\n')
            await asyncio.sleep(6)
            text = await page.evaluate("document.body.innerText")
            return text
        else:
            return "Search box not found."
    except Exception as e:
        return f"Error during search: {e}"

async def main():
    print("Starting browser...")
    # nodriver starts a real Chrome instance
    browser = await uc.start(headless=True)
    try:
        page = await browser.get('https://www.bing.com')
        await asyncio.sleep(4)
        
        queries = [
            "Dakahlia STEM School contact phone email",
            "Talkha STEM School principal headteacher coordinator LinkedIn",
            "Mansoura STEM School address coordinates Google Maps",
            "Dakhlia STEM School funding sponsorship projects USAID",
            "Dakahlia STEM School Capstone exhibition"
        ]
        
        results = {}
        for q in queries:
            text = await search_query(page, q)
            results[q] = text
            await asyncio.sleep(4)
            
        with open('browser_results.txt', 'w', encoding='utf-8') as f:
            for q, text in results.items():
                f.write(f"========================================\n")
                f.write(f"QUERY: {q}\n")
                f.write(f"========================================\n")
                f.write(text)
                f.write("\n\n")
                
        print("All searches finished. Saved to browser_results.txt")
    except Exception as e:
        print("Error in main execution loop:", e)
    finally:
        try:
            # stop browser
            browser.stop()
            print("Browser stopped.")
        except Exception as e:
            print("Error stopping browser:", e)

if __name__ == '__main__':
    asyncio.run(main())

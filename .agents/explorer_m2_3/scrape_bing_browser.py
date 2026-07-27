import asyncio
import nodriver as uc
import os
import urllib.parse

async def scrape_query(browser, query):
    print(f"Scraping query directly: {query}")
    try:
        # Create a new tab/page
        page = await browser.get('about:blank')
        await asyncio.sleep(1)
        
        # Navigate directly to the Bing search URL
        url = "https://www.bing.com/search?q=" + urllib.parse.quote(query)
        await page.get(url)
        await asyncio.sleep(6) # Wait for page load and rendering
        
        # Extract the page text
        text = await page.evaluate("document.body.innerText")
        
        # Try to save a screenshot for debugging
        try:
            filename = f"screenshot_{query[:15].replace(' ', '_').replace(':', '_')}.png"
            await page.save_screenshot(filename)
            print(f"Saved screenshot to {filename}")
        except Exception as e:
            print("Screenshot failed:", e)
            
        return text
    except Exception as e:
        return f"Error: {e}"

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
        
        results = {}
        for q in queries:
            res = await scrape_query(browser, q)
            results[q] = res
            await asyncio.sleep(3)
            
        with open('bing_browser_results.txt', 'w', encoding='utf-8') as f:
            for q, text in results.items():
                f.write(f"========================================\n")
                f.write(f"QUERY: {q}\n")
                f.write(f"========================================\n")
                f.write(text)
                f.write("\n\n")
                
        print("All queries processed. Results saved to bing_browser_results.txt")
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

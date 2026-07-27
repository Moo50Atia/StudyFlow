import asyncio
import nodriver as uc

async def main():
    print("Starting nodriver...")
    browser = await uc.start(headless=True)
    print("Browser started.")
    try:
        page = await browser.get('https://www.google.com')
        print("Navigated to google. Waiting for page load...")
        await asyncio.sleep(3)
        
        search_box = await page.select('textarea[name="q"]')
        if not search_box:
            search_box = await page.select('input[name="q"]')
            
        if search_box:
            print("Search box found, sending keys...")
            await search_box.send_keys('Dakahlia STEM School OR Talkha STEM OR Mansoura STEM Egypt contact email phone LinkedIn funding')
            await search_box.send_keys('\n')
            print("Keys sent. Waiting for results...")
            await asyncio.sleep(5)
            
            # Use page.evaluate to get body innerText
            text = await page.evaluate("document.body.innerText")
            print("--- SEARCH RESULTS ---")
            print(text[:5000])
            print("--- END RESULTS ---")
            
            try:
                await page.save_screenshot('search_results.png')
                print("Screenshot saved.")
            except Exception as e:
                print("Screenshot failed:", e)
        else:
            print("Search box not found.")
            # Let's see what the HTML looks like
            html = await page.get_content()
            print("HTML length:", len(html))
            print(html[:1000])
    except Exception as e:
        print("An error occurred during execution:", e)
    finally:
        await browser.stop()

if __name__ == '__main__':
    asyncio.run(main())

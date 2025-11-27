import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from playwright.async_api import async_playwright
from scrapers.luma import LumaScraper
from scrapers.district import DistrictScraper
from scrapers.bookmyshow import BookMyShowScraper
from scrapers.allevents import AllEventsScraper
from scrapers.sortmyscene import SortMySceneScraper
from scrapers.blrtoday import BlrTodayScraper
from scrapers.highape import HighApeScraper

# MongoDB Config
# MongoDB Config
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27018")
DB_NAME = os.getenv("MONGO_DB_NAME", "mp2_db")

async def run_scrapers():
    print("Starting Multi-Source Scraper...")
    
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    scrapers = [
        AllEventsScraper(),
        BookMyShowScraper(),
        HighApeScraper()
    ]
    
    async with async_playwright() as p:
        # Launch with stealthier args
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-infobars',
                '--window-position=0,0',
                '--ignore-certifcate-errors',
                '--ignore-certifcate-errors-spki-list',
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
            ]
        )
        
        for scraper in scrapers:
            print(f"\n--- Running {scraper.name} ---")
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
            )
            page = await context.new_page()
            
            # Add init script to mask webdriver
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """)
            
            try:
                events = await scraper.scrape(page)
                print(f"[{scraper.name}] Extracted {len(events)} events.")
                
                if not events:
                    print(f"[{scraper.name}] No events found. Taking debug screenshot...")
                    await page.screenshot(path=f"/app/debug_{scraper.name.lower()}.png")
                
                if events:
                    count = 0
                    for event in events:
                        # Upsert based on title
                        await db.events_clean.update_one(
                            {"title": event["title"]},
                            {"$set": event},
                            upsert=True
                        )
                        count += 1
                    print(f"[{scraper.name}] Saved {count} events to DB.")
            except Exception as e:
                print(f"[{scraper.name}] Critical Error: {e}")
                await page.screenshot(path=f"/app/error_{scraper.name.lower()}.png")
            finally:
                await context.close()
                
        await browser.close()
    
    print("\nScraping Completed.")
    client.close()

if __name__ == "__main__":
    asyncio.run(run_scrapers())

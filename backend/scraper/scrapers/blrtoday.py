from .base_scraper import BaseScraper
from typing import List, Dict, Any
from playwright.async_api import Page
from datetime import datetime, timedelta
import random

class BlrTodayScraper(BaseScraper):
    def __init__(self):
        super().__init__("BlrToday", "https://blr.today/")

    async def scrape(self, page: Page) -> List[Dict[str, Any]]:
        print(f"[{self.name}] Navigating to {self.base_url}...")
        try:
            await page.goto(self.base_url, timeout=60000)
            try:
                await page.wait_for_load_state("networkidle", timeout=10000)
            except:
                pass
            
            await page.wait_for_timeout(5000)
            
            # Blr.Today selectors
            # Look for list items or articles
            items = await page.query_selector_all("article, li[class*='post']")
            print(f"[{self.name}] Found {len(items)} potential items.")
            
            events = []
            processed_titles = set()
            
            for item in items[:15]:
                try:
                    title_el = await item.query_selector("h2, h3, .entry-title")
                    if not title_el:
                        continue
                        
                    title = await title_el.inner_text()
                    if title in processed_titles or len(title) > 100:
                        continue
                        
                    processed_titles.add(title)
                    
                    # Mock details
                    start_time = datetime.utcnow() + timedelta(days=random.randint(1, 7))
                    lat = 12.97 + random.uniform(-0.05, 0.05)
                    lng = 77.59 + random.uniform(-0.05, 0.05)
                    
                    link_el = await item.query_selector("a")
                    if link_el:
                        href = await link_el.get_attribute("href")
                        link = href if href else self.base_url
                    else:
                        link = self.base_url
                    
                    event = {
                        "title": title,
                        "description": "Curated by Blr.Today.",
                        "source_url": link,
                        "start_time": start_time,
                        "location": {
                            "type": "Point",
                            "coordinates": [lng, lat]
                        },
                        "main_zone": "Bengaluru",
                        "category": "Culture/Art"
                    }
                    events.append(self.clean_event(event))
                except:
                    continue
            return events
        except Exception as e:
            print(f"[{self.name}] Failed: {e}")
            return []

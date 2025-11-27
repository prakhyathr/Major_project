from .base_scraper import BaseScraper
from typing import List, Dict, Any
from playwright.async_api import Page
from datetime import datetime, timedelta
import random

class SortMySceneScraper(BaseScraper):
    def __init__(self):
        super().__init__("SortMyScene", "https://sortmyscene.com/bangalore")

    async def scrape(self, page: Page) -> List[Dict[str, Any]]:
        print(f"[{self.name}] Navigating to {self.base_url}...")
        try:
            await page.goto(self.base_url, timeout=60000)
            try:
                await page.wait_for_load_state("networkidle", timeout=10000)
            except:
                pass
            
            await page.wait_for_timeout(5000)
            
            # SortMyScene selectors
            # Look for event cards
            cards = await page.query_selector_all("a[href*='/event/'], div[class*='card']")
            print(f"[{self.name}] Found {len(cards)} potential cards.")
            
            events = []
            processed_titles = set()
            
            for card in cards[:15]:
                try:
                    text = await card.inner_text()
                    if not text or len(text) < 5:
                        continue
                        
                    lines = [l for l in text.split('\n') if l.strip()]
                    if not lines:
                        continue
                        
                    title = lines[0]
                    if title in processed_titles or len(title) > 100:
                        continue
                        
                    processed_titles.add(title)
                    
                    # Mock details
                    start_time = datetime.utcnow() + timedelta(days=random.randint(1, 14))
                    lat = 12.97 + random.uniform(-0.05, 0.05)
                    lng = 77.59 + random.uniform(-0.05, 0.05)
                    
                    href = await card.get_attribute("href")
                    if href:
                        if href.startswith("/"):
                            link = f"https://sortmyscene.com{href}"
                        else:
                            link = href
                    else:
                        link = self.base_url
                    
                    event = {
                        "title": title,
                        "description": "Discovered on SortMyScene.",
                        "source_url": link,
                        "start_time": start_time,
                        "location": {
                            "type": "Point",
                            "coordinates": [lng, lat]
                        },
                        "main_zone": "Bengaluru",
                        "category": "Party/Nightlife"
                    }
                    events.append(self.clean_event(event))
                except:
                    continue
            return events
        except Exception as e:
            print(f"[{self.name}] Failed: {e}")
            return []

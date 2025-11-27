from .base_scraper import BaseScraper
from typing import List, Dict, Any
from playwright.async_api import Page
from datetime import datetime, timedelta
import random

class DistrictScraper(BaseScraper):
    def __init__(self):
        super().__init__("District", "https://district.in/bangalore")

    async def scrape(self, page: Page) -> List[Dict[str, Any]]:
        print(f"[{self.name}] Navigating to {self.base_url}...")
        try:
            await page.goto(self.base_url, timeout=60000)
            try:
                await page.wait_for_load_state("networkidle", timeout=10000)
            except:
                pass
            
            await page.wait_for_timeout(5000)
            
            # District selectors
            # Look for links that might be events
            cards = await page.query_selector_all("a[href*='/event/'], div[class*='card']")
            print(f"[{self.name}] Found {len(cards)} potential cards.")
            
            events = []
            processed_titles = set()
            
            for card in cards[:15]:
                try:
                    text = await card.inner_text()
                    if not text or len(text) < 10:
                        continue
                        
                    lines = [l for l in text.split('\n') if l.strip()]
                    if len(lines) < 2:
                        continue
                        
                    title = lines[0]
                    if title in processed_titles or len(title) > 100:
                        continue
                        
                    processed_titles.add(title)
                    
                    # Mock details
                    start_time = datetime.utcnow() + timedelta(days=random.randint(1, 14))
                    lat = 12.93 + random.uniform(-0.02, 0.02) # Koramangala area
                    lng = 77.62 + random.uniform(-0.02, 0.02)
                    
                    href = await card.get_attribute("href")
                    if href and href.startswith("/"):
                        link = f"https://district.in{href}"
                    else:
                        link = self.base_url
                    
                    event = {
                        "title": title,
                        "description": "Discovered on District.",
                        "source_url": link,
                        "start_time": start_time,
                        "location": {
                            "type": "Point",
                            "coordinates": [lng, lat]
                        },
                        "main_zone": "Koramangala",
                        "category": "Lifestyle"
                    }
                    events.append(self.clean_event(event))
                except:
                    continue
            return events
        except Exception as e:
            print(f"[{self.name}] Failed: {e}")
            return []

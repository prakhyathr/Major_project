from .base_scraper import BaseScraper
from typing import List, Dict, Any
from playwright.async_api import Page
from datetime import datetime, timedelta
import random

class HighApeScraper(BaseScraper):
    def __init__(self):
        super().__init__("HighApe", "https://highape.com/bangalore/events")

    async def scrape(self, page: Page) -> List[Dict[str, Any]]:
        print(f"[{self.name}] Navigating to {self.base_url}...")
        try:
            await page.goto(self.base_url, timeout=60000)
            try:
                await page.wait_for_load_state("networkidle", timeout=10000)
            except:
                pass
            
            # Scroll a bit to load more
            for _ in range(3):
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(2000)

            # HighApe selectors
            # Look for event cards (often links with specific classes or structure)
            cards = await page.query_selector_all("a[href*='/bangalore/events/']")
            print(f"[{self.name}] Found {len(cards)} potential cards.")
            
            events = []
            processed_urls = set()
            
            for card in cards:
                try:
                    href = await card.get_attribute("href")
                    if not href or href in processed_urls:
                        continue
                        
                    full_link = f"https://highape.com{href}" if href.startswith("/") else href
                    processed_urls.add(href)
                    
                    # Try to extract title
                    title_el = await card.query_selector("h2, h3, .event-name, div[class*='name']")
                    if not title_el:
                        # Fallback: get text from card
                        text = await card.inner_text()
                        lines = [l for l in text.split('\n') if l.strip()]
                        if not lines:
                            continue
                        title = lines[0]
                    else:
                        title = await title_el.inner_text()
                        
                    if len(title) < 3:
                        continue

                    # Mock details
                    start_time = datetime.utcnow() + timedelta(days=random.randint(0, 6))
                    # HighApe focuses on nightlife, often in Indiranagar/Koramangala/MG Road
                    zones = ["Indiranagar", "Koramangala", "MG Road", "HSR Layout"]
                    zone = random.choice(zones)
                    
                    # Approximate coords for these zones
                    coords = {
                        "Indiranagar": [77.6412, 12.9719],
                        "Koramangala": [77.6271, 12.9352],
                        "MG Road": [77.6066, 12.9756],
                        "HSR Layout": [77.6446, 12.9121]
                    }
                    lng, lat = coords[zone]
                    # Add jitter
                    lat += random.uniform(-0.01, 0.01)
                    lng += random.uniform(-0.01, 0.01)
                    
                    event = {
                        "title": title,
                        "description": f"Nightlife event on HighApe. Check details at {full_link}",
                        "source_url": full_link,
                        "start_time": start_time,
                        "location": {
                            "type": "Point",
                            "coordinates": [lng, lat]
                        },
                        "main_zone": zone,
                        "category": "Nightlife/Party"
                    }
                    events.append(self.clean_event(event))
                except:
                    continue
            return events
        except Exception as e:
            print(f"[{self.name}] Failed: {e}")
            return []

from .base_scraper import BaseScraper
from typing import List, Dict, Any
from playwright.async_api import Page
from datetime import datetime, timedelta
import random

class BookMyShowScraper(BaseScraper):
    def __init__(self):
        super().__init__("BookMyShow", "https://in.bookmyshow.com/explore/events-bengaluru")

    async def scrape(self, page: Page) -> List[Dict[str, Any]]:
        print(f"[{self.name}] Navigating to {self.base_url}...")
        try:
            await page.goto(self.base_url, timeout=60000)
            await page.wait_for_timeout(5000)
            
            # Specific selector for event cards based on browser inspection
            # We look for anchor tags that contain '/events/' in their href
            cards = await page.query_selector_all("a[href*='/events/']")
            print(f"[{self.name}] Found {len(cards)} potential event links.")
            
            events = []
            processed_urls = set()
            
            for card in cards:
                try:
                    href = await card.get_attribute("href")
                    if not href or href in processed_urls:
                        continue
                        
                    # Construct full URL
                    if href.startswith("/"):
                        link = f"https://in.bookmyshow.com{href}"
                    else:
                        link = href
                        
                    processed_urls.add(href)
                    
                    # Extract title from within the card
                    # The title is usually in a div or h3 inside the anchor
                    title_el = await card.query_selector("div[class*='sc-'], h3, h4")
                    if title_el:
                        title = await title_el.inner_text()
                    else:
                        # Fallback: get all text and take the first non-empty line
                        text = await card.inner_text()
                        lines = [l for l in text.split('\n') if l.strip()]
                        if lines:
                            title = lines[0]
                        else:
                            title = "Untitled Event"

                    if len(title) < 3 or "View All" in title:
                        continue

                    # Try to get real coords based on title/text
                    # We use the full text of the card to find venue names
                    card_text = await card.inner_text()
                    full_search_text = f"{title} {card_text}"
                    
                    from .zones import get_coords_for_text
                    zone_match = get_coords_for_text(full_search_text)
                    
                    # Mock details
                    start_time = datetime.utcnow() + timedelta(days=random.randint(1, 30))

                    if zone_match:
                        lat_base, lng_base, zone_name = zone_match
                        lat = lat_base + random.uniform(-0.005, 0.005)
                        lng = lng_base + random.uniform(-0.005, 0.005)
                        main_zone = zone_name
                    else:
                        # Fallback: Random location in Bengaluru
                        lat = 12.97 + random.uniform(-0.1, 0.1)
                        lng = 77.59 + random.uniform(-0.1, 0.1)
                        main_zone = "Bengaluru"
                    
                    event = {
                        "title": title,
                        "description": f"Book on BookMyShow: {link}",
                        "source_url": link,
                        "start_time": start_time,
                        "location": {
                            "type": "Point",
                            "coordinates": [lng, lat]
                        },
                        "main_zone": main_zone,
                        "category": "Entertainment"
                    }
                    events.append(self.clean_event(event))
                except Exception as e:
                    print(f"Error extracting event: {e}")
                    continue
            
            return events
        except Exception as e:
            print(f"[{self.name}] Failed: {e}")
            return []

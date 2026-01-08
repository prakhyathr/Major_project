from .base_scraper import BaseScraper
from typing import List, Dict, Any
from playwright.async_api import Page
from datetime import datetime, timedelta
import random

class AllEventsScraper(BaseScraper):
    def __init__(self):
        super().__init__("AllEvents", "https://allevents.in/bangalore")

    async def scrape(self, page: Page) -> List[Dict[str, Any]]:
        category_urls = [
            "https://allevents.in/bangalore/parties",
            "https://allevents.in/bangalore/music",
            "https://allevents.in/bangalore/comedy",
            "https://allevents.in/bangalore/workshops",
            "https://allevents.in/bangalore/business",
            "https://allevents.in/bangalore/sports",
            "https://allevents.in/bangalore/all?ref=cityhome_viewall"
        ]
        
        all_events = []
        seen_urls = set()
        
        for url in category_urls:
            print(f"[{self.name}] Navigating to {url}...")
            try:
                await page.goto(url, timeout=60000)
                try:
                    await page.wait_for_selector(".event-card", timeout=15000)
                except:
                    print(f"[{self.name}] No events found for {url}")
                    continue
                
                # Scroll a bit to trigger lazy loading if any
                for _ in range(3):
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await page.wait_for_timeout(1000)
                
                event_cards = await page.query_selector_all(".event-card")
                print(f"[{self.name}] Found {len(event_cards)} cards in {url.split('/')[-1]}")
                
                for card in event_cards:
                    try:
                        link_el = await card.query_selector("a")
                        href = await link_el.get_attribute("href") if link_el else ""
                        
                        if not href or href in seen_urls:
                            continue
                        seen_urls.add(href)
                        
                        title_el = await card.query_selector(".title h3")
                        title = await title_el.inner_text() if title_el else "Untitled Event"
                        
                        date_el = await card.query_selector(".date")
                        date_text = await date_el.inner_text() if date_el else ""
                        
                        # Extract venue/location text
                        venue_el = await card.query_selector(".subtitle")
                        venue_text = await venue_el.inner_text() if venue_el else ""
                        
                        # Extract Price
                        price_el = await card.query_selector(".price span")
                        price_text = await price_el.inner_text() if price_el else ""
                        price_text = price_text.strip()
                        
                        # Extract Interested Count
                        interested_count = 0
                        audience_el = await card.query_selector(".audience-text")
                        if audience_el:
                            audience_text = await audience_el.inner_text()
                            # Parse "1891+ Interested" -> 1891
                            try:
                                # Remove commas and non-digits
                                import re
                                digits = re.sub(r"[^\d]", "", audience_text)
                                if digits:
                                    interested_count = int(digits)
                            except:
                                pass

                        # Fallback: Use full card text if venue is empty or for better matching
                        card_text = await card.inner_text()
                        full_text = f"{title} {venue_text} {card_text}"
                        
                        # Try to get real coords based on text
                        from .zones import get_coords_for_text
                        zone_match = get_coords_for_text(full_text)
                        
                        # Mock details for demo
                        start_time = datetime.utcnow() + timedelta(days=random.randint(1, 14))
                        
                        if zone_match:
                            lat_base, lng_base, zone_name = zone_match
                            # Add small jitter to avoid exact overlap
                            lat = lat_base + random.uniform(-0.005, 0.005)
                            lng = lng_base + random.uniform(-0.005, 0.005)
                            main_zone = zone_name
                            
                            # If we found a specific venue name (not just a zone), use it
                            # zone_name from get_coords_for_text is either the Venue Name or Zone Name
                            if not venue_text or venue_text == ".":
                                venue_text = zone_name
                        else:
                            # Fallback: Random location in Bengaluru
                            lat = 12.9716 + random.uniform(-0.08, 0.08)
                            lng = 77.5946 + random.uniform(-0.08, 0.08)
                            main_zone = "Bengaluru"
                        
                        category_slug = url.split('/')[-1]
                        category = "General All Categories" if "cityhome_viewall" in category_slug else category_slug.capitalize()
                        
                        event = {
                            "title": title.strip(),
                            "description": f"Scraped from AllEvents ({category}). Venue: {venue_text}. Date: {date_text}",
                            "source_url": href,
                            "start_time": start_time,
                            "location": {
                                "type": "Point",
                                "coordinates": [lng, lat]
                            },
                            "main_zone": main_zone,
                            "category": category,
                            "price_text": price_text,
                            "interested_count": interested_count
                        }
                        all_events.append(self.clean_event(event))
                    except Exception as e:
                        print(f"Error extracting AllEvents event: {e}")
                        continue
                        
            except Exception as e:
                print(f"[{self.name}] Failed to scrape {url}: {e}")
                continue
                
        print(f"[{self.name}] Total unique events scraped: {len(all_events)}")
        return all_events

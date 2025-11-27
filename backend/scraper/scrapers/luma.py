from .base_scraper import BaseScraper
from typing import List, Dict, Any
from playwright.async_api import Page
from datetime import datetime, timedelta
import random

class LumaScraper(BaseScraper):
    def __init__(self):
        super().__init__("Luma", "https://lu.ma/bangalore")

    async def scrape(self, page: Page) -> List[Dict[str, Any]]:
        print(f"[{self.name}] Navigating to {self.base_url}...")
        try:
            await page.goto(self.base_url, timeout=60000)
            # Wait for network idle to ensure dynamic content loads
            try:
                await page.wait_for_load_state("networkidle", timeout=10000)
            except:
                pass
                
            await page.wait_for_timeout(5000) 
            
            # Luma uses very dynamic classes. We'll try to find event cards by:
            # 1. Links containing '/event/'
            # 2. Elements with 'event' in class name
            # 3. Semantic article tags
            
            event_links = await page.query_selector_all("a[href*='/event/']")
            print(f"[{self.name}] Found {len(event_links)} potential event links.")
            
            events = []
            processed_urls = set()
            
            for link in event_links[:15]:
                try:
                    href = await link.get_attribute("href")
                    if not href or href in processed_urls:
                        continue
                        
                    full_link = f"https://lu.ma{href}" if href.startswith("/") else href
                    processed_urls.add(href)
                    
                    # Try to find a title within the link or its parent
                    title_el = await link.query_selector("h3, h2, div[class*='title'], span[class*='title']")
                    if not title_el:
                        # If link itself doesn't have title, maybe it's a card wrapper.
                        # Get text content of the link
                        text = await link.inner_text()
                        lines = [l for l in text.split('\n') if l.strip()]
                        if lines:
                            title = lines[0]
                        else:
                            continue
                    else:
                        title = await title_el.inner_text()
                    
                    if len(title) < 3 or "Register" in title:
                        continue

                    # Mock details
                    start_time = datetime.utcnow() + timedelta(days=random.randint(1, 7))
                    lat = 12.97 + random.uniform(-0.03, 0.03)
                    lng = 77.64 + random.uniform(-0.03, 0.03)
                    
                    event = {
                        "title": title[:100],
                        "description": f"Event on Luma. Check details at {full_link}",
                        "source_url": full_link,
                        "start_time": start_time,
                        "location": {
                            "type": "Point",
                            "coordinates": [lng, lat]
                        },
                        "main_zone": "Indiranagar",
                        "category": "Tech/Meetup"
                    }
                    events.append(self.clean_event(event))
                except Exception as e:
                    print(f"[{self.name}] Error parsing event: {e}")
                    
            return events
            
        except Exception as e:
            print(f"[{self.name}] Failed: {e}")
            return []

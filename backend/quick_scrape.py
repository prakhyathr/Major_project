import requests
from bs4 import BeautifulSoup
import os
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import random
from datetime import datetime, timedelta

# MongoDB Config
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27018")
DB_NAME = os.getenv("MONGO_DB_NAME", "mp2_db")

# Zones for fallback
BENGALURU_ZONES = [
    "Indiranagar", "Koramangala", "Whitefield", "HSR Layout", "Jayanagar",
    "JP Nagar", "Electronic City", "MG Road", "Malleshwaram", "Marathahalli"
]

async def quick_scrape():
    print("Starting Quick Scraper (Requests)...")
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    category_urls = [
        ("https://allevents.in/bangalore/parties", "Parties"),
        ("https://allevents.in/bangalore/music", "Music"),
        ("https://allevents.in/bangalore/comedy", "Comedy"),
        ("https://allevents.in/bangalore/workshops", "Workshops"),
        ("https://allevents.in/bangalore/business", "Business"),
        ("https://allevents.in/bangalore/sports", "Sports")
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    total_saved = 0
    
    for url, category in category_urls:
        print(f"Scraping {category} from {url}...")
        try:
            resp = requests.get(url, headers=headers)
            if resp.status_code != 200:
                print(f"Failed to fetch {url}: {resp.status_code}")
                continue
                
            soup = BeautifulSoup(resp.text, 'html.parser')
            cards = soup.select(".event-card")
            print(f"Found {len(cards)} cards for {category}")
            
            for card in cards:
                try:
                    title_el = card.select_one(".title h3")
                    title = title_el.get_text(strip=True) if title_el else "Untitled Event"
                    
                    link_el = card.select_one("a")
                    href = link_el['href'] if link_el else ""
                    
                    venue_el = card.select_one(".subtitle")
                    venue_text = venue_el.get_text(strip=True) if venue_el else ""
                    
                    date_el = card.select_one(".date")
                    date_text = date_el.get_text(strip=True) if date_el else ""
                    
                    # Simple zone matching
                    main_zone = "Bengaluru"
                    for zone in BENGALURU_ZONES:
                        if zone.lower() in venue_text.lower():
                            main_zone = zone
                            break
                    
                    # Random coords near zone or center
                    lat = 12.9716 + random.uniform(-0.05, 0.05)
                    lng = 77.5946 + random.uniform(-0.05, 0.05)
                    
                    event = {
                        "title": title,
                        "description": f"Scraped from AllEvents ({category}). Venue: {venue_text}. Date: {date_text}",
                        "source_url": href,
                        "start_time": datetime.utcnow() + timedelta(days=random.randint(1, 30)),
                        "location": {
                            "type": "Point",
                            "coordinates": [lng, lat]
                        },
                        "main_zone": main_zone,
                        "category": category
                    }
                    
                    await db.events_clean.update_one(
                        {"title": title},
                        {"$set": event},
                        upsert=True
                    )
                    total_saved += 1
                    
                except Exception as e:
                    print(f"Error parsing card: {e}")
                    
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            
    print(f"Quick Scrape Completed. Saved {total_saved} events.")
    client.close()

if __name__ == "__main__":
    asyncio.run(quick_scrape())

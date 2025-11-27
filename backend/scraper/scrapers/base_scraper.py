from abc import ABC, abstractmethod
from typing import List, Dict, Any
from playwright.async_api import Page
from datetime import datetime

class BaseScraper(ABC):
    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url

    @abstractmethod
    async def scrape(self, page: Page) -> List[Dict[str, Any]]:
        """
        Scrape events from the page.
        Returns a list of event dictionaries.
        """
        pass

    def clean_event(self, raw_event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Common cleaning logic.
        """
        # Ensure required fields
        if "title" not in raw_event:
            raw_event["title"] = "Untitled Event"
        
        if "scraped_at" not in raw_event:
            raw_event["scraped_at"] = datetime.utcnow()
            
        if "source" not in raw_event:
            raw_event["source"] = self.name
            
        return raw_event

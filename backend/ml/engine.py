import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any
import joblib
import os

class MLEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.event_vectors = None
        self.event_ids = []
        self.events_df = None
        self.model_path = "ml_model.joblib"

    def train(self, events: List[Dict[str, Any]]):
        """
        Train the content-based filtering model (TF-IDF on descriptions/titles).
        In a real scenario, this would also train an XGBoost ranker on interaction logs.
        """
        if not events:
            print("No events to train on.")
            return

        self.events_df = pd.DataFrame(events)
        self.event_ids = self.events_df['_id'].astype(str).tolist()
        
        # Create a rich text field for vectorization
        self.events_df['content'] = (
            self.events_df['title'].fillna('') + " " + 
            self.events_df['description'].fillna('') + " " + 
            self.events_df['category'].fillna('') + " " +
            self.events_df['main_zone'].fillna('')
        )
        
        print(f"Training vectorizer on {len(events)} events...")
        self.event_vectors = self.vectorizer.fit_transform(self.events_df['content'])
        print("Training complete.")

    def predict(self, vendor_profile: Dict[str, Any], candidate_events: List[Dict[str, Any]], top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Rank events for a vendor based on:
        1. Content Similarity (Vendor Interests vs Event Content)
        2. Location Proximity (already filtered by DB, but can be re-scored)
        """
        if self.event_vectors is None or not candidate_events:
            return candidate_events[:top_n]

        # 1. Build Vendor Profile Vector
        # Combine vendor interests and category into a query string
        vendor_text = (
            (vendor_profile.get('category') or '') + " " + 
            " ".join(vendor_profile.get('interests', []))
        )
        
        if not vendor_text.strip():
            # Fallback: Return recent events if no profile info
            return candidate_events[:top_n]

        vendor_vector = self.vectorizer.transform([vendor_text])

        # 2. Calculate Similarity with ALL trained events
        # Note: In production, we'd only score the 'candidate_events', but for simplicity
        # we'll assume candidate_events are the ones we trained on or a subset.
        # If candidates are new, we need to transform them on the fly.
        
        # Let's handle the case where candidates might not be in the training set
        # by transforming them now. This is safer for dynamic data.
        
        candidate_df = pd.DataFrame(candidate_events)
        candidate_content = (
            candidate_df['title'].fillna('') + " " + 
            candidate_df['description'].fillna('') + " " + 
            candidate_df['category'].fillna('') + " " +
            candidate_df['main_zone'].fillna('')
        )
        
        candidate_vectors = self.vectorizer.transform(candidate_content)
        
        # Cosine Similarity
        scores = cosine_similarity(vendor_vector, candidate_vectors).flatten()
        
        # 3. Add scores to events and sort
        scored_events = []
        for i, event in enumerate(candidate_events):
            event_with_score = event.copy()
            event_with_score['ml_score'] = float(scores[i])
            scored_events.append(event_with_score)
            
        # Sort by score descending
        scored_events.sort(key=lambda x: x['ml_score'], reverse=True)
        
        return scored_events[:top_n]

ml_engine = MLEngine()

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
from typing import List, Dict, Any
import joblib
import os

class MLEngine:
    def __init__(self):
        # Load a pre-trained model (MiniLM is fast and accurate)
        # This will download ~90MB on first run
        print("Loading BERT model (all-MiniLM-L6-v2)...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.event_embeddings = None
        self.event_ids = []
        self.events_df = None
        self.model_path = "ml_model_bert.joblib"

    def train(self, events: List[Dict[str, Any]]):
        """
        Train the content-based filtering model (BERT Embeddings).
        """
        if not events:
            print("No events to train on.")
            return

        self.events_df = pd.DataFrame(events)
        self.event_ids = self.events_df['_id'].astype(str).tolist()
        
        # Create a rich text field for embedding
        # We emphasize Category and Interests for semantic matching
        self.events_df['content'] = (
            "Category: " + self.events_df['category'].fillna('') + ". " +
            "Title: " + self.events_df['title'].fillna('') + ". " + 
            "Description: " + self.events_df['description'].fillna('') + ". " +
            "Zone: " + self.events_df['main_zone'].fillna('')
        )
        
        print(f"Encoding {len(events)} events with BERT...")
        # Convert to tensor for fast cosine similarity on GPU/CPU
        self.event_embeddings = self.model.encode(self.events_df['content'].tolist(), convert_to_tensor=True)
        print("Encoding complete.")

    def predict(self, vendor_profile: Dict[str, Any], candidate_events: List[Dict[str, Any]], top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Rank events using Semantic Similarity.
        """
        if self.event_embeddings is None or not candidate_events:
            return candidate_events[:top_n]

        # 1. Build Vendor Profile Query
        vendor_text = (
            "Category: " + (vendor_profile.get('category') or '') + ". " + 
            "Interests: " + ", ".join(vendor_profile.get('interests', [])) + "."
        )
        
        # 2. Encode Vendor Profile
        vendor_embedding = self.model.encode(vendor_text, convert_to_tensor=True)

        # 3. Handle Candidate Matching
        # In a real app with static events, we use self.event_embeddings.
        # But if candidate_events allows dynamic filtering, we should map them back to embeddings.
        # For simplicity in this demo, we'll re-encode the specific candidates if they differ from training set
        # OR just assume we are ranking the 'candidate_events' passed in.
        
        # Fast path: If all candidates are in our training set (naive check), use pre-computed
        # For now, let's re-encode candidates to be safe and robust for dynamic lists
        
        candidate_df = pd.DataFrame(candidate_events)
        candidate_content = (
            "Category: " + candidate_df['category'].fillna('') + ". " +
            "Title: " + candidate_df['title'].fillna('') + ". " + 
            "Description: " + candidate_df['description'].fillna('') + ". " +
            "Zone: " + candidate_df['main_zone'].fillna('')
        )
        
        candidate_embeddings = self.model.encode(candidate_content.tolist(), convert_to_tensor=True)
        
        # 4. Calculate Cosine Similarity
        # util.cos_sim returns a matrix [1, N_candidates]
        cosine_scores = util.cos_sim(vendor_embedding, candidate_embeddings)[0]

        # 5. Add scores and sort
        scored_events = []
        for i, event in enumerate(candidate_events):
            event_with_score = event.copy()
            event_with_score['ml_score'] = float(cosine_scores[i])
            scored_events.append(event_with_score)
            
        # Sort by score descending
        scored_events.sort(key=lambda x: x['ml_score'], reverse=True)
        
        return scored_events[:top_n]

ml_engine = MLEngine()

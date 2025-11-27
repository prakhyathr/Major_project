import numpy as np
from sklearn.cluster import DBSCAN
# from hdbscan import HDBSCAN # Optional: Better for variable density

def cluster_events(locations: np.ndarray, eps_km: float = 0.5, min_samples: int = 5):
    """
    Cluster events based on lat/long using DBSCAN.
    locations: (N, 2) array of [lat, long]
    eps_km: The maximum distance between two samples for one to be considered as in the neighborhood of the other.
    """
    # Convert km to radians for haversine metric
    kms_per_radian = 6371.0088
    epsilon = eps_km / kms_per_radian
    
    # Haversine metric requires [lat, long] in radians
    coords = np.radians(locations)
    
    db = DBSCAN(eps=epsilon, min_samples=min_samples, metric='haversine', algorithm='ball_tree')
    db.fit(coords)
    
    return db.labels_

if __name__ == "__main__":
    # Example usage
    data = np.array([
        [12.9716, 77.5946], # Bangalore
        [12.9720, 77.5950], # Nearby
        [13.0000, 77.6000], # Far away
    ])
    labels = cluster_events(data)
    print(f"Cluster labels: {labels}")

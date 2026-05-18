import faiss
import numpy as np
import pickle
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from feature_extractor import FeatureExtractor

class SimilaritySearch:
    def __init__(self):
        print("Loading FAISS index...")
        self.index = faiss.read_index('models/fashion_index.faiss')
        
        with open('models/valid_ids.pkl', 'rb') as f:
            self.valid_ids = pickle.load(f)
        
        self.extractor = FeatureExtractor()
        print(f"✅ Loaded index with {self.index.ntotal} products")

    def search(self, image_path, top_k=5):
        # Extract features from query image
        query_features = self.extractor.extract(image_path)
        
        if query_features is None:
            return []
        
        # Search FAISS index
        query_vector = query_features.reshape(1, -1).astype('float32')
        distances, indices = self.index.search(query_vector, top_k)
        
        # Return product IDs with similarity scores
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.valid_ids):
                results.append({
                    'product_id': self.valid_ids[idx],
                    'similarity_score': float(dist)
                })
        
        return results

# Test
if __name__ == "__main__":
    searcher = SimilaritySearch()
    results = searcher.search("data/images/15970.jpg", top_k=5)
    print("Top 5 similar products:")
    for r in results:
        print(f"  Product {r['product_id']} — Score: {r['similarity_score']:.4f}")
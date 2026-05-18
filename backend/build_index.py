import numpy as np
import faiss
import os
import pickle
import pandas as pd
from tqdm import tqdm
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from feature_extractor import FeatureExtractor

def build_faiss_index():
    extractor = FeatureExtractor()
    
    # Load product list from CSV
    df = pd.read_csv('data/fashion_dataset.csv', on_bad_lines='skip')
    df = df.dropna(subset=['id'])
    
    features_list = []
    valid_ids = []
    
    print(f"Processing {len(df)} images...")
    
    for _, row in tqdm(df.iterrows(), total=len(df)):
        image_path = f"data/images/{int(row['id'])}.jpg"
        
        if os.path.exists(image_path):
            features = extractor.extract(image_path)
            if features is not None:
                features_list.append(features)
                valid_ids.append(int(row['id']))
    
    print(f"✅ Extracted features for {len(features_list)} images")
    
    # Convert to numpy array
    features_matrix = np.array(features_list).astype('float32')
    
    # Build FAISS index
    dimension = 2048
    index = faiss.IndexFlatIP(dimension)  # Inner product = cosine similarity
    index.add(features_matrix)
    
    print(f"✅ FAISS index built with {index.ntotal} vectors")
    
    # Save index and IDs
    os.makedirs('models', exist_ok=True)
    faiss.write_index(index, 'models/fashion_index.faiss')
    
    with open('models/valid_ids.pkl', 'wb') as f:
        pickle.dump(valid_ids, f)
    
    print("✅ Saved FAISS index to models/fashion_index.faiss")
    print("✅ Saved product IDs to models/valid_ids.pkl")

if __name__ == "__main__":
    build_faiss_index()
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from db_connect import get_engine

def load_products():
    # Load CSV
    df = pd.read_csv('data/fashion_dataset.csv', on_bad_lines='skip')
    
    print(f"Total rows loaded: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Clean and select columns
    df_clean = pd.DataFrame({
        'product_id': df['id'],
        'name': df['productDisplayName'],
        'category': df['masterCategory'],
        'sub_category': df['subCategory'],
        'brand': df['brandName'] if 'brandName' in df.columns else 'Unknown',
        'color': df['baseColour'],
        'gender': df['gender'],
        'image_path': df['id'].astype(str) + '.jpg'
    })
    
    # Remove missing values
    df_clean = df_clean.dropna()
    print(f"Clean rows: {len(df_clean)}")
    
    # Load into PostgreSQL
    engine = get_engine()
    df_clean.to_sql(
        'products',
        engine,
        if_exists='append',
        index=False
    )
    
    print(f"✅ Successfully loaded {len(df_clean)} products into PostgreSQL")

if __name__ == "__main__":
    load_products()
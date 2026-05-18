from sqlalchemy import create_engine
import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "fashionlens",
    "user": "postgres",
    "password": "admin123"
}

def get_engine():
    url = f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    return create_engine(url)

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("✅ PostgreSQL connected successfully")
        conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
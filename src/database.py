import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    """Connect to PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def setup_database():
    """Create the weather table if it doesn't exist"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS weather (
                    id SERIAL PRIMARY KEY,
                    city VARCHAR(100),
                    country VARCHAR(100),
                    temperature_c NUMERIC(5,2),
                    wind_kph NUMERIC(5,2),
                    wind_direction VARCHAR(20),
                    humidity INTEGER,
                    condition_text VARCHAR(100),
                    last_updated TIMESTAMP,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            print("Database setup complete!")
        except Exception as e:
            print(f"Error setting up database: {e}")
        finally:
            conn.close()
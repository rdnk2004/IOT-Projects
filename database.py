import os
import sqlite3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Determine if we should use Supabase
use_supabase = False
supabase_client = None

if SUPABASE_URL and SUPABASE_KEY:
    # Filter out empty/placeholder values
    url_clean = SUPABASE_URL.strip()
    key_clean = SUPABASE_KEY.strip()
    if (
        url_clean 
        and "your-project-id" not in url_clean 
        and url_clean.startswith("http")
        and key_clean 
        and "your-supabase-anon" not in key_clean
    ):
        try:
            from supabase import create_client
            supabase_client = create_client(url_clean, key_clean)
            use_supabase = True
            print("Successfully initialized Supabase client.")
        except Exception as e:
            print(f"Failed to initialize Supabase client: {e}. Falling back to local SQLite.")

# SQLite fallback setup
SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), "data.sqlite3")

def init_sqlite():
    """Initializes local SQLite database and creates table if it does not exist."""
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temperature_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            timestamp REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Initialize SQLite database immediately on import
init_sqlite()

def insert_reading(temperature, date_str, time_str, timestamp):
    """
    Inserts a temperature reading into the active database (Supabase or SQLite fallback).
    Returns (success_bool, message_str)
    """
    if use_supabase and supabase_client:
        try:
            data = {
                "temperature": float(temperature),
                "date": date_str,
                "time": time_str,
                "timestamp": float(timestamp)
            }
            # PostgREST insert
            response = supabase_client.table("temperature_readings").insert(data).execute()
            if response.data:
                return True, "Uploaded to Supabase Successfully"
            return False, "Failed to upload to Supabase: Empty response"
        except Exception as e:
            print(f"Supabase upload error: {e}. Attempting SQLite backup...")
            # Fall through to SQLite on failure
            
    # Local SQLite fallback
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO temperature_readings (temperature, date, time, timestamp) VALUES (?, ?, ?, ?)",
            (float(temperature), date_str, time_str, float(timestamp))
        )
        conn.commit()
        conn.close()
        msg = "Saved to local SQLite Successfully"
        if use_supabase:
            msg += " (Supabase upload failed, fallback used)"
        return True, msg
    except Exception as e:
        return False, f"Failed to save to SQLite: {e}"

def get_readings(start_date=None, end_date=None):
    """
    Retrieves temperature records from the active database.
    Optionally filters by start_date and end_date (inclusive, YYYY-MM-DD format).
    Returns a list of dicts, sorted by timestamp descending.
    """
    readings = []
    
    if use_supabase and supabase_client:
        try:
            query = supabase_client.table("temperature_readings").select("*")
            
            # Note: supabase python filters return a builder on which we chain operations
            if start_date:
                query = query.gte("date", start_date)
            if end_date:
                query = query.lte("date", end_date)
                
            response = query.order("timestamp", desc=True).execute()
            if response.data:
                for row in response.data:
                    readings.append({
                        "id": row.get("id"),
                        "temperature": float(row.get("temperature")),
                        "date": row.get("date"),
                        "time": row.get("time"),
                        "timestamp": float(row.get("timestamp"))
                    })
                return readings
        except Exception as e:
            print(f"Failed to query Supabase: {e}. Querying local SQLite instead...")
            
    # SQLite Query
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT id, temperature, date, time, timestamp FROM temperature_readings"
        params = []
        
        conditions = []
        if start_date:
            conditions.append("date >= ?")
            params.append(start_date)
        if end_date:
            conditions.append("date <= ?")
            params.append(end_date)
            
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        query += " ORDER BY timestamp DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        for row in rows:
            readings.append({
                "id": row["id"],
                "temperature": float(row["temperature"]),
                "date": row["date"],
                "time": row["time"],
                "timestamp": float(row["timestamp"])
            })
        conn.close()
    except Exception as e:
        print(f"Error querying SQLite database: {e}")
        
    return readings

import os
from dotenv import load_dotenv

load_dotenv()

# Open-Meteo Weather API Configuration for Kochi
KOCHI_LATITUDE = float(os.getenv("KOCHI_LATITUDE", "9.9312"))
KOCHI_LONGITUDE = float(os.getenv("KOCHI_LONGITUDE", "76.2673"))
KOCHI_TIMEZONE = os.getenv("KOCHI_TIMEZONE", "Asia/Kolkata")
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

# Ingestion Settings
FETCH_INTERVAL_SECONDS = int(os.getenv("FETCH_INTERVAL_SECONDS", "300")) # 5 minutes

# Database Configuration (Supports local SQLite or Cloud Database like Supabase PostgreSQL)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///kochi_weather.db")

# Optional Supabase REST API credentials
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Secret key for Flask app
SECRET_KEY = os.getenv("SECRET_KEY", "kochi_iot_weather_monitoring_secret_key_2026")

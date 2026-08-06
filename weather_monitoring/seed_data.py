from datetime import datetime
import requests
import logging
import config
import database
from fetcher import fetch_kochi_weather

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_past_24h_data():
    """
    Fetches the past 24 hours of hourly weather data from Open-Meteo
    and populates the database so the dashboard has rich historical graphs instantly.
    """
    database.init_db()
    
    logger.info("Checking database for existing readings...")
    latest = database.get_latest_reading()
    
    # Always fetch current weather reading first
    logger.info("Fetching immediate current weather reading...")
    fetch_kochi_weather()
    
    params = {
        "latitude": config.KOCHI_LATITUDE,
        "longitude": config.KOCHI_LONGITUDE,
        "hourly": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
        "past_days": 1,
        "forecast_days": 1,
        "timezone": config.KOCHI_TIMEZONE
    }
    
    try:
        logger.info("Fetching 24h historical weather data from Open-Meteo...")
        response = requests.get(config.OPEN_METEO_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        hourly = data.get("hourly", {})
        times = hourly.get("time", [])
        temps = hourly.get("temperature_2m", [])
        app_temps = hourly.get("apparent_temperature", [])
        humidities = hourly.get("relative_humidity_2m", [])
        wind_speeds = hourly.get("wind_speed_10m", [])
        weather_codes = hourly.get("weather_code", [])
        
        count = 0
        now = datetime.now()
        
        for i in range(len(times)):
            time_str = times[i]
            dt = datetime.fromisoformat(time_str)
            # Only seed data points up to current time
            if dt <= now:
                temp = temps[i] if i < len(temps) else None
                app_temp = app_temps[i] if i < len(app_temps) else None
                hum = humidities[i] if i < len(humidities) else None
                wind = wind_speeds[i] if i < len(wind_speeds) else None
                code = weather_codes[i] if i < len(weather_codes) else None
                
                if temp is not None:
                    database.save_reading(
                        timestamp=dt,
                        temperature=temp,
                        apparent_temperature=app_temp,
                        humidity=hum,
                        wind_speed=wind,
                        weather_code=code
                    )
                    count += 1
                    
        logger.info(f"Successfully seeded {count} historical weather readings for Kochi.")
    except Exception as e:
        logger.error(f"Error seeding historical weather data: {e}")

if __name__ == "__main__":
    seed_past_24h_data()

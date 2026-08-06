from datetime import datetime
import logging
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import config
import database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = None

def fetch_kochi_weather():
    """
    Retrieves current temperature and weather metadata for Kochi from Open-Meteo API
    and persists it into the cloud/local database.
    """
    params = {
        "latitude": config.KOCHI_LATITUDE,
        "longitude": config.KOCHI_LONGITUDE,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
        "timezone": config.KOCHI_TIMEZONE
    }
    
    try:
        response = requests.get(config.OPEN_METEO_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        current = data.get("current", {})
        time_str = current.get("time") # ISO 8601 string, e.g. "2026-08-06T09:30"
        
        if time_str:
            timestamp = datetime.fromisoformat(time_str)
        else:
            timestamp = datetime.now()
            
        temperature = current.get("temperature_2m")
        apparent_temp = current.get("apparent_temperature")
        humidity = current.get("relative_humidity_2m")
        wind_speed = current.get("wind_speed_10m")
        weather_code = current.get("weather_code")
        
        if temperature is not None:
            saved_dict = database.save_reading(
                timestamp=timestamp,
                temperature=temperature,
                apparent_temperature=apparent_temp,
                humidity=humidity,
                wind_speed=wind_speed,
                weather_code=weather_code
            )
            logger.info(f"Successfully fetched and saved Kochi temperature: {temperature}°C at {timestamp}")
            return saved_dict
        else:
            logger.warning("Open-Meteo API response missing temperature_2m data.")
            return None
    except Exception as e:
        logger.error(f"Error fetching weather data from Open-Meteo: {e}")
        return None

def start_weather_scheduler():
    """Starts background APScheduler to regularly fetch Kochi weather."""
    global scheduler
    if scheduler is None:
        scheduler = BackgroundScheduler(daemon=True)
        scheduler.add_job(
            fetch_kochi_weather,
            'interval',
            seconds=config.FETCH_INTERVAL_SECONDS,
            id='kochi_weather_job',
            replace_existing=True
        )
        scheduler.start()
        logger.info(f"Started weather background scheduler (interval: {config.FETCH_INTERVAL_SECONDS}s).")

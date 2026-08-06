import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USGS_ALL_WEEK_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson"

def fetch_usgs_earthquake_data():
    """
    Retrieves GeoJSON earthquake data for the past 7 days from USGS API.
    Returns a list of parsed earthquake record dictionaries.
    """
    try:
        logger.info("Fetching 7-day earthquake telemetry from USGS API...")
        response = requests.get(USGS_ALL_WEEK_URL, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        features = data.get("features", [])
        records = []
        
        for feat in features:
            props = feat.get("properties", {})
            geom = feat.get("geometry", {})
            coords = geom.get("coordinates", [None, None, None])
            
            mag = props.get("mag")
            time_ms = props.get("time")
            
            # Filter valid records with non-null magnitude and timestamp
            if mag is not None and time_ms is not None:
                records.append({
                    "id": feat.get("id"),
                    "magnitude": float(mag),
                    "place": props.get("place", "Unknown Location"),
                    "title": props.get("title", f"M {mag} Earthquake"),
                    "time_ms": time_ms,
                    "url": props.get("url", "#"),
                    "tsunami": props.get("tsunami", 0),
                    "sig": props.get("sig", 0),
                    "longitude": coords[0] if len(coords) > 0 else None,
                    "latitude": coords[1] if len(coords) > 1 else None,
                    "depth_km": coords[2] if len(coords) > 2 else None
                })
                
        logger.info(f"Successfully retrieved {len(records)} earthquake events from USGS.")
        return records
    except Exception as e:
        logger.error(f"Error fetching data from USGS API: {e}")
        return []

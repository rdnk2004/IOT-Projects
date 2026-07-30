import requests
import time
import csv
import os
from datetime import datetime

API_URL = "http://api.open-notify.org/iss-now.json"
DEFAULT_FILENAME = "iss_location_data.csv"

def fetch_iss_location(timeout=5):
    """
    Fetch current ISS location from Open Notify API.
    Returns (timestamp, latitude, longitude) or None if request fails.
    """
    try:
        response = requests.get(API_URL, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            if data.get("message") == "success":
                epoch_ts = data["timestamp"]
                dt_str = datetime.fromtimestamp(epoch_ts).strftime('%Y-%m-%d %H:%M:%S')
                lat = float(data["iss_position"]["latitude"])
                lon = float(data["iss_position"]["longitude"])
                return dt_str, lat, lon
        print(f"API Warning: Unexpected status {response.status_code} or response format.")
    except Exception as e:
        print(f"Network error while fetching ISS data: {e}")
    return None

def collect_iss_data(total_records=100, interval_seconds=5, output_file=DEFAULT_FILENAME):
    """
    Collect consecutive ISS location records and save to CSV.
    """
    print(f"=== Starting ISS Data Collection ({total_records} records every {interval_seconds}s) ===")
    print(f"Output File: {os.path.abspath(output_file)}")
    
    headers = ["Timestamp", "Latitude", "Longitude"]
    
    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        
        records_saved = 0
        consecutive_errors = 0
        
        while records_saved < total_records:
            start_time = time.time()
            record = fetch_iss_location()
            
            if record:
                dt_str, lat, lon = record
                writer.writerow([dt_str, lat, lon])
                csvfile.flush()
                records_saved += 1
                consecutive_errors = 0
                print(f"[{records_saved}/{total_records}] {dt_str} | Lat: {lat:8.4f} | Lon: {lon:8.4f}")
            else:
                consecutive_errors += 1
                print(f"Failed to fetch record. Retry count: {consecutive_errors}")
                if consecutive_errors >= 10:
                    print("Too many consecutive errors. Aborting data collection.")
                    break
            
            if records_saved < total_records:
                elapsed = time.time() - start_time
                sleep_time = max(0.0, interval_seconds - elapsed)
                time.sleep(sleep_time)

    print(f"\nCollection Complete! Total records saved: {records_saved}\n")
    return output_file

if __name__ == "__main__":
    collect_iss_data(total_records=100, interval_seconds=5)

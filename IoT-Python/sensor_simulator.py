import time
import random
from datetime import datetime
import sys

# Import our database router
try:
    import database
except ImportError:
    # Handle paths if run from a different directory level
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import database

def run_sensor_simulator():
    print("==================================================")
    print("      IoT Temperature Sensor Simulator Started     ")
    print("      Generates a reading every 5 seconds.         ")
    print("      Press Ctrl+C to exit.                        ")
    print("==================================================")
    print(f"Database Mode: {'Supabase Cloud' if database.use_supabase else 'Local SQLite Fallback'}")
    print("--------------------------------------------------")

    try:
        while True:
            # Generate random temperature between 20°C and 40°C
            # Rounded to 1 decimal place
            temp = round(random.uniform(20.0, 40.0), 1)
            
            # Get current timestamp, date and time
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")
            timestamp = now.timestamp()
            
            # Upload to database
            success, msg = database.insert_reading(temp, date_str, time_str, timestamp)
            
            if success:
                print(f"Temperature: {temp:.1f}°C | Time: {date_str} {time_str} | {msg}")
            else:
                print(f"Temperature: {temp:.1f}°C | Time: {date_str} {time_str} | FAILED: {msg}", file=sys.stderr)
                
            # Flush output to make sure it displays immediately
            sys.stdout.flush()
            
            # Wait 5 seconds
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nSimulator stopped by user. Exiting...")
    except Exception as e:
        print(f"\nUnexpected error in simulator: {e}", file=sys.stderr)

if __name__ == "__main__":
    run_sensor_simulator()

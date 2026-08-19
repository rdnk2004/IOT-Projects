import os
import random
import time
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    print("Error: Missing SUPABASE_URL or SUPABASE_KEY in environment variables. Please check your .env file.")
    exit(1)

supabase = create_client(url, key)
print("Starting continuous temperature telemetry transmission to Supabase...")

try:
    while True:
        temp = random.randint(25, 40)
        supabase.table("temperature").insert({"temp": temp}).execute()
        print(f"Inserted telemetry reading: {temp} °C")
        time.sleep(5)
except KeyboardInterrupt:
    print("\nTelemetry transmitter stopped by user.")

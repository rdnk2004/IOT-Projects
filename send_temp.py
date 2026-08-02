import os
import random
import time
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key or url == "YOUR_SUPABASE_URL":
    print("Please set SUPABASE_URL and SUPABASE_KEY in your .env file.")
    exit(1)

supabase = create_client(url, key)

while True:
    temp = random.randint(25, 40)
    supabase.table("temperature").insert({"temp": temp}).execute()
    print("Inserted:", temp)
    time.sleep(5)

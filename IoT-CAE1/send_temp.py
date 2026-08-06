import os
import random
import time
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from supabase import create_client
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)
while True:
    temp = random.randint(25, 40)
    supabase.table("temperature").insert({"temp": temp}).execute()
    print("Inserted:", temp)
    time.sleep(5)

import os
from pymongo import MongoClient
from decouple import config

print("Testing database connection...")

# Load URI
env_file = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_file):
    with open(env_file, "r") as f:
        for line in f:
            if line.startswith("MONGODB_URI="):
                uri = line.replace("MONGODB_URI=", "").strip()
                break
else:
    uri = "mongodb://localhost:27017"

print(f"Connecting to: {uri.split('@')[-1] if '@' in uri else uri}")

try:
    # Setup client with short timeout (5s) for quick test
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    
    # Ping
    client.admin.command("ping")
    print("SUCCESS: Connected to MongoDB Atlas successfully!")
    
except Exception as e:
    print("\nFAILURE: Connection failed.")
    print("Error Details:", e)
    print("\nHow to fix:")
    print("1. Go to cloud.mongodb.com")
    print("2. Navigate to Network Access")
    print("3. Add your current IP address to the whitelist.")

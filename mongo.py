import json
import time
import os
from pymongo import MongoClient
from config import MONGO_URI

# ✅ MongoDB Connection
client = MongoClient(MONGO_URI)
db = client["PlantDoctorDB"]
plants_collection = db["plants"]

# ✅ JSON Logs Directory
LOGS_DIR = "hardware/PlantLogs"
last_processed_timestamp = None  # Stores the last inserted timestamp

def get_latest_json_file():
    """Finds the most recent JSON log file in the PlantLogs folder."""
    try:
        files = [f for f in os.listdir(LOGS_DIR) if f.endswith(".json")]
        if not files:
            print("❌ ERROR: No JSON files found in", LOGS_DIR)
            return None

        # Sort files by date (YYYY-MM-DD.json format assumed)
        latest_file = sorted(files)[-1]
        return os.path.join(LOGS_DIR, latest_file)

    except Exception as e:
        print("❌ ERROR: Failed to get latest JSON file -", e)
        return None

def read_json_file(filepath):
    """Reads a JSON file and returns the data"""
    if filepath and os.path.exists(filepath):
        with open(filepath, "r") as file:
            try:
                data = json.load(file)
                if isinstance(data, list):  # Ensure it's a list of entries
                    return data
                else:
                    print("❌ ERROR: JSON file does not contain a list.")
                    return []
            except json.JSONDecodeError:
                print("❌ ERROR: Invalid JSON format in", filepath)
                return []
    else:
        print("❌ ERROR: JSON file not found:", filepath)
        return []

def filter_new_data(data):
    """Filters out already inserted data based on timestamp"""
    global last_processed_timestamp
    if last_processed_timestamp is None:
        # Get the latest timestamp from MongoDB to avoid duplicates on restart
        latest_entry = plants_collection.find_one({}, sort=[("timestamp", -1)])
        last_processed_timestamp = latest_entry["timestamp"] if latest_entry else None

    new_data = []
    for entry in data:
        if last_processed_timestamp is None or entry["timestamp"] > last_processed_timestamp:
            new_data.append(entry)

    if new_data:
        last_processed_timestamp = new_data[-1]["timestamp"]  # Update last processed timestamp
    return new_data

def save_to_mongo(data):
    """Saves only new records to MongoDB efficiently using batch insert."""
    if data:
        result = plants_collection.insert_many(data)
        print(f"✅ Inserted {len(result.inserted_ids)} new records into MongoDB.")

def main():
    """Continuously checks for new JSON logs and inserts only new data into MongoDB."""
    while True:
        latest_file = get_latest_json_file()
        if latest_file:
            data = read_json_file(latest_file)
            new_data = filter_new_data(data)  # Only insert new records
            if new_data:
                save_to_mongo(new_data)
            else:
                print("🔄 No new data to insert.")
        time.sleep(20)  

if __name__ == "__main__":
    main()

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
processed_timestamps = {}  # Stores the last inserted timestamp for each date

TARGET_FILE = "2025-02-09.json"  # Specific file to process

def get_json_files():
    """Returns only the specified JSON file if it exists."""
    file_path = os.path.join(LOGS_DIR, TARGET_FILE)
    if os.path.exists(file_path):
        return [TARGET_FILE]  # Return a list containing only the target file
    else:
        print(f"❌ ERROR: File {TARGET_FILE} not found in {LOGS_DIR}")
        return []

def read_json_file(filepath):
    """Reads a JSON file and returns the data."""
    if filepath and os.path.exists(filepath):
        with open(filepath, "r") as file:
            try:
                data = json.load(file)
                if isinstance(data, list):  # Ensure it's a list of entries
                    return data
                else:
                    print(f"❌ ERROR: JSON file {filepath} does not contain a list.")
                    return []
            except json.JSONDecodeError:
                print(f"❌ ERROR: Invalid JSON format in {filepath}")
                return []
    else:
        print(f"❌ ERROR: JSON file not found: {filepath}")
        return []

def get_last_processed_timestamp(date):
    """Gets the last processed timestamp for a given date from MongoDB."""
    if date not in processed_timestamps:
        latest_entry = plants_collection.find_one({"date": date}, sort=[("timestamp", -1)])
        processed_timestamps[date] = latest_entry["timestamp"] if latest_entry else None
    return processed_timestamps[date]

def filter_new_data(data, date):
    """Filters out already inserted data based on timestamp for the given date."""
    last_processed_timestamp = get_last_processed_timestamp(date)

    new_data = []
    for entry in data:
        if last_processed_timestamp is None or entry["timestamp"] > last_processed_timestamp:
            new_data.append(entry)

    if new_data:
        processed_timestamps[date] = new_data[-1]["timestamp"]  # Update last processed timestamp
    return new_data

def save_to_mongo(data):
    """Saves only new records to MongoDB efficiently using batch insert."""
    if data:
        result = plants_collection.insert_many(data)
        print(f"✅ Inserted {len(result.inserted_ids)} new records into MongoDB.")

def main():
    """Processes only the specified JSON file and inserts new data into MongoDB."""
    json_files = get_json_files()
    if not json_files:
        print("❌ No valid JSON file found. Exiting...")
        return

    json_file = json_files[0]  # Only process `2023-02-09.json`
    file_date = json_file.replace(".json", "")  # Extract date from filename
    file_path = os.path.join(LOGS_DIR, json_file)
    
    data = read_json_file(file_path)
    new_data = filter_new_data(data, file_date)  # Only insert new records for this date
    
    if new_data:
        save_to_mongo(new_data)
    else:
        print(f"🔄 No new data to insert for {file_date}.")

if __name__ == "__main__":
    main()


# MONGO_URI = "mongodb+srv://shatakshiranjan9:adminaccess69@plantdoctor.i6wzb.mongodb.net/"
# client = MongoClient(MONGO_URI)

# try:
#     # Select a database
#     db = client["PlantDoctorDB"]

#     # Select a collection
#     plants_collection = db["plants"]

#     # Insert a sample document
#     new_plant = {"name": "Aloe Vera", "health": "Good", "temperature": 22}
#     insert_result = plants_collection.insert_one(new_plant)
#     print("✅ Plant Added! Document ID:", insert_result.inserted_id)

#     # Fetch and display all plants
#     plants = list(plants_collection.find({}, {"_id": 0}))  # Exclude MongoDB's default "_id"
#     print("\n🌱 List of Plants in Database:")
#     for plant in plants:
#         print(plant)

#     # Delete **ALL** plants in the collection
#     delete_result = plants_collection.delete_many({})  # Deletes all documents

#     if delete_result.deleted_count > 0:
#         print(f"\n🗑️ Deleted {delete_result.deleted_count} plants from the database!")
#     else:
#         print("\n❌ No plants found to delete.")

#     # Fetch and display all plants after deletion (should be empty)
#     plants_after_deletion = list(plants_collection.find({}, {"_id": 0}))
#     print("\n🌱 List of Plants After Deletion (should be empty):")
#     for plant in plants_after_deletion:
#         print(plant)

# except Exception as e:
#     print("❌ MongoDB Connection Failed:", e)

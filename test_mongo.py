from pymongo import MongoClient

MONGO_URI = "mongodb+srv://shatakshiranjan9:adminaccess69@plantdoctor.i6wzb.mongodb.net/"
client = MongoClient(MONGO_URI)

try:
    # Select a database
    db = client["PlantDoctorDB"]

    # Select a collection
    plants_collection = db["plants"]

    # Insert a sample document
    new_plant = {"name": "Aloe Vera", "health": "Good", "temperature": 22}
    insert_result = plants_collection.insert_one(new_plant)
    print("✅ Plant Added! Document ID:", insert_result.inserted_id)

    # Fetch and display all plants
    plants = list(plants_collection.find({}, {"_id": 0}))  # Exclude MongoDB's default "_id"
    print("\n🌱 List of Plants in Database:")
    for plant in plants:
        print(plant)

    # Delete the inserted plant
    delete_result = plants_collection.delete_one({"name": "Aloe Vera", "temperature": 22})

    if delete_result.deleted_count > 0:
        print("\n🗑️ Deleted the inserted plant successfully!")
    else:
        print("\n❌ No matching plant found to delete.")

    # Fetch and display all plants after deletion
    plants_after_deletion = list(plants_collection.find({}, {"_id": 0}))
    print("\n🌱 List of Plants After Deletion:")
    for plant in plants_after_deletion:
        print(plant)

except Exception as e:
    print("❌ MongoDB Connection Failed:", e)


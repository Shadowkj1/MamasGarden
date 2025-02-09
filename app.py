from flask import Flask, render_template, request, send_from_directory, jsonify
from pymongo import MongoClient
import json
import os
from config import MONGO_URI as mongo_uri

app = Flask(__name__)

# Load MongoDB URI
print("🔗 Connecting to MongoDB at:", mongo_uri)

# Test connection using MongoClient
try:
    client = MongoClient(mongo_uri)
    db = client["PlantDoctorDB"]
    db.command("ping")  # Check if the database is accessible
    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print("❌ MongoDB Connection Failed:", e)
    exit(1)

# Collections
plants_collection = db.plants

# Serve fonts
@app.route('/static/fonts/<path:filename>')
def serve_fonts(filename):
    return send_from_directory('static/fonts', filename)

# Home page
@app.route('/')
def home():
    return render_template('main.html')

# Dashboard with latest sensor data
@app.route('/dashboard')
def dashboard():
    latest_data = plants_collection.find().sort("timestamp", -1).limit(10)  # Get latest 10 readings
    return render_template('dashboard.html', plants=latest_data)

# Plant details page
@app.route('/plant')
def plant():
    plant_id = request.args.get('plant')  # Get plant ID from URL
    return render_template('plant.html', plant_id=plant_id)

# API to return latest plant sensor data from MongoDB
@app.route('/get_plants', methods=['GET'])
def get_plants():
    plants = list(plants_collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(10))
    return jsonify(plants)

# ✅ ADDING THE JSON FILE API BELOW
@app.route('/api/plant-logs')
def get_plant_logs():
    """API to serve JSON data from local file (hardware/PlantLogs/2025-02-08.json)"""
    log_file = os.path.join("hardware", "PlantLogs", "2025-02-08.json")
    try:
        with open(log_file, "r") as file:
            data = json.load(file)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

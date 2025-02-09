from flask import Flask, render_template, send_from_directory, jsonify
from pymongo import MongoClient
import os
from config import MONGO_URI as mongo_uri

app = Flask(__name__)

# Load MongoDB URI
print("🔗 Connecting to MongoDB at:", mongo_uri)

# Test connection using MongoClient (instead of Flask-PyMongo)
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

@app.route('/static/fonts/<path:filename>')
def serve_fonts(filename):
    return send_from_directory('static/fonts', filename)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/dashboard')
def dashboard():
    """Displays the latest sensor data"""
    latest_data = plants_collection.find().sort("timestamp", -1).limit(1)  # Get latest 10 readings
    return render_template('dashboard.html', plants=latest_data)

@app.route('/get_plants', methods=['GET'])
def get_plants():
    """API to return latest plant sensor data"""
    plants = list(plants_collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(10))
    return jsonify(plants)

if __name__ == '__main__':
    app.run(debug=True)

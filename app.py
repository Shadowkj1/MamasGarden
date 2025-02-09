from flask import Flask, render_template, request, send_from_directory, jsonify
from pymongo import MongoClient
from google import genai
from random import choice
import json
import os
from config import MONGO_URI as mongo_uri, Gemini_API_KEY

# Initialize Flask App
app = Flask(__name__)

# Initialize Google GenAI Client
genai_client = genai.Client(api_key=Gemini_API_KEY)

# Load MongoDB URI
print("🔗 Connecting to MongoDB at:", mongo_uri)

# Test MongoDB Connection
try:
    client = MongoClient(mongo_uri)
    db = client["PlantDoctorDB"]
    db.command("ping")  # Check if the database is accessible
    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print("❌ MongoDB Connection Failed:", e)
    exit(1)

# MongoDB Collections
plants_collection = db.plants

# Serve fonts
@app.route('/static/fonts/<path:filename>')
def serve_fonts(filename):
    return send_from_directory('static/fonts', filename)

# Home page
@app.route('/')
def home():
    """Home Page"""
    # List of potential prompts to generate diverse responses
    prompts = [
        "Generate an interesting fact about house plants, keep short and sweet",
        "Tell me a surprising fact about indoor plants, keep short and sweet",
        "Share a fun fact about how houseplants improve health, keep short and sweet",
        "Write an amazing fact about air-purifying plants, keep short and sweet",
        "Give me a curious fact about houseplants and their benefits, keep short and sweet"
    ]
    
    # Randomly select a prompt to add variety
    selected_prompt = choice(prompts)
    
    # Generate a plant fact using Google GenAI
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=selected_prompt
        )
        raw_fact = response.text.strip()
        
        # Format the response
        formatted_fact = ""
        lines = raw_fact.split("\n")  # Split by lines in case of multi-line responses
        for line in lines:
            bold_text = ""
            while "**" in line:  # Process bold markers
                start_index = line.index("*")
                end_index = line.index("*", start_index + 2)
                bold_text += "<strong>" + line[start_index + 2:end_index] + "</strong>"
                line = line[:start_index] + bold_text + line[end_index + 2:]
            formatted_fact += line + "<br>"  # Add HTML line breaks for formatting
    except Exception as e:
        print("❌ Error generating plant fact:", e)
        formatted_fact = (
            "Plants are amazing! They improve air quality and brighten up any space.<br>"
        )

    # Pass the formatted fact to the template
    return render_template('main.html', plant_fact=formatted_fact)
@app.route('/dashboard')
def dashboard():
    """Displays the latest sensor data"""
    latest_data = plants_collection.find().sort("timestamp", -1).limit(1)  # Get latest 1 reading
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

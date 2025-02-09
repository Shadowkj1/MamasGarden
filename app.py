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

# ======================== Home Route (Plant Facts) ======================== #
@app.route('/')
def home():
    """Home Page - Displays a random plant fact using Google Gemini AI"""

    # List of potential prompts to generate diverse responses
    prompts = [
        "Generate an interesting fact about house plants, keep it short and sweet",
        "Tell me a surprising fact about indoor plants, keep it short and sweet",
        "Share a fun fact about how houseplants improve health, keep it short and sweet",
        "Write an amazing fact about air-purifying plants, keep it short and sweet",
        "Give me a curious fact about houseplants and their benefits, keep it short and sweet"
    ]
    
    # Select a random prompt
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
        lines = raw_fact.split("\n")  # Split in case of multi-line responses
        for line in lines:
            while "**" in line:  # Process bold markers
                start_index = line.index("**")
                end_index = line.index("**", start_index + 2)
                bold_text = "<strong>" + line[start_index + 2:end_index] + "</strong>"
                line = line[:start_index] + bold_text + line[end_index + 2:]
            formatted_fact += line + "<br>"  # Add HTML line breaks for better display
    except Exception as e:
        print("❌ Error generating plant fact:", e)
        formatted_fact = "Plants are amazing! They improve air quality and brighten up any space.<br>"

    return render_template('main.html', plant_fact=formatted_fact)

# ======================== Dashboard Route ======================== #
@app.route('/dashboard')
def dashboard():
    """Displays the latest sensor data for the plant"""
    latest_data = plants_collection.find().sort("timestamp", -1).limit(1)  # Get latest reading
    
    # Convert MongoDB cursor to a list
    latest_data_list = list(latest_data)
    plant = latest_data_list[0] if latest_data_list else None  # Get the first document or None
    
    return render_template('dashboard.html', plant=plant)  # Pass 'plant' to the template

# ======================== Plant Details Route ======================== #
@app.route('/plant')
def plant():
    """Displays details of a selected plant"""
    plant_id = request.args.get('plant')  # Get plant ID from URL
    return render_template('plant.html', plant_id=plant_id)

# ======================== API: Get Latest Plant Logs from MongoDB ======================== #
@app.route('/api/plant-logs', methods=['GET'])
def get_plant_logs():
    """API to fetch latest plant logs directly from MongoDB"""
    try:
        # Fetch the latest 10 plant sensor records sorted by timestamp
        logs = list(plants_collection.find({}, {"_id": 0}).sort("timestamp", -1))

        if not logs:
            return jsonify({"error": "No plant log data found in MongoDB"}), 404

        return jsonify(logs)  # Send as JSON response
    except Exception as e:
        print(f"❌ Error fetching plant logs from MongoDB: {e}")
        return jsonify({"error": str(e)}), 500


# ======================== API: AI Smart Recommendation ======================== #
@app.route('/get_recommendation', methods=['GET'])
def get_recommendation():
    """Fetch latest Bonsai data and get a recommendation from Gemini AI"""
    latest_data = plants_collection.find_one({}, sort=[("timestamp", -1)])  # Get latest plant data

    if not latest_data:
        print("⚠️ No plant data found in MongoDB!")
        return jsonify({"recommendation": "No data available at the moment."})

    print("📊 Latest Bonsai Data:", latest_data)  # Debugging print statement

    # Ensure required keys exist in the MongoDB document
    required_keys = ["temperatureF", "humidity", "light", "moisture", "waterLevel"]
    for key in required_keys:
        if key not in latest_data:
            latest_data[key] = "N/A"  # Default to "N/A" if missing

    # Format plant data for AI prompt
    plant_prompt = (
        f"Given this latest Bonsai plant data:\n"
        f"- **Temperature:** {latest_data['temperatureF']}°F\n"
        f"- **Humidity:** {latest_data['humidity']}%\n"
        f"- **Light Level:** {latest_data['light']} lux\n"
        f"- **Moisture Level:** {latest_data['moisture']}%\n"
        f"- **Water Level:** {latest_data['waterLevel']}cm\n\n"
        f"What should I do to maintain my Bonsai's health?"
    )

    print("📢 Sending this prompt to Gemini AI:\n", plant_prompt)

    try:
        # Get recommendation from Gemini AI
        response = genai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=plant_prompt
        )
        raw_recommendation = response.text.strip()

        # Format the response
        formatted_recommendation = ""
        lines = raw_recommendation.split("\n")  # Split by new lines
        for line in lines:
            while "**" in line:  # Process bold markers
                start_index = line.index("**")
                end_index = line.index("**", start_index + 2)
                bold_text = "<strong>" + line[start_index + 2:end_index] + "</strong>"
                line = line[:start_index] + bold_text + line[end_index + 2:]
            formatted_recommendation += line + "<br>"  # Add HTML line breaks

    except Exception as e:
        print("❌ Gemini AI Error:", e)
        formatted_recommendation = "Unable to generate a recommendation at this time."

    return jsonify({"recommendation": formatted_recommendation})


# ======================== Run Flask App ======================== #
if __name__ == '__main__':
    app.run(debug=True)

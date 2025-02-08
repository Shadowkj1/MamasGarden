from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
import config  # Import config.py
from marshmallow import ValidationError
from pymongo.errors import ServerSelectionTimeoutError

app = Flask(__name__)

# Configure MongoDB from config.py
app.config["MONGO_URI"] = config.MONGO_URI
mongo = PyMongo(app)

# Test MongoDB Connection
try:
    db = mongo.db
    plants_collection = db.plants  # Ensure the collection is accessible

    # Ping MongoDB to verify connection
    mongo.cx.admin.command('ping')
    print("✅ SUCCESS: MongoDB connected!")

except ServerSelectionTimeoutError:
    print("❌ ERROR: MongoDB connection timed out! Check if MongoDB Atlas is accessible.")
    exit(1)

except Exception as e:
    print("❌ ERROR: MongoDB connection failed!", e)
    exit(1)  # Stop execution if MongoDB connection fails

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/dashboard')
def dashboard():
    plants = list(plants_collection.find({}, {"_id": 0}))  # Fetch data
    return render_template('dashboard.html', plants=plants)

# 🌱 API Endpoint to Add a Plant (With Validation)
@app.route('/add_plant', methods=['POST'])
def add_plant():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Validate data using schema
    try:
        validated_data = config.plant_schema.load(data)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    # Insert into MongoDB
    plant_id = plants_collection.insert_one(validated_data).inserted_id
    return jsonify({"message": "Plant added!", "plant_id": str(plant_id)}), 201

# 🌱 API Endpoint to Get All Plants
@app.route('/get_plants', methods=['GET'])
def get_plants():
    plants = list(plants_collection.find({}, {"_id": 0}))
    return jsonify(plants)

if __name__ == '__main__':
    app.run(debug=True)


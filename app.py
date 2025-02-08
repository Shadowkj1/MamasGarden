from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
import config  # Import config.py

app = Flask(__name__)

# Check if MONGO_URI is correctly loaded
print("MongoDB URI:", config.MONGO_URI)  # Debugging

# Configure MongoDB from config.py
app.config["MONGO_URI"] = config.MONGO_URI
mongo = PyMongo(app)

# Ensure MongoDB is connected
if not mongo.db:
    print("❌ ERROR: MongoDB connection failed!")
    exit(1)  # Stop Flask from running if MongoDB fails

# Collections
db = mongo.db
plants_collection = db.plants  # Example collection

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/dashboard')
def dashboard():
    plants = list(plants_collection.find({}, {"_id": 0}))  # Fetch data
    return render_template('dashboard.html', plants=plants)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, send_from_directory
from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
import config

app = Flask(__name__)
app.config["MONGO_URI"] = config.MONGO_URI
mongo = PyMongo(app)

# Collections
db = mongo.db
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
    latest_data = plants_collection.find().sort("timestamp", -1).limit(10)  # Get latest 10 readings
    return render_template('dashboard.html', plants=latest_data)

@app.route('/get_plants', methods=['GET'])
def get_plants():
    """API to return latest plant sensor data"""
    plants = list(plants_collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(10))
    return jsonify(plants)

if __name__ == '__main__':
    app.run(debug=True)


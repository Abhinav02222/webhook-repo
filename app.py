from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

app = Flask(_name_)
load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))  # Connects to MongoDB
db = client["webhookDB"]
collection = db["events"]

@app.route('/events', methods=['GET'])
def get_events():
    recent_events = collection.find().sort('timestamp', -1).limit(10)
    output = []
    for event in recent_events:
        output.append({
            "type": event.get("type"),
            "repo": event.get("repository", {}).get("full_name"),
            "branch": event.get("ref", "").split("/")[-1],
            "timestamp": event.get("timestamp").strftime("%Y-%m-%d %H:%M:%S UTC")
        })
    return jsonify(output)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"message": "No data received"}), 400

    payload = {
        "event_type": request.headers.get('X-GitHub-Event'),
        "timestamp": datetime.utcnow().isoformat(),
        "raw_data": data
    }

    collection.insert_one(payload)
    return jsonify({"message": "Webhook received"}), 200

if _name_ == '_main_':
    app.run(port=5000, debug=True)
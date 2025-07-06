from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

client = MongoClient("mongodb+srv://abhinavbehera2001:#Abhinav2001@cluster0.ixvnta3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # Connects to MongoDB
db = client["webhookDB"]
collection = db["events"]

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

if __name__ == '__main__':
    app.run(port=5000, debug=True)
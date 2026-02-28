from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os


# ======================
# LOAD ENV FILE
# ======================
load_dotenv()


# ======================
# FLASK APP SETUP
# ======================
app = Flask(__name__)


# ======================
# MONGODB CONNECTION
# ======================
MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017")

client = MongoClient(MONGO_URI)

db = client.notes_app

notes = db.notes


# ======================
# HOME / NOTES PAGE
# ======================
@app.route("/")
@app.route("/notes")
def notes_page():

    return render_template("index.html")


# ======================
# API - GET NOTES
# ======================
@app.route("/api/notes", methods=["GET"])
def get_notes():

    data = list(notes.find())

    for note in data:
        note["_id"] = str(note["_id"])

    return jsonify(data)


# ======================
# API - CREATE NOTE
# ======================
@app.route("/api/notes", methods=["POST"])
def create_note():

    data = request.json

    notes.insert_one({
        "title": data.get("title"),
        "content": data.get("content")
    })

    return jsonify({"status": "created"})


# ======================
# API - UPDATE NOTE
# ======================
@app.route("/api/notes/<id>", methods=["PUT"])
def update_note(id):

    data = request.json

    notes.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "title": data.get("title"),
                "content": data.get("content")
            }
        }
    )

    return jsonify({"status": "updated"})


# ======================
# API - DELETE NOTE
# ======================
@app.route("/api/notes/<id>", methods=["DELETE"])
def delete_note(id):

    notes.delete_one({"_id": ObjectId(id)})

    return jsonify({"status": "deleted"})


# ======================
# RUN APP
# ======================
if __name__ == "__main__":
    app.run(debug=True)
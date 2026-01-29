from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

#  MongoDB Atlas connection (Vercel-compatible)
client = MongoClient(os.environ.get("MONGODB_URI_"))
db = client["NotesApp"]
notes_col = db["notes"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/notes", methods=["GET"])
def get_notes():
    notes = []
    for n in notes_col.find().sort("_id", -1):
        notes.append({
            "_id": str(n["_id"]),
            "title": n.get("title", ""),
            "content": n.get("content", "")
        })
    return jsonify(notes), 200


@app.route("/api/notes", methods=["POST"])
def add_note():
    data = request.get_json()
    title = data.get("title", "").strip()
    content = data.get("content", "").strip()

    if not title and not content:
        return jsonify({"error": "Note cannot be empty"}), 400

    res = notes_col.insert_one({
        "title": title,
        "content": content
    })

    return jsonify({
        "_id": str(res.inserted_id),
        "title": title,
        "content": content
    }), 201


@app.route("/api/notes/<note_id>", methods=["PUT"])
def update_note(note_id):
    data = request.get_json()
    notes_col.update_one(
        {"_id": ObjectId(note_id)},
        {"$set": {
            "title": data.get("title", ""),
            "content": data.get("content", "")
        }}
    )
    return jsonify({"message": "Updated"}), 200


@app.route("/api/notes/<note_id>", methods=["DELETE"])
def delete_note(note_id):
    notes_col.delete_one({"_id": ObjectId(note_id)})
    return jsonify({"message": "Deleted"}), 200

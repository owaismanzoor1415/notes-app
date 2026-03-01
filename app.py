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
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI not found in environment variables")

client = MongoClient(MONGO_URI)

db = client.notes_app

notes = db.notes


# ======================
# HOME PAGE
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

    try:

        data = list(notes.find().sort("_id", -1))

        for note in data:
            note["_id"] = str(note["_id"])

        return jsonify(data), 200

    except Exception as e:

        print("GET ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ======================
# API - CREATE NOTE
# ======================
@app.route("/api/notes", methods=["POST"])
def create_note():

    try:

        # force=True ensures JSON works on Render/Gunicorn
        data = request.get_json(force=True)

        print("Incoming data:", data)

        title = data.get("title", "")
        content = data.get("content", "")

        if not title and not content:
            return jsonify({
                "status": "error",
                "message": "Note cannot be empty"
            }), 400

        result = notes.insert_one({
            "title": title,
            "content": content
        })

        return jsonify({
            "status": "created",
            "id": str(result.inserted_id)
        }), 201

    except Exception as e:

        print("POST ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ======================
# API - UPDATE NOTE
# ======================
@app.route("/api/notes/<id>", methods=["PUT"])
def update_note(id):

    try:

        data = request.get_json(force=True)

        notes.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "title": data.get("title", ""),
                    "content": data.get("content", "")
                }
            }
        )

        return jsonify({"status": "updated"}), 200

    except Exception as e:

        print("PUT ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ======================
# API - DELETE NOTE
# ======================
@app.route("/api/notes/<id>", methods=["DELETE"])
def delete_note(id):

    try:

        notes.delete_one({"_id": ObjectId(id)})

        return jsonify({"status": "deleted"}), 200

    except Exception as e:

        print("DELETE ERROR:", e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ======================
# RUN APP
# ======================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
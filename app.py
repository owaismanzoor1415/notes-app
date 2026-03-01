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
# FLASK APP
# ======================
app = Flask(__name__)


# ======================
# SAFE MONGODB CONNECTION (RENDER FIX)
# ======================
def get_db():

    mongo_uri = os.getenv("MONGO_URI")

    if not mongo_uri:
        raise RuntimeError("MONGO_URI not set")

    client = MongoClient(mongo_uri)

    return client.notes_app.notes


# ======================
# HOME PAGE
# ======================
@app.route("/")
@app.route("/notes")
def notes_page():
    return render_template("index.html")


# ======================
# GET NOTES
# ======================
@app.route("/api/notes", methods=["GET"])
def get_notes():

    try:

        notes = get_db()

        data = list(notes.find().sort("_id", -1))

        for note in data:
            note["_id"] = str(note["_id"])

        return jsonify(data), 200

    except Exception as e:

        print("GET ERROR:", e)

        return jsonify({"error": str(e)}), 500


# ======================
# CREATE NOTE
# ======================
@app.route("/api/notes", methods=["POST"])
def create_note():

    try:

        notes = get_db()

        data = request.get_json(force=True)

        print("POST DATA:", data)

        result = notes.insert_one({
            "title": data.get("title", ""),
            "content": data.get("content", "")
        })

        return jsonify({
            "status": "created",
            "id": str(result.inserted_id)
        }), 201

    except Exception as e:

        print("POST ERROR:", e)

        return jsonify({
            "error": str(e)
        }), 500


# ======================
# DELETE NOTE
# ======================
@app.route("/api/notes/<id>", methods=["DELETE"])
def delete_note(id):

    try:

        notes = get_db()

        notes.delete_one({"_id": ObjectId(id)})

        return jsonify({"status": "deleted"}), 200

    except Exception as e:

        print("DELETE ERROR:", e)

        return jsonify({"error": str(e)}), 500


# ======================
# RUN APP
# ======================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
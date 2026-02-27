from flask import Flask, render_template, request, redirect, session, url_for, jsonify
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

# Secret key from .env
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret")


# ======================
# MONGODB CONNECTION
# ======================
MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017")

client = MongoClient(MONGO_URI)

db = client.notes_app

users = db.users
notes = db.notes


# ======================
# LOGIN
# ======================
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = users.find_one({
            "email": email,
            "password": password
        })

        if user:
            session["user_id"] = str(user["_id"])
            session["email"] = user["email"]

            return redirect("/notes")

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


# ======================
# REGISTER
# ======================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match")

        existing_user = users.find_one({"email": email})

        if existing_user:
            return render_template("register.html", error="User already exists")

        users.insert_one({
            "email": email,
            "password": password
        })

        return redirect("/")

    return render_template("register.html")

# ======================
# LOGOUT
# ======================
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

# ======================
# NOTES PAGE
# ======================
@app.route("/notes")
def notes_page():

    if "user_id" not in session:
        return redirect("/")

    return render_template("index.html", email=session.get("email"))


# ======================
# API - GET NOTES
# ======================
@app.route("/api/notes", methods=["GET"])
def get_notes():

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session["user_id"]

    data = list(notes.find({"user_id": user_id}))

    for note in data:
        note["_id"] = str(note["_id"])

    return jsonify(data)


# ======================
# API - CREATE NOTE
# ======================
@app.route("/api/notes", methods=["POST"])
def create_note():

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json

    notes.insert_one({
        "title": data.get("title"),
        "content": data.get("content"),
        "user_id": session["user_id"]
    })

    return jsonify({"status": "created"})


# ======================
# API - UPDATE NOTE
# ======================
@app.route("/api/notes/<id>", methods=["PUT"])
def update_note(id):

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json

    notes.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "title": data.get("title"),
            "content": data.get("content")
        }}
    )

    return jsonify({"status": "updated"})


# ======================
# API - DELETE NOTE
# ======================
@app.route("/api/notes/<id>", methods=["DELETE"])
def delete_note(id):

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    notes.delete_one({
        "_id": ObjectId(id)
    })

    return jsonify({"status": "deleted"})


# ======================
# RUN APP
# ======================
if __name__ == "__main__":

    app.run(debug=True)
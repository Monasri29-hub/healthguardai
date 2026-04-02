from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import pickle
import numpy as np

app = Flask(__name__)
@app.route("/")
def home():
    return "Backend is running successfully!"
CORS(app)

model = pickle.load(open("model.pkl","rb"))

# ---------------- DB ----------------
def db():
    return sqlite3.connect("database.db")

def init():
    con = db()
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        email TEXT,
        password TEXT,
        phone TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS history(
        email TEXT,
        age INT,
        bmi INT,
        glucose INT,
        bp INT,
        result TEXT,
        score REAL
    )""")

    con.commit()
    con.close()

init()

# ---------------- AUTH ----------------
@app.route("/signup", methods=["POST"])
def signup():
    d = request.json
    con = db()
    cur = con.cursor()
    cur.execute("INSERT INTO users VALUES (?,?,?)",
                (d["email"], d["password"], d["phone"]))
    con.commit()
    con.close()
    return jsonify({"msg":"Signup success"})

@app.route("/login", methods=["POST"])
def login():
    d = request.json
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE email=? AND password=?",
                (d["email"], d["password"]))
    user = cur.fetchone()
    con.close()
    return jsonify({"status":"ok" if user else "fail"})

# ---------------- PREDICTION ----------------
@app.route("/predict", methods=["POST"])
def predict():
    d = request.json

    X = np.array([[d["age"], d["bmi"], d["glucose"], d["bp"]]])
    pred = model.predict(X)[0]
    prob = model.predict_proba(X)[0][1]

    result = "High Risk" if pred else "Low Risk"

    con = db()
    cur = con.cursor()
    cur.execute("INSERT INTO history VALUES (?,?,?,?,?,?,?)",
                (d["email"], d["age"], d["bmi"], d["glucose"], d["bp"], result, prob))
    con.commit()
    con.close()

    emergency = True if prob > 0.8 else False

    return jsonify({
        "result": result,
        "score": round(prob*100,2),
        "emergency": emergency
    })

# ---------------- CHATBOT ----------------
@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("msg", "").lower()

    if "diet" in msg:
        reply = """Diet Plan:
• Eat vegetables & fruits
• Avoid sugar & junk food
• Drink plenty of water
• Eat whole grains"""

    elif "exercise" in msg:
        reply = """Exercise Tips:
• Walk 30 minutes daily
• Do light cardio
• Try yoga or stretching"""

    elif "diabetes" in msg:
        reply = """Diabetes is a condition where blood sugar levels are too high.
It can be controlled with diet, exercise, and medication."""

    elif "high risk" in msg:
        reply = """If you have high risk:
• Reduce sugar intake
• Exercise daily
• Monitor glucose levels
• Consult a doctor"""

    elif "hello" in msg or "hi" in msg:
        reply = "Hello! Ask me about diet, exercise, or diabetes."

    else:
        reply = "I can help with diet, exercise, diabetes, or risk advice."

    return jsonify({"reply": reply})
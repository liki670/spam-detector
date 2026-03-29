from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

# Initialize app
app = Flask(__name__)
CORS(app)  # Allow frontend (Vercel) to access backend

# Load model and vectorizer
try:
    model = pickle.load(open("model.pkl", "rb"))
    vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
except Exception as e:
    print("Error loading model:", e)

# Home route
@app.route("/")
def home():
    return "Spam Detector Backend Running"

# Prediction route
@app.route("/check", methods=["POST"])
def check_spam():
    try:
        data = request.get_json()
        text = data.get("text", "")

        if text.strip() == "":
            return jsonify({"result": "Empty input"}), 400

        # Transform input
        vector = vectorizer.transform([text])

        # Predict
        prediction = model.predict(vector)[0]

        result = "Spam" if prediction == 1 else "Not Spam"

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
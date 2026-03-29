from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)

# Load model + vectorizer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

@app.route("/")
def home():
    return "Spam Detector Backend Running 🚀"

@app.route("/check", methods=["POST"])
def check_spam():
    text = request.json["text"]

    # Convert text → numbers
    vect = vectorizer.transform([text])

    # Predict
    prediction = model.predict(vect)[0]

    result = "Spam" if prediction == 1 else "Not Spam"

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
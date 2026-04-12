from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# ================= ML MODELS =================
model = pickle.load(open("model.pkl", "rb"))
preprocessor = pickle.load(open("preprocessor.pkl", "rb"))
label_encoder = pickle.load(open("label_encoder.pkl", "rb"))

# ================= ROUTES =================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/cropprediction")
def crop():
    return render_template("cropprediction.html")

@app.route("/analytics")
def analytics():
    return render_template("analytics.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# ================= ML PREDICTION =================

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    input_data = pd.DataFrame([{
        "Temperature": data["temperature"],
        "Humidity": data["humidity"],
        "Rainfall": data["rainfall"],
        "PH": data["ph"],
        "Nitrogen": data["nitrogen"],
        "Phosphorous": data["phosphorus"],
        "Potassium": data["potassium"],
        "Carbon": data["carbon"],
        "Soil": data["soil"]
    }])

    processed = preprocessor.transform(input_data)
    prediction = model.predict(processed)
    crop = label_encoder.inverse_transform(prediction)[0]

    return jsonify({"crop": crop})

# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)
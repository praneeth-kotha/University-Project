from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)

# LOAD MODEL
model = None
preprocessor = None
label_encoder = None

try:
    print("📁 Current directory:", os.getcwd())

    model = joblib.load("model.pkl")
    preprocessor = joblib.load("preprocessor.pkl")
    label_encoder = joblib.load("label_encoder.pkl")

    print("✅ Models loaded successfully")

except Exception as e:
    print("❌ Error loading models:", e)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        if model is None:
            return jsonify({"error": "Model not loaded"}), 500

        data = request.get_json()

        input_data = pd.DataFrame([{
            "Temperature": float(data["temperature"]),
            "Humidity": float(data["humidity"]),
            "Rainfall": float(data["rainfall"]),
            "PH": float(data["ph"]),
            "Nitrogen": float(data["nitrogen"]),
            "Phosphorous": float(data["phosphorus"]),
            "Potassium": float(data["potassium"]),
            "Carbon": float(data["carbon"]),
            "Soil": str(data["soil"]).lower().strip()
        }])

        processed = preprocessor.transform(input_data)
        prediction = model.predict(processed)
        crop = label_encoder.inverse_transform(prediction)[0]

        return jsonify({"crop": crop})

    except Exception as e:
        print("❌ Prediction error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

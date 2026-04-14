import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

print("📁 Current folder:", os.getcwd())

# ================= LOAD DATA =================
df = pd.read_csv("crop_recommendation_dataset_2.csv")

print("✅ Dataset loaded")
print("Shape:", df.shape)

# ================= FEATURES =================
X = df.drop("Crop", axis=1)
y = df["Crop"]

# ================= ENCODE =================
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# ================= PREPROCESS =================
numeric_cols = [
    "Temperature", "Humidity", "Rainfall", "PH",
    "Nitrogen", "Phosphorous", "Potassium", "Carbon"
]

categorical_cols = ["Soil"]

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numeric_cols),
    ("cat", OneHotEncoder(handle_unknown='ignore'), categorical_cols)
])

# ================= SPLIT =================
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)

# ================= TRANSFORM =================
X_train = preprocessor.fit_transform(X_train)
X_test = preprocessor.transform(X_test)

# ================= MODEL (FINAL FIX) =================
model = RandomForestClassifier(
    n_estimators=60,       # 🔥 balanced size
    max_depth=10,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)

# ================= TRAIN =================
model.fit(X_train, y_train)

print("✅ Model trained")

# ================= EVALUATE =================
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"🎯 Accuracy: {accuracy*100:.2f}%")

# ================= SAVE =================
joblib.dump(model, "model.pkl", compress=3)
joblib.dump(preprocessor, "preprocessor.pkl", compress=3)
joblib.dump(label_encoder, "label_encoder.pkl", compress=3)

print("✅ Files saved successfully")
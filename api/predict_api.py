from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import uvicorn
import os

# Get the current directory and construct absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "..", "models", "churn_model.pkl")
encoders_path = os.path.join(current_dir, "..", "models", "label_encoders.pkl")

# Load model and encoders
model = joblib.load(model_path)
label_encoders = joblib.load(encoders_path)

# Request schema
class SubscriptionInput(BaseModel):
    service_name: str
    category: str
    monthly_cost: float
    login_frequency: int
    time_spent: float
    feature_usage: float

# Init FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "🟢 Churn Prediction API is running!"}

@app.post("/predict")
def predict_churn(data: SubscriptionInput):
    try:
        service_encoded = label_encoders["service_name"].transform([data.service_name])[0]
        category_encoded = label_encoders["category"].transform([data.category])[0]
    except ValueError as e:
        return {"error": f"Invalid service or category: {e}"}

    # Prepare features
    features = np.array([[ 
        data.monthly_cost,
        data.login_frequency,
        data.time_spent,
        data.feature_usage,
        service_encoded,
        category_encoded
    ]])

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]

    prediction_label = label_encoders["churned"].inverse_transform([prediction])[0]

    return {
        "prediction": prediction_label,
        "probability": round(probability, 2)
    }

# For local development
if __name__ == "__main__":
    uvicorn.run("predict_api:app", host="0.0.0.0", port=8000, reload=True)

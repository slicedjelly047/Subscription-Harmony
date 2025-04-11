import os
from dotenv import load_dotenv
from pymongo import MongoClient
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load .env
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

# MongoDB setup
client = MongoClient(MONGODB_URI)
db = client["subscriptionApp"]
collection = db["subscription_data"]

# Fetch data from MongoDB
cursor = collection.find({})
df = pd.DataFrame(list(cursor))

# Drop MongoDB ID if present
df.drop(columns=['_id'], inplace=True, errors='ignore')

# Encode categorical columns
label_encoders = {}
for col in ["service_name", "category", "churned"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Feature columns
feature_cols = [
    "monthly_cost",
    "login_frequency",
    "time_spent",
    "feature_usage",
    "service_name",
    "category"
]
X = df[feature_cols]
y = df["churned"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and encoders
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/churn_model.pkl")
joblib.dump(label_encoders, "models/label_encoders.pkl")

print("\nModel trained and saved to models/churn_model.pkl")

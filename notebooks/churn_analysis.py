import os
from dotenv import load_dotenv
from pymongo import MongoClient
import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

# Load environment
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

# MongoDB connection
client = MongoClient(MONGODB_URI)
db = client["subscriptionApp"]
collection = db["subscription_data"]

# Load data from MongoDB
df = pd.DataFrame(list(collection.find()))
df.drop(columns=['_id'], inplace=True, errors='ignore')

# Load model and encoders
model = joblib.load("models/churn_model.pkl")
label_encoders = joblib.load("models/label_encoders.pkl")

# Store original churned values before encoding
original_churned = df["churned"].copy()

# Encode categorical features
for col in ["service_name", "category", "churned"]:
    df[col] = label_encoders[col].transform(df[col])

# Feature columns (same as used during training)
feature_cols = [
    "monthly_cost",
    "login_frequency",
    "time_spent",
    "feature_usage",
    "service_name",
    "category"
]
X = df[feature_cols]

# Predict churn
df["churn_predicted"] = model.predict(X)

# Decode predicted churn for readability
df["churn_predicted"] = label_encoders["churned"].inverse_transform(df["churn_predicted"])

# Print a few prediction results
print("\n Sample Predictions:")
print(df[["username", "service_name", "churned", "churn_predicted"]].head(10))

# Accuracy check
accuracy = (original_churned == df["churn_predicted"]).mean()
print(f"\n Model Accuracy on MongoDB Data: {accuracy * 100:.2f}%")

# Create plots directory if it doesn't exist
os.makedirs("plots", exist_ok=True)

# Optional: Save or visualize
sns.set(style="whitegrid")
plt.figure(figsize=(6, 4))
sns.countplot(data=df, x="churn_predicted", hue="churn_predicted", palette="Set2", legend=False)
plt.title("Predicted Churn Distribution")
plt.xlabel("Predicted Churned?")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("plots/predicted_churn_distribution.png")
print("\n Saved predicted_churn_distribution.png")

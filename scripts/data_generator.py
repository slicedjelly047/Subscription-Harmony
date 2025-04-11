import random
import numpy as np
from pymongo import MongoClient
from faker import Faker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

# Connect to MongoDB Atlas
client = MongoClient(MONGODB_URI)
db = client["subscriptionApp"]
collection = db["subscription_data"]

# Clear old data (optional)
collection.delete_many({})
print("Cleared old data from subscription_data collection.")

# Faker setup
fake = Faker()

subscriptions = [
    {"service_name": "Netflix", "category": "Streaming", "monthly_cost": 499},
    {"service_name": "Spotify", "category": "Music", "monthly_cost": 199},
    {"service_name": "Amazon Prime", "category": "Streaming", "monthly_cost": 299},
    {"service_name": "YouTube Premium", "category": "Streaming", "monthly_cost": 129},
    {"service_name": "Apple Music", "category": "Music", "monthly_cost": 179},
    {"service_name": "Google One", "category": "Storage", "monthly_cost": 130},
    {"service_name": "Dropbox", "category": "Storage", "monthly_cost": 150},
    {"service_name": "Hotstar", "category": "Streaming", "monthly_cost": 299},
    {"service_name": "Canva Pro", "category": "Productivity", "monthly_cost": 399},
    {"service_name": "Notion Pro", "category": "Productivity", "monthly_cost": 300},
]

# Generate data
num_users = 200
documents = []

for user_id in range(1, num_users + 1):
    username = fake.user_name()
    user_subs = random.sample(subscriptions, k=random.randint(2, 5))

    for sub in user_subs:
        login_frequency = np.random.randint(1, 25)
        time_spent = round(np.random.uniform(0.5, 15.0), 2)
        feature_usage = round(np.random.uniform(10, 100), 2)

        churn_prob = (
            0.8 if login_frequency < 5 and feature_usage < 30 else
            0.5 if login_frequency < 10 else
            0.2
        )
        churned = "Yes" if np.random.rand() < churn_prob else "No"

        doc = {
            "user_id": user_id,
            "username": username,
            "service_name": sub["service_name"],
            "category": sub["category"],
            "monthly_cost": sub["monthly_cost"],
            "login_frequency": login_frequency,
            "time_spent": time_spent,
            "feature_usage": feature_usage,
            "churned": churned
        }
        documents.append(doc)

collection.insert_many(documents)
print(f" Inserted {len(documents)} records into subscription_data collection in Atlas.")

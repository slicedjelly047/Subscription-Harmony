=======================================================
🔧 SETUP GUIDE: Subscription Harmony – ML + FastAPI
=======================================================


-----------------------------------------
📁 Step 1: Clone the Repository
-----------------------------------------
git clone https://github.com/YOUR_USERNAME/Subscription-Harmony.git
cd Subscription-Harmony

-----------------------------------------
🐍 Step 2: Create and Activate a Virtual Environment
-----------------------------------------
# On Linux/Mac
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate


-----------------------------------------
📦 Step 3: Install Dependencies
-----------------------------------------
pip install -r requirements.txt



-----------------------------------------
🧪 Step 4: Create `.env` File
-----------------------------------------
In the project root folder, create a file called `.env` and add:

MONGODB_URI=mongodb+srv://appuser:vBMTfdXTjIGixEyL@subscription-app-db.tuy8pft.mongodb.net/subscriptionApp?retryWrites=true&w=majority&appName=subscription-app-db&ssl=true

(Note: Do NOT share this URI publicly)



-----------------------------------------
🧠 Step 5: Run ML Analysis 
-----------------------------------------
python ml/churn_analysis.py

This will:
- Connect to MongoDB
- Load model and encoders
- Predict churn on existing data
- Show accuracy and save a plot



-----------------------------------------
🚀 Step 6: Start the Prediction API
-----------------------------------------
cd api
uvicorn predict_api:app --reload

Then open this in your browser:
👉 http://localhost:8000/docs

To test if it's working, you can:

Click on the POST /predict endpoint

Click "Try it out"

Use this sample input:

{
  "service_name": "Netflix",
  "category": "Streaming",
  "monthly_cost": 499,
  "login_frequency": 15,
  "time_spent": 10.5,
  "feature_usage": 75.0
}

Click "Execute"
The API should return a prediction indicating whether this customer is likely to churn or not, along with the probability

You will get:
- Prediction: Churned or Retained
- Probability (0.00–1.00)

To stop the server, press Ctrl+C in the terminal.

-----------------------------------------
✅ Done! You're Ready to Explore 🎉
-----------------------------------------

📌 Next Tasks:
- Soumyadeep: Build subscription/user APIs
- Soumojit: Build React dashboard + prediction UI



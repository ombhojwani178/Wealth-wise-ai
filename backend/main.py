# 1. Standard library imports
import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor
import json

# 2. Third-party imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# 3. Load environment variables from your .env file
load_dotenv()

# --- Database Setup ---
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Create table if it doesn't exist
def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            id SERIAL PRIMARY KEY,
            age INTEGER,
            income INTEGER,
            goals TEXT,
            current_investments TEXT,
            ai_summary TEXT,
            ai_opportunity TEXT,
            ai_risk_assessment TEXT,
            ai_suggested_action TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

create_table()

# 4. Create the FastAPI app instance
app = FastAPI()

# 5. Configure CORS Middleware
origins = [
    "http://localhost:3000",
    "https://your-vercel-frontend-url.vercel.app" # Add your Vercel URL here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 6. Pydantic Model for incoming data validation
class UserProfile(BaseModel):
    age: int
    income: int
    goals: str
    current_investments: str

# 7. API Endpoints (Routes)
@app.get("/")
def read_root():
    """ A simple 'health check' endpoint to confirm the server is running. """
    return {"status": "ok", "message": "AI Financial Advisor backend is running."}


@app.post("/api/analyze")
def analyze_profile(profile: UserProfile):
    """
    Receives user profile, gets a mock insight, and saves it to the database.
    """
    print(f"Received profile for analysis: {profile.dict()}")

    time.sleep(2) # Simulate AI processing time

    mock_insight = {
        "summary": f"Based on your profile as a {profile.age}-year-old with a goal of '{profile.goals}', we've identified several opportunities.",
        "opportunity": "The renewable energy sector is showing strong growth potential. An ETF focused on this sector could be a good addition to your portfolio.",
        "risk_assessment": "Your current investments are heavily weighted in the tech sector. To mitigate risk, we recommend diversifying into healthcare and consumer staples.",
        "suggested_action": "Consider allocating 10-15% of your monthly investment budget to a renewable energy ETF. Also, review your tech holdings."
    }

    # --- Save the profile and analysis to the database ---
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO user_profiles (age, income, goals, current_investments, ai_summary, ai_opportunity, ai_risk_assessment, ai_suggested_action)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (profile.age, profile.income, profile.goals, profile.current_investments, mock_insight['summary'], mock_insight['opportunity'], mock_insight['risk_assessment'], mock_insight['suggested_action'])
    )
    conn.commit()
    cur.close()
    conn.close()

    return {"status": "success", "insight": mock_insight}

@app.get("/api/profiles")
def get_profiles():
    """ An endpoint to retrieve all profiles from the database. """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM user_profiles ORDER BY created_at DESC")
    profiles = cur.fetchall()
    cur.close()
    conn.close()
    return profiles

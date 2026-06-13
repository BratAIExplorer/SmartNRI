from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import sqlite3
import os
from datetime import datetime

app = FastAPI(title="SmartNRI API")

DB_PATH = os.getenv("DB_PATH", "data/smartnri.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # Ensure directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            country TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            processed INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS bug_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            processed INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    country: str
    role: str

class BugReport(BaseModel):
    email: EmailStr
    description: str

@app.post("/api/register")
def register_user(user: UserRegister):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (name, email, country, role) VALUES (?, ?, ?, ?)",
            (user.name, user.email, user.country, user.role)
        )
        conn.commit()
        conn.close()
        return {"status": "success", "message": "User registered"}
    except sqlite3.IntegrityError:
        # Email already exists
        return {"status": "success", "message": "User already registered"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/report-bug")
def report_bug(report: BugReport):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute(
            "INSERT INTO bug_reports (email, description) VALUES (?, ?)",
            (report.email, report.description)
        )
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Bug report saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

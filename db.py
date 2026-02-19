# db.py
import sqlite3
from datetime import datetime

DB_NAME = "rewards.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            cibil INTEGER,
            streak INTEGER,
            fraud INTEGER,
            coins REAL,
            risk_score REAL,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()

def insert_simulation(amount, cibil, streak, fraud, coins, risk_score):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO simulations (amount, cibil, streak, fraud, coins, risk_score, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        amount,
        cibil,
        streak,
        int(fraud),
        coins,
        risk_score,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

def fetch_last_simulations(limit=10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT amount, cibil, streak, fraud, coins, risk_score, timestamp
        FROM simulations
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()
    return rows

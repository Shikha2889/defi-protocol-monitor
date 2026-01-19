from fastapi import FastAPI
from database import get_connection

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/protocols")
def protocols():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM protocol_metrics")
    data = cursor.fetchall()
    conn.close()
    return data

@app.get("/alerts")
def alerts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM protocol_alerts")
    data = cursor.fetchall()
    conn.close()
    return data


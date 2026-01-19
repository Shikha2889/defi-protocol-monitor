import sqlite3

DB_NAME = "defi.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Stores protocol metrics over time
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS protocol_metrics (
        protocol_name TEXT,
        timestamp TEXT,
        tvl_usd REAL,
        apy REAL,
        utilization REAL,
        PRIMARY KEY (protocol_name, timestamp)
    )
    """)

    # Stores anomaly alerts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS protocol_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        protocol_name TEXT,
        alert_type TEXT,
        severity TEXT,
        metric TEXT,
        value REAL,
        threshold REAL,
        timestamp TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()

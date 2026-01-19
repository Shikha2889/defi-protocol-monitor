from fastapi import FastAPI, Query
from database import get_connection

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

#  Protocol summary with health status
@app.get("/protocols")
def get_protocols():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT protocol_name, tvl_usd, apy
    FROM protocol_metrics
    WHERE (protocol_name, timestamp) IN (
        SELECT protocol_name, MAX(timestamp)
        FROM protocol_metrics
        GROUP BY protocol_name
    )
    """)

    protocols = []
    for name, tvl, apy in cursor.fetchall():
        status = "healthy"
        if apy is not None and apy < 0.02:
            status = "warning"

        protocols.append({
            "name": name,
            "tvl": tvl,
            "apy": apy,
            "status": status
        })

    conn.close()
    return protocols

# 2️ Protocol history
@app.get("/protocols/{name}/history")
def protocol_history(name: str, days: int = Query(30)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT timestamp, tvl_usd, apy
    FROM protocol_metrics
    WHERE protocol_name = ?
    ORDER BY timestamp DESC
    LIMIT ?
    """, (name, days))

    history = [
        {"timestamp": ts, "tvl": tvl, "apy": apy}
        for ts, tvl, apy in cursor.fetchall()
    ]

    conn.close()
    return history

#
#  Filtered alerts
@app.get("/alerts")
def get_alerts(status: str = Query("open")):
    conn = get_connection()
    cursor = conn.cursor()

    # For this assignment, all alerts are treated as open
    cursor.execute("""
    SELECT protocol_name, alert_type, severity, message, timestamp
    FROM protocol_alerts
    ORDER BY timestamp DESC
    """)

    alerts = [
        {
            "protocol": p,
            "type": t,
            "severity": s,
            "message": m,
            "timestamp": ts
        }
        for p, t, s, m, ts in cursor.fetchall()
    ]

    conn.close()
    return alerts

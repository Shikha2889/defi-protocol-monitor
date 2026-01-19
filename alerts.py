from database import get_connection
from datetime import datetime, timedelta

def check_alerts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT protocol_name, timestamp, tvl_usd, apy, utilization
    FROM protocol_metrics
    ORDER BY timestamp DESC
    """)

    rows = cursor.fetchall()

    for protocol, ts, tvl, apy, util in rows:
        # APY alert
        if apy is not None and apy < 0.02:
            cursor.execute("""
            INSERT INTO protocol_alerts
            (protocol_name, alert_type, severity, metric, value, threshold, timestamp, message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                protocol,
                "LOW_APY",
                "WARNING",
                "APY",
                apy,
                0.02,
                datetime.utcnow().isoformat(),
                "APY below 2%"
            ))

        # Utilization alert
        if util is not None and util > 0.95:
            cursor.execute("""
            INSERT INTO protocol_alerts
            (protocol_name, alert_type, severity, metric, value, threshold, timestamp, message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                protocol,
                "HIGH_UTILIZATION",
                "WARNING",
                "UTILIZATION",
                util,
                0.95,
                datetime.utcnow().isoformat(),
                "Utilization above 95%"
            ))

    conn.commit()
    conn.close()

def check_tvl_drop():
    conn = get_connection()
    cursor = conn.cursor()

    # Get latest timestamp per protocol
    cursor.execute("""
    SELECT protocol_name, MAX(timestamp)
    FROM protocol_metrics
    GROUP BY protocol_name
    """)

    latest_rows = cursor.fetchall()

    for protocol, latest_ts in latest_rows:
        # Latest TVL
        cursor.execute("""
        SELECT tvl_usd FROM protocol_metrics
        WHERE protocol_name = ? AND timestamp = ?
        """, (protocol, latest_ts))

        latest_tvl = cursor.fetchone()
        if not latest_tvl:
            continue

        latest_tvl = latest_tvl[0]

        # TVL ~24 hours ago
        target_time = datetime.fromisoformat(latest_ts) - timedelta(hours=24)

        cursor.execute("""
        SELECT tvl_usd FROM protocol_metrics
        WHERE protocol_name = ?
        AND timestamp <= ?
        ORDER BY timestamp DESC
        LIMIT 1
        """, (protocol, target_time.isoformat()))

        old_tvl = cursor.fetchone()
        if not old_tvl:
            continue

        old_tvl = old_tvl[0]

        # Compare drop
        drop_pct = (old_tvl - latest_tvl) / old_tvl

        if drop_pct > 0.20:
            cursor.execute("""
            INSERT INTO protocol_alerts
            (protocol_name, alert_type, severity, metric, value, threshold, timestamp, message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                protocol,
                "TVL_DROP",
                "CRITICAL",
                "TVL",
                latest_tvl,
                0.20,
                datetime.utcnow().isoformat(),
                f"TVL dropped {round(drop_pct*100,2)}% in last 24h"
            ))

    conn.commit()
    conn.close()
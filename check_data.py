import sqlite3

conn = sqlite3.connect("defi.db")
cursor = conn.cursor()

print("---- PROTOCOL METRICS ----")
for row in cursor.execute("SELECT * FROM protocol_metrics"):
    print(row)

print("\n---- PROTOCOL ALERTS ----")
for row in cursor.execute("SELECT * FROM protocol_alerts"):
    print(row)

conn.close()

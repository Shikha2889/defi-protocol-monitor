# DeFi Protocol Monitoring Pipeline

This project implements a monitoring pipeline for DeFi protocols, designed to track protocol health metrics and detect risk signals.  
It mirrors how Token Metrics monitors protocols that vault strategies deposit into.

---

## Features

- Fetches protocol metrics (TVL, APY, utilization)
- Supports multiple protocols (Felix, HLP)
- Resilient ingestion with timeout and error handling
- Detects anomalies and inserts alerts
- Exposes data via a FastAPI service
- Idempotent writes to prevent duplicate data

##  Tracked Metrics

| Metric | Description |
|------|------------|
| TVL | Total Value Locked (USD) |
| APY | Lending yield |
| Utilization | Borrow utilization ratio |

---

##  Alert Rules

| Condition | Severity |
|---------|----------|
| TVL drop > 20% in 24h | CRITICAL |
| APY < 2% | WARNING |
| Utilization > 95% | WARNING |

Alerts are written to the `protocol_alerts` table.

---

##  Architecture
Ingest Script
    ↓
Protocol Metrics (SQLite)
    ↓
Anomaly Detection
    ↓
Alerts Table
    ↓
FastAPI Endpoints
---

## Database Schema

### protocol_metrics

- protocol_name (TEXT)
- timestamp (TEXT)
- tvl_usd (REAL)
- apy (REAL)
- utilization (REAL)

Primary Key: `(protocol_name, timestamp)`

---

### protocol_alerts

- id (INTEGER)
- protocol_name (TEXT)
- alert_type (TEXT)
- severity (TEXT)
- metric (TEXT)
- value (REAL)
- threshold (REAL)
- timestamp (TEXT)
- message (TEXT)

---

##  Setup Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the monitoring pipeline

This will:

- Create database tables

- Fetch protocol metrics

- Run anomaly detection

- Log errors without crashing the pipeline

Run the pipeline using:

```bash
python main.py
```
## API Usage

Start the API server:

```bash
uvicorn api:app --reload
```
### Available Endpoints

- `GET /health` → Service health check
- `GET /protocols` → Latest protocol metrics
- `GET /alerts` → Triggered alerts

---

## Idempotency & Resilience

- Duplicate writes are prevented using a composite primary key (`protocol_name`, `timestamp`)
- Partial failures (e.g., one protocol down) do not stop the pipeline
- Errors are logged with protocol context

---

## Notes

- TVL is fetched from the DeFiLlama API where available
- Some protocols (e.g., HLP) do not expose public endpoints; mock data is used as a fallback
- TVL drop detection activates once sufficient historical data exists

---

## Future Improvements

- On-chain reads via smart contract calls
- Slack alert integration
- Grafana dashboards
- Containerization via Docker

---

## Author

**Gowri**

Take-home assignment submission for Token Metrics.

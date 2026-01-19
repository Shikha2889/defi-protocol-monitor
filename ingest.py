import requests
from datetime import datetime
from database import get_connection
from logger import logger


def fetch_defillama_tvl(protocol):
    url = f"https://api.llama.fi/tvl/{protocol}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print(f"Timeout fetching TVL for {protocol}")
    except requests.exceptions.HTTPError:
        logger.error(
            "HTTP error fetching TVL",
            extra={"protocol": protocol}
        )

    except Exception as e:
        print(f"Malformed response for {protocol}: {e}")
    return None

def fetch_felix_data():
    # Mock APY & utilization (on-chain read simulated)
    tvl = fetch_defillama_tvl("felix") or 120_000_000

    return {
        "protocol": "Felix",
        "tvl": tvl if isinstance(tvl, (int, float)) else 120_000_000,
        "apy": 0.035,
        "utilization": 0.82
    }

def fetch_hlp_data():
    tvl = fetch_defillama_tvl("hlp") or 75_000_000

    return {
        "protocol": "HLP",
        "tvl": tvl if isinstance(tvl, (int, float)) else 75_000_000,
        "apy": None,
        "utilization": None
    }

def store_metrics(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO protocol_metrics
    VALUES (?, ?, ?, ?, ?)
    """, (
        data["protocol"],
        datetime.utcnow().isoformat(),
        data["tvl"],
        data["apy"],
        data["utilization"]
    ))

    conn.commit()
    conn.close()

def run_ingestion():
    for fetcher in [fetch_felix_data, fetch_hlp_data]:
        try:
            data = fetcher()
            store_metrics(data)
        except Exception as e:
            print("Pipeline error:", e)

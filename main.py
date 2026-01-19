from database import create_tables
from ingest import run_ingestion
from alerts import check_alerts, check_tvl_drop
from logger import logger

if __name__ == "__main__":
    logger.info("Starting DeFi monitoring pipeline")
    create_tables()
    run_ingestion()
    check_alerts()
    check_tvl_drop()
    logger.info("Monitoring pipeline completed")



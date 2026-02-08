"""
Scheduler for automatic SEC tickers update
"""

import schedule
import time
import logging
from update_tickers import update_tickers

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def job():
    """Job to run for scheduled updates"""
    logger.info("Running scheduled update...")
    success = update_tickers()
    if success:
        logger.info("✓ Scheduled update completed")
    else:
        logger.error("✗ Scheduled update failed")

def start_scheduler(hour: int = 9, minute: int = 0):
    """
    Start the scheduler
    
    Args:
        hour: Hour to run update (24-hour format)
        minute: Minute to run update
    """
    schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(job)
    logger.info(f"Scheduler started. Update scheduled for {hour:02d}:{minute:02d} daily")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # Run daily at 9:00 AM
    # start_scheduler(hour=9, minute=0)
    job()
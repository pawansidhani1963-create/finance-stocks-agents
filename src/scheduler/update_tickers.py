"""
SEC Company Tickers Update Script
Downloads and updates company_tickers.json from SEC
"""

import json
import requests
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
SEC_URL = "https://www.sec.gov/files/company_tickers.json"
SEC_HEADER = {
    "User-Agent": "Pawan Sidhani (pawan.sidhani1963@gmail.com)"
}
DATA_DIR = Path(__file__).parent.parent
OUTPUT_FILE = DATA_DIR / "company_tickers.json"
BACKUP_DIR = DATA_DIR / "backups"

def ensure_backup_dir():
    """Create backup directory if it doesn't exist"""
    BACKUP_DIR.mkdir(exist_ok=True)

def create_backup(file_path: Path):
    """Create a timestamped backup of existing file"""
    if file_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = BACKUP_DIR / f"company_tickers_{timestamp}.json"
        try:
            with open(file_path, 'r') as src:
                backup_content = src.read()
            with open(backup_file, 'w') as dst:
                dst.write(backup_content)
            logger.info(f"Backup created: {backup_file}")
            return backup_file
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return None
    return None

def download_tickers(url: str, header) -> dict | None:
    """
    Download company tickers from SEC
    
    Args:
        url: SEC endpoint URL
        
    Returns:
        Dictionary of tickers or None if failed
    """
    try:
        logger.info(f"Downloading from {url}...")
        response = requests.get(url, header, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        logger.info(f"Successfully downloaded {len(data)} records")
        return data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON response: {e}")
        return None

def validate_data(data: dict) -> bool:
    """
    Validate downloaded data structure
    
    Args:
        data: Dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(data, dict):
        logger.error("Data is not a dictionary")
        return False
    
    if not data:
        logger.error("Data is empty")
        return False
    
    # Check sample record structure
    first_key = next(iter(data.keys()))
    sample_record = data[first_key]
    
    required_fields = ['cik_str', 'ticker', 'title']
    if not all(field in sample_record for field in required_fields):
        logger.error(f"Missing required fields. Found: {sample_record.keys()}")
        return False
    
    logger.info("Data validation passed")
    return True

def save_data(data: dict, file_path: Path) -> bool:
    """
    Save data to JSON file
    
    Args:
        data: Dictionary to save
        file_path: Path to save file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Data saved to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save data: {e}")
        return False

def update_tickers(url: str = SEC_URL,
                   header = SEC_HEADER, 
                   output_file: Path = OUTPUT_FILE,
                   create_backup_flag: bool = True) -> bool:
    """
    Main update function
    
    Args:
        url: SEC endpoint URL
        output_file: Path to output file
        create_backup_flag: Whether to create backup
        
    Returns:
        True if successful, False otherwise
    """
    logger.info("=" * 60)
    logger.info("Starting SEC Company Tickers Update")
    logger.info("=" * 60)
    
    # Create backup
    if create_backup_flag:
        ensure_backup_dir()
        create_backup(output_file)
    
    # Download data
    data = download_tickers(url, header)
    if data is None:
        logger.error("Update failed: Unable to download data")
        return False
    
    # Validate data
    if not validate_data(data):
        logger.error("Update failed: Data validation failed")
        return False
    
    # Save data
    if not save_data(data, output_file):
        logger.error("Update failed: Unable to save data")
        return False
    
    logger.info("=" * 60)
    logger.info("Update completed successfully!")
    logger.info("=" * 60)
    return True

if __name__ == "__main__":
    update_tickers()
"""
Balance Sheet Retriever
--------------------------
Specialized retriever for balance sheet facts using GenericRetriever
"""
# import sys
# print(sys.path)

import json
from datetime import date
import logging
from pathlib import Path
from retrievers.generic_direct_fact_retriever import GenericDirectFactRetriever, FactType, load_registry


# =========================
# LOGGING
# =========================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =========================
# BALANCE SHEET RETRIEVER
# =========================

class BalanceSheetRetriever:
    """
    Specialized retriever for extracting normalized balance sheet facts
    from SEC companyfacts JSON
    """
    
    def __init__(self, company_ticker: str, registry: dict = None):
        """
        Initialize balance sheet retriever with FactType.BALANCE_SHEET
        
        Args:
            company_ticker: Company ticker symbol
        """
        self.company_ticker = company_ticker
        self.direct_fact_registry = {}
        self.derived_fact_registry = {}
        self.current_date = date.today().isoformat()
        for section, facts in registry.items():
            if facts:
                if facts.get("retrieval") == "direct":
                    self.direct_fact_registry[section] = facts
                elif facts.get("retrieval") == "derived":
                    self.derived_fact_registry[section] = facts
        self.retriever = GenericDirectFactRetriever(company_ticker, FactType.BALANCE_SHEET, self.direct_fact_registry)

    def extract(self, companyfacts):
        """
        Extract normalized balance sheet facts
        
        Args:
            companyfacts: SEC companyfacts dictionary
            
        Returns:
            List of normalized balance sheet facts
        """
        return self.retriever.extract(companyfacts)
    
    def write(self, facts, project_root):
        """
        Write balance sheet facts to storage
        
        Args:
            facts: List of normalized facts
            project_root: Path to project root directory
        """
        self.retriever.write(facts, project_root, self.current_date)


# =========================
# ENTRY POINT
# =========================

def run(company_ticker, companyfacts_path, registry_path, write_dir):
    """
    Run balance sheet retrieval process
    
    Args:
        companyfacts_path: Path to companyfacts JSON file
        company_ticker: Company ticker symbol
    """
    project_root = Path(__file__).parent.parent.parent.parent
    registry_final_path = project_root / registry_path
    registry = load_registry(FactType.BALANCE_SHEET, registry_final_path)
    companyfacts_file_path = project_root / companyfacts_path
    write_dir = project_root / write_dir
    write_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Loading companyfacts from {companyfacts_file_path}")
    
    try:
        with open(companyfacts_file_path, "r") as f:
            companyfacts = json.load(f)
    except FileNotFoundError:
        logger.error(f"Company facts file not found: {companyfacts_file_path}")
        return
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing company facts JSON: {e}")
        return

    # Initialize balance sheet retriever
    retriever = BalanceSheetRetriever(company_ticker, registry)
    
    # Extract facts
    facts = retriever.extract(companyfacts)
    
    if not facts:
        logger.warning(f"No balance sheet facts extracted for {company_ticker}")
        return
    
    # Write to storage
    retriever.write(facts, write_dir)

    print(f"✓ Extracted {len(facts)} balance sheet facts for {company_ticker}")


# =========================
# USAGE
# =========================

if __name__ == "__main__":
    run("RDDT", 
        "data/RDDT/raw/company_facts.json",
        "src/retrievers/registry/sec_facts_canonical_mappings_v1.json",
        "data/RDDT/normalized")

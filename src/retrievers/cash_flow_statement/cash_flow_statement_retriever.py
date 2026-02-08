"""
Cash Flow Statement Retriever
--------------------------
Specialized retriever for cash flow statement facts using GenericRetriever
"""

import json
import logging
from pathlib import Path
from retrievers.generic_derived_fact_retriever import GenericDerivedFactRetriever
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
# CASH FLOW STATEMENT RETRIEVER
# =========================

class CashflowStatementRetriever:
    """
    Specialized retriever for extracting normalized cash flow statement facts
    from SEC companyfacts JSON
    """
    
    def __init__(self, company_ticker: str, registry: dict = None):
        """
        Initialize cash flow statement retriever with FactType.CASH_FLOW_STATEMENT
        
        Args:
            company_ticker: Company ticker symbol
        """
        
        self.company_ticker = company_ticker
        self.direct_fact_registry = {}
        self.derived_fact_registry = {}
        for section, facts in registry.items():
            if facts:
                if facts.get("retrieval") == "direct":
                    self.direct_fact_registry[section] = facts
                elif facts.get("retrieval") == "derived":
                    self.derived_fact_registry[section] = facts

        if self.direct_fact_registry:
            self.direct_fact_retriever = GenericDirectFactRetriever(company_ticker, FactType.CASH_FLOW_STATEMENT, self.direct_fact_registry)
        
        if self.derived_fact_registry:
            self.derived_fact_retriever = GenericDerivedFactRetriever(company_ticker, FactType.CASH_FLOW_STATEMENT, self.derived_fact_registry)

    def extract(self, companyfacts):
        """
        Extract normalized cash flow statement facts
        
        Args:
            companyfacts: SEC companyfacts dictionary
            
        Returns:
            List of normalized cash flow statement facts
        """
        if self.direct_fact_registry:
            return self.direct_fact_retriever.extract(companyfacts)
        
        return None
    
    def write(self, facts, write_dir):
        """
        Write cash flow statement facts to storage
        
        Args:
            facts: List of normalized facts
            project_root: Path to project root directory
        """
        if self.direct_fact_registry:
            self.direct_fact_retriever.write(facts, write_dir)

        return None
    
    def extract_derived_facts(self, normalized_facts):
        """
        Extract derived cash flow statement facts
        
        Returns:
            List of derived normalized cash flow statement facts
        """
        if self.derived_fact_registry:
            return self.derived_fact_retriever.extract_derived_facts(normalized_facts)

        return None
    
    def write_derived_facts(self, facts, write_dir):
        """
        Write derived cash flow statement facts to storage
        
        Args:
            facts: List of derived normalized facts
            project_root: Path to project root directory
        """
        if self.derived_fact_registry:
            self.derived_fact_retriever.write(facts, write_dir)

        return None


# =========================
# ENTRY POINT
# =========================

def run(company_ticker, companyfacts_path, registry_path, write_dir_normalized, write_dir_derived):
    """
    Run cash flow statement retrieval process
    
    Args:
        companyfacts_path: Path to companyfacts JSON file
        company_ticker: Company ticker symbol
    """
    project_root = Path(__file__).parent.parent.parent.parent
    registry_final_path = project_root / registry_path
    registry = load_registry(FactType.CASH_FLOW_STATEMENT, registry_final_path)
    companyfacts_file_path = project_root / companyfacts_path
    write_dir_normalized = project_root / write_dir_normalized
    write_dir_normalized.mkdir(parents=True, exist_ok=True)

    write_dir_derived = project_root / write_dir_derived
    write_dir_derived.mkdir(parents=True, exist_ok=True)
    
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

    # Initialize cash flow statement retriever
    retriever = CashflowStatementRetriever(company_ticker, registry)

    
    # Extract facts
    normalized_facts = retriever.extract(companyfacts)
    
    if not normalized_facts:
        logger.warning(f"No cash flow statement facts extracted for {company_ticker}")
        return
    
    # Write to storage
    retriever.write(normalized_facts, write_dir_normalized)

    print(f"✓ Extracted {len(normalized_facts)} cash flow statement facts for {company_ticker}")

    # Extract facts
    derived_facts = retriever.extract_derived_facts(normalized_facts)
    
    if not derived_facts:
        logger.warning(f"No cash flow statement derived facts extracted for {company_ticker}")
        return
    
    # Write to storage
    retriever.write_derived_facts(derived_facts, write_dir_derived)
    print(f"✓ Extracted {len(derived_facts)} cash flow statement derived facts for {company_ticker}")


# =========================
# USAGE
# =========================

if __name__ == "__main__":
    run("RDDT", 
        "data/RDDT/raw/company_facts.json",
        "src/retrievers/registry/sec_facts_canonical_mappings_v1.json",
        "data/RDDT/normalized",
        "data/RDDT/derived")
"""
Generic Direct Fact Retriever
--------------------------
Inputs:
- SEC companyfacts JSON (already downloaded)
- fact registry

Outputs:
- Normalized fact entries
- Written to file-based JSON storage
"""

import json
import sys
import logging
from enum import Enum
from datetime import datetime
from pathlib import Path


# =========================
# LOGGING
# =========================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =========================
# ENUMS
# =========================

class FactType(Enum):
    """Enum for financial statement types"""
    INCOME_STATEMENT = "income_statement"
    BALANCE_SHEET = "balance_sheet"
    CASH_FLOW_STATEMENT = "cash_flow_statement"


# =========================
# CONFIG
# =========================

FORM_PRIORITY = {
    "10-K/A": 4,
    "10-Q/A": 3,
    "10-K": 2,
    "10-Q": 1
}


# =========================
# REGISTRY LOADER
# =========================

def load_registry(statement_type: FactType, registry_path: str):
    """
    Load registry for a specific statement type from canonical mappings file
    
    Args:
        statement_type: StatementType enum value
        
    Returns:
        Dictionary mapping canonical fields to XBRL metadata
    """
    
    try:
        with open(registry_path, "r") as f:
            mappings = json.load(f)
        logger.info(f"Loaded registry from {registry_path}")
        return mappings.get(statement_type.value, {})
    except FileNotFoundError:
        logger.error(f"Registry file not found at {registry_path}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing registry file: {e}")
        return {}


# =========================
# GENERIC RETRIEVER CLASS
# =========================

class GenericDirectFactRetriever:
    """
    Generic retriever for extracting and normalizing facts
    from SEC companyfacts JSON
    """

    def __init__(self, company_ticker: str, statement_type: FactType, registry: dict):
        """
        Initialize retriever
        
        Args:
            company_ticker: Company ticker symbol
            statement_type: Type of financial statement to retrieve
        """
        self.company_ticker = company_ticker
        self.statement_type = statement_type
        self.registry = registry
        
    
    # =========================
    # DATE HELPERS
    # =========================
    
    @staticmethod
    def parse_date(date_str):
        """Parse date string to datetime object"""
        return datetime.strptime(date_str, "%Y-%m-%d")

    def duration_days(self, fact):
        """Calculate duration in days for a fact"""
        if "start" not in fact or fact["start"] is None:
            return None
        return (self.parse_date(fact["end"]) - self.parse_date(fact["start"])).days

    def is_discrete_quarter(self, fact):
        """Check if fact represents a discrete quarter (80-100 days)"""
        days = self.duration_days(fact)
        return days is not None and 80 <= days <= 100

    # =========================
    # RAW FACT EXTRACTION
    # =========================

    def extract_raw_facts(self, companyfacts, tag):
        """
        Returns list of raw SEC facts for a given us-gaap tag
        
        Args:
            companyfacts: SEC companyfacts dictionary
            tag: XBRL tag name
            
        Returns:
            List of facts in USD
        """
        try:
            return companyfacts["facts"]["us-gaap"][tag]["units"]["USD"]
        except KeyError:
            logger.debug(f"Tag {tag} not found in companyfacts")
            return []

    # =========================
    # AUTHORITATIVE SELECTION
    # =========================

    def pick_authoritative(self, facts):
        """
        Picks the most recent filing for the same period
        
        Args:
            facts: List of facts for same period
            
        Returns:
            Single best fact (prioritizes amended filings)
        """
        facts.sort(
            key=lambda f: (
                f["filed"],
                FORM_PRIORITY.get(f["form"], 0)
            ),
            reverse=True
        )
        return facts[0]

    def group_by_period(self, facts):
        """
        Groups facts by (start, end) period
        
        Args:
            facts: List of facts
            
        Returns:
            Dictionary grouped by period key
        """
        groups = {}
        for f in facts:
            key = (f.get("start"), f.get("end"))
            groups.setdefault(key, []).append(f)
        return groups

    # =========================
    # PERIOD CLASSIFICATION
    # =========================

    def classify_period(self, fact):
        """
        Returns normalized period label or None
        
        Args:
            fact: Individual fact
            
        Returns:
            Period label (e.g., "FY-2024", "Q1-2024") or None
        """
        if fact["fp"] == "FY":
            return f"FY-{fact['fy']}"

        if self.is_discrete_quarter(fact):
            return f"{fact['fp']}-{fact['fy']}"

        # YTD or unsupported period → ignore for now
        return None

    # =========================
    # MAIN EXTRACTION LOGIC
    # =========================

    def extract(self, companyfacts):
        """
        Extract and normalize financial statement facts
        
        Args:
            companyfacts: SEC companyfacts dictionary
            
        Returns:
            List of normalized facts
        """
        logger.info(f"Extracting {self.statement_type.value} for {self.company_ticker}")
        normalized = []
        logger.info(f"Using registry with {len(self.registry)} concepts")
        for concept, meta in self.registry.items():
            tag = meta["tag"]
            raw_facts = self.extract_raw_facts(companyfacts, tag)

            if not raw_facts:
                logger.debug(f"No facts found for {concept} (tag: {tag})")
                continue

            grouped = self.group_by_period(raw_facts)

            for _, facts in grouped.items():
                fact = self.pick_authoritative(facts)
                period = self.classify_period(fact)

                if not period:
                    continue

                normalized.append({
                    "company": self.company_ticker,
                    "statement": self.statement_type.value,
                    "concept": concept,
                    "value": fact["val"],
                    "currency": "USD",
                    "period": period,
                    "reported": True,
                    "source_form": fact["form"],
                    "filed_date": fact["filed"]
                })

        logger.info(f"Extracted {len(normalized)} facts")
        return normalized

    # =========================
    # FILE-BASED STORAGE
    # =========================

    def write(self, facts, output_dir):
        """
        Write normalized facts to storage
        
        Args:
            facts: List of normalized facts
            output_dir: Path to output directory
        """

        output_file = output_dir / f"{self.statement_type.value}.json"

        payload = {
            "company": self.company_ticker,
            "statement": self.statement_type.value,
            "facts": facts
        }

        with open(output_file, "w") as f:
            json.dump(payload, f, indent=2)
        
        logger.info(f"Written {len(facts)} facts to {output_file}")


# =========================
# ENTRY POINT
# =========================

def run(companyfacts_path, company_ticker, statement_type=FactType.INCOME_STATEMENT):
    """
    Run retrieval process
    
    Args:
        companyfacts_path: Path to companyfacts JSON file
        company_ticker: Company ticker symbol
        statement_type: Type of statement to retrieve (default: INCOME_STATEMENT)
    """
    project_root = Path(__file__).parent.parent.parent
    companyfacts_file_path = project_root / companyfacts_path
    
    logger.info(f"Loading companyfacts from {companyfacts_file_path}")
    
    with open(companyfacts_file_path, "r") as f:
        companyfacts = json.load(f)

    # Initialize retriever
    retriever = GenericDirectFactRetriever(company_ticker, statement_type)
    
    # Extract facts
    facts = retriever.extract(companyfacts)
    
    # Write to storage
    retriever.write(facts, project_root)

    print(f"✓ Extracted {len(facts)} {statement_type.value} facts for {company_ticker}")


# =========================
# USAGE EXAMPLES
# =========================

if __name__ == "__main__":
    # Income Statement
    run("data/RDDT/raw/company_facts.json", "RDDT", FactType.INCOME_STATEMENT)
    
    # Balance Sheet (when ready)
    # run("data/RDDT/raw/company_facts.json", "RDDT", StatementType.BALANCE_SHEET)
    
    # Cash Flow Statement (when ready)
    # run("data/RDDT/raw/company_facts.json", "RDDT", StatementType.CASH_FLOW_STATEMENT)
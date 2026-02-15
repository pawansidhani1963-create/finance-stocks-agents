import json
import logging
from pathlib import Path

# =========================
# LOGGING
# =========================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def merge_cashflow_statements(normalized_facts, derived_facts):
        merged_data = normalized_facts.copy()
        merged_data["facts"].extend(derived_facts["facts"])
        return merged_data

class FetchAllFinancialStatements:
    def fetch_income_statement(company_ticker: str):
        company_ticker = company_ticker.upper()
        project_root = Path(__file__).parent.parent.parent.parent
        normalized_path = f"{project_root}/data/{company_ticker}/normalized/income_statement.json"
        try:
            with open(normalized_path, "r") as f:
                normalized_facts = json.load(f)
        except FileNotFoundError:
            logger.error(f"Income statement not found at: {normalized_path}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing company facts JSON: {e}")
            return None
        
        return normalized_facts
    
    def fetch_balance_sheet(company_ticker: str):
        company_ticker = company_ticker.upper()
        project_root = Path(__file__).parent.parent.parent.parent
        normalized_path = f"{project_root}/data/{company_ticker}/normalized/balance_sheet.json"
        try:
            with open(normalized_path, "r") as f:
                normalized_facts = json.load(f)
        except FileNotFoundError:
            logger.error(f"Balance sheet not found at: {normalized_path}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing company facts JSON: {e}")
            return None
        
        return normalized_facts
    
    def fetch_cash_flow_statement(company_ticker: str):
        company_ticker = company_ticker.upper()
        project_root = Path(__file__).parent.parent.parent.parent
        normalized_path = f"{project_root}/data/{company_ticker}/normalized/cash_flow_statement.json"
        derived_path = f"{project_root}/data/{company_ticker}/normalized/cash_flow_statement.json"
        try:
            with open(normalized_path, "r") as n, open(derived_path, "r") as d:
                normalized_facts = json.load(n)
                derived_facts = json.load(d)
                merged_facts = merge_cashflow_statements(normalized_facts, derived_facts)
        except FileNotFoundError:
            logger.error(f"Cashflow not found at: {normalized_path} or {derived_path}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing company facts JSON: {e}")
            return None
        
        return normalized_facts
    


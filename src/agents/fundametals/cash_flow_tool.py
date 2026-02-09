import json
from pathlib import Path

from agents.fundametals.utils import download_companyfacts, get_latest_filed_date

def get_cash_flow_statement_facts(company_ticker: str):
    ticker = company_ticker.upper()
    project_root = Path(__file__).parent.parent.parent.parent
    current_company_facts_path = project_root / "data" / ticker / "raw" / "companyfacts.json"
    if current_company_facts_path.exists():
        with open(current_company_facts_path, "r") as f:
            current_company_facts = json.load(f)
        current_processed_date = current_company_facts.get("processed_date")
        latest_filed_date = get_latest_filed_date(company_facts = download_companyfacts(ticker))
        if current_processed_date > latest_filed_date:
             # No new filings, can use existing companyfacts
        else:
            # New filings detected, need to redownload companyfacts and recompute latest filed date
            
    else:
        # Download companyfacts from SEC API
        # compute metrics and write to disk
        company_facts = download_companyfacts(ticker)
    
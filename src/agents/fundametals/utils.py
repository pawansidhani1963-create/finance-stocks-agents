import json
from pathlib import Path
import requests

SEC_HEADERS = {
    "User-Agent": "FundamentalsAgent/1.0 (your_email@example.com)"
}


def get_latest_filed_date(companyfacts: dict) -> str | None:
    """
    Traverse SEC companyfacts JSON and return the most recent `filed` date.

    Returns:
        ISO date string (YYYY-MM-DD) or None if no dates found.
    """

    latest_filed = None

    facts = companyfacts.get("facts", {})

    for taxonomy in facts.values():
        for tag_data in taxonomy.values():
            units = tag_data.get("units", {})
            for unit_facts in units.values():
                for fact in unit_facts:
                    filed = fact.get("filed")
                    if not filed:
                        continue

                    # ISO date strings can be compared lexicographically
                    if latest_filed is None or filed > latest_filed:
                        latest_filed = filed

    return latest_filed

def get_cik_for_ticker(company_ticker: str):
    project_root = Path(__file__).parent.parent.parent.parent
    ticker_cik_path = project_root / "data" / "ticker_cik_map.json"
    with open(ticker_cik_path, "r") as f:
        ticker_cik_map = json.load(f)
    cik = ticker_cik_map.get(company_ticker.upper())
    if not cik:
        raise ValueError(f"CIK not found for ticker: {company_ticker}")
    return cik

def download_companyfacts(company_ticker: str) -> dict:
    cik = get_cik_for_ticker(company_ticker)
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    resp = requests.get(url, headers=SEC_HEADERS)
    resp.raise_for_status()
    return resp.json()

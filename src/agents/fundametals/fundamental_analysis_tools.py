import json
from pathlib import Path

from filelock import FileLock

from agents.fundametals.utils import download_companyfacts, get_latest_filed_date, write_company_facts
from retrievers.fetch_all_financial_statements import FetchAllFinancialStatements
from retrievers.run_all_retrievers import RunAllRetrievers
from enum import Enum

class MetadataType(Enum):
    CASHFLOW_STATEMENT = 1
    INCOME_STATEMENT = 2
    BALANCE_SHEET = 3

class FundamentalsManager:

    def __init__(self):
        self._raw_facts_cache = {}
    
    def ensure_up_to_date(self, company_ticker: str, metadata_type: MetadataType):
        ticker = company_ticker.upper()

        project_root = Path(__file__).parent.parent.parent.parent
        company_dir = project_root / "data" / ticker
        lock_path = company_dir / ".lock"

        company_dir.mkdir(parents=True, exist_ok=True)
        if ticker in self._raw_facts_cache:
                company_facts = self._raw_facts_cache.get(ticker)
        else:
                company_facts = download_companyfacts(ticker)
                self._raw_facts_cache[ticker] = company_facts

        lock = FileLock(str(lock_path))
        with lock:
            # Re-check freshness INSIDE lock
            latest_filed = get_latest_filed_date(company_facts)
            current_company_facts_path = project_root / "data" / ticker / "raw" / "companyfacts.json"

            metadata = self._load_metadata(ticker, metadata_type)

            if current_company_facts_path.exists() and metadata and metadata.get("processed_date") >= latest_filed:
                return

            # Recompute
            write_company_facts(company_facts, ticker)

            run_all_retrievers = RunAllRetrievers()
            run_all_retrievers.process_financial_statements(ticker)

    
    def _load_metadata(ticker: str, metadata_type):
        fetch_all_financial_statements = FetchAllFinancialStatements()
        match metadata_type:
            case MetadataType.INCOME_STATEMENT:
                return fetch_all_financial_statements.fetch_income_statement(ticker)
            case MetadataType.BALANCE_SHEET:
                return fetch_all_financial_statements.fetch_balance_sheet(ticker)
            case MetadataType.CASHFLOW_STATEMENT:
                return fetch_all_financial_statements.fetch_cash_flow_statement(ticker)

class FundamentalAnalysisTools:
    
    def __init__(self):
        self.fundamentals_manager = FundamentalsManager()
        self.fetch_all_financial_statements = FetchAllFinancialStatements()

    def get_cash_flow_statement_facts(self, company_ticker: str):
        ticker = company_ticker.upper()
        self.fundamentals_manager.ensure_up_to_date(ticker, MetadataType.CASHFLOW_STATEMENT)
        cash_flow_statement = self.fetch_all_financial_statements.fetch_cash_flow_statement(ticker)
        return cash_flow_statement

    def get_income_statement_facts(self, company_ticker: str):
        ticker = company_ticker.upper()
        self.fundamentals_manager.ensure_up_to_date(ticker, MetadataType.INCOME_STATEMENT)
        income_statement = self.fetch_all_financial_statements.fetch_income_statement(ticker)
        return income_statement
    
    def get_balance_sheet_facts(self, company_ticker: str):
        ticker = company_ticker.upper()
        self.fundamentals_manager.ensure_up_to_date(ticker, MetadataType.BALANCE_SHEET)
        balance_sheet_facts = self.fetch_all_financial_statements.fetch_balance_sheet(ticker)
        return balance_sheet_facts



        
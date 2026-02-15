import json
from pathlib import Path

# Import the retriever classes and their run method
from balance_sheet.balance_sheet_retriever import run as run_balance_sheet
from cash_flow_statement.cash_flow_statement_retriever import run as run_cash_flow_statement
from income_statement.income_statement_retriever import run as run_income_statement


# =========================
# RUN ALL RETRIEVERS
# =========================

class RunAllRetrievers:
    def __init__(self):
        self.balance_sheet_retriever = "balance_sheet"
        self.cash_flow_statement_retriever = "cash_flow_statement"
        self.income_statement_retriever = "income_statement"

    def process_financial_statements(self, company_ticker: str):
        """
        Process financial statements for a given company ticker
        
        Args:
            company_ticker: Company ticker symbol
            companyfacts_path: Path to the companyfacts JSON file
            registry_path: Path to the registry JSON file
        """

        company_ticker = company_ticker.upper()
        raw_path = f"data/{company_ticker}/raw/company_facts.json"
        registry_path = "src/retrievers/registry/sec_facts_canonical_mappings_v1.json"
        normalized = f"data/{company_ticker}/normalized"
        derived = f"data/{company_ticker}/derived"

        # Run balance sheet retriever
        run_balance_sheet(company_ticker, raw_path, registry_path, normalized)

        # Run cash flow statement retriever
        run_cash_flow_statement(company_ticker, raw_path, registry_path, normalized, derived)

        # Run income statement retriever
        run_income_statement(company_ticker, raw_path, registry_path, normalized)

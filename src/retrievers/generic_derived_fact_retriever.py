from retrievers.generic_direct_fact_retriever import FactType
import json
import logging

# =========================
# LOGGING
# =========================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def derive_binary_subtraction(
    company,
    concept_name,
    spec,
    normalized_facts
):
    derived = []
    facts_by_period = index_facts_by_period(normalized_facts)
    left_key, right_key = spec["derived_from"]

    for period, facts in facts_by_period.items():
        left = facts.get(left_key)
        right = facts.get(right_key)

        # Fail closed
        if not left or not right:
            continue

        # Constraint: same currency
        if spec["constraints"].get("same_currency"):
            if left["currency"] != right["currency"]:
                continue

        value = left["value"] - right["value"]

        derived.append({
            "company": company,
            "statement": spec["statement"],
            "concept": concept_name,
            "value": value,
            "currency": left["currency"],
            "period": period,
            "reported": False,
            "derived_from": spec["derived_from"],
            "derivation_type": spec["derivation_type"],
            "confidence": "high"
        })

    return derived

def index_facts_by_period(normalized_facts):
    """
    Returns:
    {
        "Q2-2023": {
            "operating_cash_flow": {...},
            "capital_expenditure": {...}
        }
    }
    """
    index = {}

    for fact in normalized_facts:
        period = fact["period"]
        concept = fact["concept"]

        index.setdefault(period, {})
        index[period][concept] = fact

    return index


DERIVATION_HANDLERS = {
    "binary_subtraction": derive_binary_subtraction
}

class GenericDerivedFactRetriever:
    """
    Generic retriever for extracting and normalizing derived facts
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

    def extract_derived_facts(self, normalized_facts):
        """
        Extract derived facts based on registry specifications
        
        Returns:
            List of derived normalized facts
        """
        derived_all = []

        for concept_name, spec in self.registry.items():
            derivation_type = spec["derivation_type"]
            handler = DERIVATION_HANDLERS.get(derivation_type)

            if not handler:
                continue  # unknown derivation type

            derived = handler(
                company=self.company_ticker,
                concept_name=concept_name,
                spec=spec,
                normalized_facts=normalized_facts
            )

            derived_all.extend(derived)

        return derived_all
    
    def write(self, facts, write_dir, processed_date):
        """
        Write derived facts to storage
        
        Args:
            facts: List of derived normalized facts
            project_root: Path to project root directory
        """
        output_file = write_dir / f"{self.statement_type.value}.json"

        payload = {
            "company": self.company_ticker,
            "statement": self.statement_type.value,
            "processed_date": processed_date,
            "facts": facts
        }

        with open(output_file, "w") as f:
            json.dump(payload, f, indent=2)
        
        logger.info(f"Written {len(facts)} facts to {output_file}")
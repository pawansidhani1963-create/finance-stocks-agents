# Fundamentals Agent – Canonical Data Specification (v1.0)

This document defines the **canonical fundamentals data contract** used by the Fundamentals Agent.

The Fundamentals Agent is a **fact-normalization agent**.  
It describes economic reality exactly as reported, independent of source.

## Rules:

- start == null → point_in_time

- start == fiscal_year_start → ytd

- otherwise → discrete

---

## 1. Role of the Fundamentals Agent

The Fundamentals Agent is responsible for:

- Collecting authoritative financial facts
- Normalizing facts into a provider-agnostic schema
- Preserving period, units, and provenance
- Computing **mechanical, deterministic derived metrics**

The Fundamentals Agent does **not**:
- Interpret financial health
- Assign quality or risk judgments
- Produce investment signals

---

## 2. Entity Metadata

Identifying information for the reporting entity.

| Field | Description | Example |
|-----|------------|--------|
| ticker | Trading symbol | NVDA |
| cik | SEC Central Index Key | 0001045810 |
| company_name | Legal registrant name | NVIDIA Corporation |
| exchange | Primary exchange | NASDAQ |
| reporting_currency | Reporting currency | USD |
| fiscal_year_end | Fiscal year end month | January |

---

## 3. Provenance & Reporting Context (Required)

Every reported fact **must include provenance**.

| Field | Description |
|-----|-------------|
| source | Data origin (e.g., SEC) |
| form | Filing type (10-K, 10-Q) |
| filing_date | Date filed with regulator |
| accession_number | SEC accession number |
| period_start | Start of reporting period |
| period_end | End of reporting period |
| frame | FY / Q1 / Q2 / Q3 / Q4 |

---

## 4. Income Statement (Period-Based)

Income statement facts represent **activity over a period**.

### 4.1 Required Annual Metrics

| Canonical Field | Description |
|----------------|-------------|
| revenue | Total revenue |
| gross_profit | Revenue minus cost of goods sold |
| operating_income | Income from operations |
| net_income | Net income attributable to common shareholders |
| eps_diluted | Diluted earnings per share |

Minimum history: **5–10 fiscal years**

---

### 4.2 Optional Quarterly Metrics

Same canonical fields as annual, reported quarterly.

Quarterly data must be normalized to:
- **Standalone quarter values**
- **Not cumulative unless explicitly flagged**

---

## 5. Balance Sheet (Point-in-Time)

Balance sheet facts represent **financial position at period end**.

| Canonical Field | Description |
|----------------|-------------|
| total_assets | Total assets |
| total_liabilities | Total liabilities |
| total_equity | Shareholders' equity |
| cash_and_equivalents | Cash and cash equivalents |
| short_term_debt | Debt due within one year |
| long_term_debt | Debt due after one year |

---

## 6. Cash Flow Statement (Period-Based)

Cash flow facts represent **cash movement over a period**.

| Canonical Field | Description |
|----------------|-------------|
| operating_cash_flow | Cash generated from operations |
| capital_expenditure | Cash spent on property, plant, and equipment |
| free_cash_flow | Operating cash flow minus CapEx (derived if absent) |
| financing_cash_flow | Net cash from financing activities |

All cash flow values are normalized to **positive magnitudes**.

---

## 7. Share & Capital Structure

Share-related facts must distinguish **point-in-time** vs **period-average**.

| Canonical Field | Description |
|----------------|-------------|
| shares_outstanding | End-of-period shares outstanding |
| weighted_avg_shares_basic | Period-average basic shares |
| weighted_avg_shares_diluted | Period-average diluted shares |

---

## 8. Derived Metrics (Mechanical Only)

Derived metrics are computed deterministically from canonical facts.

### 8.1 Growth Metrics

| Metric | Definition |
|------|-----------|
| revenue_cagr | Revenue CAGR (3Y / 5Y / 10Y) |
| eps_cagr | EPS CAGR (3Y / 5Y) |
| fcf_cagr | Free cash flow CAGR (3Y / 5Y) |

---

### 8.2 Profitability Metrics

| Metric | Formula |
|------|---------|
| gross_margin | gross_profit / revenue |
| operating_margin | operating_income / revenue |
| net_margin | net_income / revenue |

---

### 8.3 Capital Efficiency Metrics

| Metric | Formula |
|------|---------|
| roe | net_income / total_equity |
| roic | nopat / invested_capital |

---

### 8.4 Financial Strength Metrics

| Metric | Formula |
|------|---------|
| debt_to_equity | total_debt / total_equity |
| net_debt | total_debt − cash_and_equivalents |
| interest_coverage | operating_income / interest_expense |

---

## 9. Canonical Output Structure

The Fundamentals Agent outputs a single normalized fundamentals object that conforms to this specification.

The output contains:

- **Canonical financial facts** – Authoritative figures from SEC filings
- **Mechanical derived metrics** – Deterministically computed ratios and growth rates
- **Explicit provenance** – Source, form, filing date, and period information

The output does **not** contain:
- Interpretation, scoring, or opinions
- Investment signals or recommendations
- Comparative assessments or quality judgments

---

## 10. Output Sections (Logical Layout)

The output is logically divided into the following sections:

1. **Entity** – Company identifying metadata
2. **Provenance** – Filing source and temporal context
3. **Financial Statements** – Income, balance sheet, cash flow data
4. **Share & Capital Data** – Share counts and capital structure
5. **Derived Metrics** – Mechanical computations

Each section is **mandatory** unless explicitly marked **optional**.

---

## 11. Entity Section

The Entity section contains identifying metadata for the reporting company.

This section is **static across periods** and does not change with reporting dates.

| Field | Description |
|-----|-------------|
| ticker | Trading symbol |
| cik | SEC Central Index Key |
| company_name | Legal registrant name |
| exchange | Primary exchange |
| reporting_currency | Financial reporting currency |
| fiscal_year_end | Fiscal year end month |

---

## 12. Provenance Section

The Provenance section describes where and when the reported facts originate.

**Each reporting period must have its own provenance entry.**

| Field | Description |
|-----|-------------|
| source | Data source (e.g., SEC) |
| form | Filing type (10-K, 10-Q, 10-K/A) |
| filing_date | Date filed with regulator |
| accession_number | SEC accession identifier |
| period_start | Start date of reporting period |
| period_end | End date of reporting period |
| frame | Fiscal frame (FY, Q1, Q2, Q3, Q4) |

**Multiple provenance entries may exist due to:**

- Amended filings (10-K/A, 10-Q/A)
- Restatements
- Multiple reporting periods (annual + quarterly)

---

## 13. Financial Statements Section

Financial statements are grouped by statement type and reporting period.

### 13.1 Income Statement

Income statement data represents **activity over a period**.

**Periods supported:**
- Annual
- Quarterly

Each period includes the canonical income statement fields defined in **Section 4**.

**Normalization rules:**
- Cumulative and standalone quarterly values must be normalized before inclusion
- Quarterly data must represent standalone quarter activity, not year-to-date

### 13.2 Balance Sheet

Balance sheet data represents **financial position at a specific point in time**.

Each entry corresponds to a **fiscal period end date** (e.g., December 31).

**Normalization rules:**
- Only point-in-time values are permitted in this section
- No averages or period-based adjustments

### 13.3 Cash Flow Statement

Cash flow data represents **cash movement over a reporting period**.

**Periods supported:**
- Annual
- Quarterly

**Normalization rules:**
- Cash flow values must be normalized to consistent sign conventions prior to output
- Operating activities are positive when cash is generated; negative when consumed

---

## 14. Share & Capital Data Section

This section contains share count and capital structure information.

**Point-in-time and period-average concepts must be kept separate.**

| Field | Description |
|-----|-------------|
| shares_outstanding | End-of-period shares outstanding |
| weighted_avg_shares_basic | Period-average basic shares |
| weighted_avg_shares_diluted | Period-average diluted shares |

---

## 15. Derived Metrics Section

Derived metrics are computed **deterministically** from canonical facts.

They **must**:

- ✅ Be reproducible from canonical inputs
- ✅ Use no external data
- ✅ Contain no judgment or classification
- ✅ Be documented with their formula

### 15.1 Growth Metrics

Revenue, EPS, and free cash flow growth over standard multi-year windows (3Y, 5Y, 10Y).

**Example:**
```
revenue_cagr_5y = (revenue_fy2024 / revenue_fy2019) ^ (1/5) - 1
```

### 15.2 Profitability Metrics

Margins computed directly from income statement facts.

**Example:**
```
net_margin = net_income / revenue
```

### 15.3 Capital Efficiency Metrics

Returns computed from income statement and balance sheet data.

**Example:**
```
roe = net_income / total_equity
```

### 15.4 Financial Strength Metrics

Leverage and coverage ratios computed from balance sheet and income statement data.

**Example:**
```
debt_to_equity = total_debt / total_equity
interest_coverage = operating_income / interest_expense
```

---

## 16. Output Constraints (Hard Rules)

The Fundamentals Agent output **must never** include:

❌ Provider-specific field names (e.g., `us-gaap:NetIncomeLoss`)  
❌ XBRL namespaces or tags (e.g., `us-gaap`, `dei`, `srt`)  
❌ HTML or PDF derived values  
❌ Interpretive labels or opinions  
❌ External data not derived from canonical facts  

**Any output violating these rules is invalid.**

---

## 17. Provider Abstraction Policy

Data providers are **implementation details** and must not leak into the output.

| Provider Type | Status |
|-----|--------|
| SEC XBRL | Authoritative |
| Market data APIs | Supplementary |
| Scraped sources | Fallback only |

**Provider changes must not affect the canonical schema.**

If SEC changes its XBRL tags or a provider deprecates an API, the canonical output remains identical.

---

## 18. Versioning

| Item | Value |
|-----|-------|
| Current version | v1.0 |
| Breaking change policy | Major version bump required |
| Backward compatibility | Not guaranteed across major versions |

**Downstream agents must explicitly declare supported versions** (e.g., `requires: Fundamentals v1.x`).

---

## 19. Non-Negotiable Principle

> **The Fundamentals Agent records facts and mechanical truths.**
> 
> **Interpretation, judgment, and decision-making belong exclusively to downstream agents.**

This separation of concerns ensures:
- Auditability and reproducibility
- Decoupling of data from analysis
- Clear responsibility boundaries
- Testability and validation

The Fundamentals Agent is a decision-making system whose decisions are constrained to interpretation and reasoning, while all data truth, normalization, and derivation decisions are handled deterministically by tools.
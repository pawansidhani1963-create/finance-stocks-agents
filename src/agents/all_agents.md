# Finance Agents Architecture

## Overview
This document outlines the multi-agent system designed to analyze stocks from multiple perspectives and synthesize conflicting signals into actionable insights.

---

## 1. Planner Agent

### Responsibility
- **Primary Role**: Orchestrate the analysis workflow
- **Decision Making**: Determines which specialist agents to invoke based on user query
- **Query Routing**: Routes questions to appropriate specialized agents

### Inputs
- User question/prompt
- Available agents registry

### Outputs
- Analysis plan (list of agents to invoke)
- Priority/sequence of analysis
- Required parameters for each agent

### Key Capabilities
- Natural language understanding
- Query decomposition
- Agent selection logic

---

## 2. Specialist Agents

### 2.1 Fundamentals Agent

#### Responsibility
Analyze company financial health and valuation metrics

#### Key Metrics
- **Growth Metrics**
  - Revenue growth (YoY, CAGR)
  - Earnings growth
  - Free cash flow growth

- **Profitability Metrics**
  - Gross margin
  - Operating margin
  - Net margin
  - EBITDA margin

- **Return Metrics**
  - Return on Invested Capital (ROIC)
  - Return on Equity (ROE)
  - Return on Assets (ROA)

- **Leverage Metrics**
  - Debt-to-Equity ratio
  - Debt-to-EBITDA
  - Interest coverage ratio
  - Net debt position

- **Valuation & Peer Comparison**
  - P/E ratio vs peers
  - P/B ratio vs peers
  - EV/EBITDA vs peers
  - PEG ratio
  - Price-to-Sales ratio

#### Tools Used
- SEC EDGAR API (10-K, 10-Q, 8-K filings)
- Company financials database
- Peer comparison database

#### Output Structure
```json
{
  "agent": "Fundamentals",
  "timestamp": "2024-12-21T10:30:00Z",
  "company": "TICKER",
  "analysis": {
    "growth": { "revenue_growth": 0.12, "earnings_growth": 0.15 },
    "profitability": { "net_margin": 0.25, "roic": 0.18 },
    "leverage": { "debt_to_equity": 0.45, "interest_coverage": 8.5 },
    "valuation": { "pe_ratio": 28, "peer_avg_pe": 32 }
  },
  "score": 8.2,
  "confidence": 0.92,
  "signal": "STRONG_BUY" | "BUY" | "HOLD" | "SELL" | "STRONG_SELL"
}
```

---

### 2.2 Technical Agent

#### Responsibility
Analyze price trends, momentum, and support/resistance levels

#### Key Indicators
- **Trend Analysis**
  - 50-Day Moving Average (DMA)
  - 200-Day Moving Average (DMA)
  - Trend direction and strength
  - Support and resistance levels

- **Momentum Indicators**
  - Relative Strength Index (RSI): overbought/oversold detection
  - MACD (Moving Average Convergence Divergence): trend confirmation
  - Momentum oscillator

- **Volume Analysis**
  - Volume trends
  - On-balance volume (OBV)
  - Volume-weighted average price (VWAP)

#### Tools Used
- Historical price/volume data
- Technical indicator calculation library
- Chart pattern recognition

#### Output Structure
```json
{
  "agent": "Technical",
  "timestamp": "2024-12-21T10:30:00Z",
  "company": "TICKER",
  "analysis": {
    "trend": {
      "short_term": "UPTREND",
      "sma_50": 180.5,
      "sma_200": 175.2,
      "strength": 0.7
    },
    "momentum": {
      "rsi": 65,
      "rsi_signal": "APPROACHING_OVERBOUGHT",
      "macd": "BULLISH_CROSS"
    },
    "levels": {
      "resistance": [185, 190],
      "support": [170, 165]
    }
  },
  "score": 7.5,
  "confidence": 0.85,
  "signal": "BUY" | "HOLD" | "SELL"
}
```

---

### 2.3 News & Sentiment Agent

#### Responsibility
Analyze news flow, earnings events, and market sentiment

#### Key Signals
- **Earnings Events**
  - Earnings surprises (actual vs expected)
  - Guidance changes (raise/maintain/lower)
  - Forward guidance implications

- **Regulatory & Risk Factors**
  - SEC filings analysis (8-K events)
  - Regulatory announcements
  - Litigation or legal issues
  - Government policy impacts

- **Insider Activity**
  - Insider buy/sell activity
  - Form 4 filings analysis
  - Insider transaction trends

- **Market Sentiment**
  - News sentiment score (positive/negative/neutral)
  - News volume and velocity
  - Analyst rating changes
  - Social media sentiment

#### Tools Used
- News API integration
- NLP sentiment analysis
- SEC filings parser (8-K, Form 4)
- Analyst consensus data

#### Output Structure
```json
{
  "agent": "NewsSentiment",
  "timestamp": "2024-12-21T10:30:00Z",
  "company": "TICKER",
  "analysis": {
    "earnings": {
      "last_surprise": 0.05,
      "guidance_change": "RAISE",
      "next_date": "2025-01-15"
    },
    "regulatory": {
      "recent_events": ["Form 8-K filed"],
      "risk_level": "LOW"
    },
    "insider_activity": {
      "recent_buys": 3,
      "recent_sells": 1,
      "trend": "ACCUMULATION"
    },
    "sentiment": {
      "news_score": 0.72,
      "analyst_rating": 4.2,
      "sentiment_trend": "IMPROVING"
    }
  },
  "score": 7.8,
  "confidence": 0.88,
  "signal": "BUY" | "HOLD" | "SELL"
}
```

---

## 3. Synthesis Agent (Critical)

### Responsibility
- **Conflict Resolution**: Reconcile opposing signals from specialist agents
- **Scenario Generation**: Create multiple outcome scenarios
- **Uncertainty Quantification**: Explicitly state confidence and risks

### Input
- Outputs from all specialist agents
- User risk tolerance/investment horizon
- Market context and macro factors

### Key Functions

#### 3.1 Signal Reconciliation
**Example Conflict:**
```
Fundamentals Agent: STRONG_BUY (excellent metrics, cheap valuation)
Technical Agent: SELL (breaking support, MACD bearish)
News Agent: HOLD (mixed sentiment, no catalyst)
```

**Resolution:**
- Identify which signal is most reliable in current context
- Assess timing: technical vs fundamental mismatch often = entry opportunity
- Weight by conviction and recency

#### 3.2 Scenario Generation
Produces 3-5 scenarios with probabilities:

```json
{
  "agent": "Synthesis",
  "timestamp": "2024-12-21T10:30:00Z",
  "company": "TICKER",
  
  "final_signal": "BUY_WITH_CAUTION",
  "confidence_score": 0.72,
  
  "specialist_signals": {
    "fundamentals": { "signal": "STRONG_BUY", "score": 8.2 },
    "technical": { "signal": "SELL", "score": 4.5 },
    "sentiment": { "signal": "HOLD", "score": 6.8 }
  },
  
  "conflict_analysis": {
    "main_conflict": "Fundamentals bullish, technicals bearish",
    "interpretation": "Classic value opportunity with timing risk",
    "resolution": "BUY on weakness with defined stops"
  },
  
  "scenarios": [
    {
      "name": "Base Case - Resumption of Uptrend",
      "probability": 0.50,
      "target_price": 195,
      "target_timeframe": "3-6 months",
      "key_catalyst": "Positive earnings next quarter"
    },
    {
      "name": "Bear Case - Continued Weakness",
      "probability": 0.30,
      "target_price": 165,
      "target_timeframe": "1-3 months",
      "key_catalyst": "Macro recession fears"
    },
    {
      "name": "Bull Case - Acceleration",
      "probability": 0.20,
      "target_price": 220,
      "target_timeframe": "6-12 months",
      "key_catalyst": "Major product launch / market expansion"
    }
  ],
  
  "risks": [
    {
      "risk": "Valuation compression from macro slowdown",
      "probability": 0.35,
      "mitigation": "Position sizing, stop loss at 170"
    },
    {
      "risk": "Technical breakdown continues",
      "probability": 0.25,
      "mitigation": "Re-evaluate if breaks below 165"
    }
  ],
  
  "uncertainty_factors": [
    "Macro economic conditions",
    "Fed policy changes",
    "Competitive threats",
    "Execution risk on company initiatives"
  ],
  
  "recommendation": {
    "action": "BUY",
    "position_size": "MODERATE",
    "entry_points": [175, 170, 165],
    "stop_loss": 160,
    "target_price": 195,
    "investment_horizon": "6-12 months",
    "risk_reward_ratio": "1:1.5"
  }
}
```

#### 3.3 Uncertainty Quantification
Explicitly communicates:
- Confidence intervals for forecasts
- Key assumptions underlying analysis
- What would change the recommendation
- Tail risks and black swan scenarios

---

## Agent Communication Flow

```
┌─────────────────┐
│  User Question  │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│  Planner Agent      │
│  (Route & Prioritize)
└────────┬────────────┘
         │
    ┌────┼────┐
    │    │    │
    ▼    ▼    ▼
┌──────┐ ┌──────────┐ ┌──────────────┐
│Funda-│ │Technical │ │News/Sentiment│
│ment  │ │  Agent   │ │    Agent     │
└──┬───┘ └────┬─────┘ └──────┬───────┘
   │          │              │
   └──────────┼──────────────┘
              │
              ▼
      ┌───────────────────┐
      │ Synthesis Agent   │
      │ (Resolve Conflicts)
      │ (Generate Scenarios)
      │ (Quantify Uncertainty)
      └─────────┬─────────┘
              │
              ▼
      ┌───────────────────┐
      │ Final Recommendation
      │ & Actionable Output
      └───────────────────┘
```

---

## Output Standards

### All Agents Must Provide:
✅ Structured JSON output (not prose)
✅ Numeric scores (0-10 scale)
✅ Confidence levels (0-1 range)
✅ Clear signal (BUY/HOLD/SELL)
✅ Timestamp and data freshness
✅ Key assumptions listed
✅ Data sources cited

### Synthesis Agent Additionally:
✅ Conflict resolution narrative
✅ Multiple scenarios with probabilities
✅ Explicit uncertainty acknowledgment
✅ Risk/reward analysis
✅ Actionable recommendation

---


<!-- ...existing code... -->

## Implementation Framework

### Technology Stack

#### LangChain
**Purpose**: Build individual agent logic and tool integration
- **Agent Chains**: Define reasoning steps for each specialist agent
- **Tools**: Integrate data sources (SEC API, price data, news APIs)
- **Prompts**: Craft specialized prompts for each agent type
- **Output Parsing**: Structured JSON extraction from LLM responses
- **Memory**: Maintain context across multi-turn conversations

**Key Components Used:**
```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import JsonOutputParser
```

#### LangGraph
**Purpose**: Orchestrate multi-agent workflow and state management
- **State Machine**: Define agent states and transitions
- **Graph Execution**: Manage parallel/sequential agent execution
- **Memory Management**: Maintain shared state across agents
- **Conditional Routing**: Route to agents based on planner decisions
- **Error Handling**: Graceful degradation if individual agents fail

**Key Components Used:**
```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from typing import TypedDict
```

### Architecture Pattern

```
┌────────────────────────────────────────────┐
│        LangGraph State Graph               │
├────────────────────────────────────────────┤
│                                            │
│  ┌──────────────┐                         │
│  │ Input State  │                         │
│  └──────┬───────┘                         │
│         │                                  │
│         ▼                                  │
│  ┌─────────────────────────────┐          │
│  │  Planner Agent (LangChain)  │          │
│  │  - Parse user query         │          │
│  │  - Decide agent sequence    │          │
│  └──────────┬────────────────┘           │
│             │                             │
│    ┌────────┼────────┐                   │
│    │        │        │                   │
│    ▼        ▼        ▼                   │
│  ┌──────┐ ┌──────┐ ┌──────┐             │
│  │Fund. │ │Tech. │ │News/ │             │
│  │Agent │ │Agent │ │Sent. │             │
│  │(LC)  │ │(LC)  │ │Agent │             │
│  │+Tool │ │+Tool │ │(LC)  │             │
│  │Exec  │ │Exec  │ │+Tool │             │
│  └──┬───┘ └──┬──┘ └──┬───┘             │
│     │        │       │                  │
│     └────────┼───────┘                  │
│              │                          │
│              ▼                          │
│  ┌─────────────────────────────┐       │
│  │Synthesis Agent (LangChain)  │       │
│  │ - Reconcile signals         │       │
│  │ - Generate scenarios        │       │
│  │ - Quantify uncertainty      │       │
│  └──────────┬────────────────┘        │
│             │                          │
│             ▼                          │
│  ┌──────────────────────────┐         │
│  │ Final Output State       │         │
│  │ - Recommendation         │         │
│  │ - Confidence scores      │         │
│  │ - Scenarios & risks      │         │
│  └──────────────────────────┘         │
│                                        │
└────────────────────────────────────────────┘
```

---

<!-- ...existing code up to Next Steps... -->

## Implementation Details

### LangChain Agent Template

```python
from langchain import LLMChain, PromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import JsonOutputParser

class FundamentalsAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.agent_executor = self._build_executor()
    
    def _build_executor(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a financial fundamentals analyst..."),
            ("human", "{input}")
        ])
        
        agent = create_react_agent(self.llm, self.tools, prompt)
        return AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )
    
    def analyze(self, ticker: str) -> dict:
        result = self.agent_executor.invoke(
            {"input": f"Analyze fundamentals for {ticker}"}
        )
        return JsonOutputParser().parse(result["output"])
```

### LangGraph State Management

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

class AnalysisState(TypedDict):
    ticker: str
    user_query: str
    plan: List[str]
    fundamentals_analysis: dict
    technical_analysis: dict
    sentiment_analysis: dict
    final_recommendation: dict
    errors: List[str]

class FinanceAgentGraph:
    def __init__(self, llm):
        self.llm = llm
        self.graph = self._build_graph()
    
    def _build_graph(self):
        graph = StateGraph(AnalysisState)
        
        # Add nodes for each agent
        graph.add_node("planner", self.planner_node)
        graph.add_node("fundamentals", self.fundamentals_node)
        graph.add_node("technical", self.technical_node)
        graph.add_node("sentiment", self.sentiment_node)
        graph.add_node("synthesis", self.synthesis_node)
        
        # Define routing logic
        graph.add_edge("planner", "fundamentals")
        graph.add_conditional_edges(
            "fundamentals",
            self.route_from_fundamentals,
            {
                "technical": "technical",
                "synthesis": "synthesis"
            }
        )
        
        graph.add_edge("technical", "sentiment")
        graph.add_edge("sentiment", "synthesis")
        graph.add_edge("synthesis", END)
        
        graph.set_entry_point("planner")
        return graph.compile()
    
    def run(self, ticker: str, query: str) -> dict:
        initial_state = {
            "ticker": ticker,
            "user_query": query,
            "plan": [],
            "errors": []
        }
        return self.graph.invoke(initial_state)
```

---

## Next Steps
1. Set up LangChain environment and LLM configuration
2. Implement Planner Agent with query routing logic
3. Build Fundamentals Agent with SEC data tools
4. Develop Technical Agent with TA-Lib tools
5. Create News/Sentiment Agent with NLP tools
6. Implement Synthesis Agent for conflict resolution
7. Build LangGraph state graph for orchestration
8. Create error handling and fallback mechanisms
9. Build unified API layer for all agents
10. Create dashboard/reporting interface

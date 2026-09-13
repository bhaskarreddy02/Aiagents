# 🚀 Aiagents — Frontier AI Venture & Intelligence Assistant
### Multi-Channel Conversational Agent Powered by Caspian SDK & Real-Time Intelligence Graph

> An autonomous, multi-channel intelligence agent that connects to **Email, Slack, Discord, Telegram, X/Twitter, and SMS** through a single unified handler. Ask questions and receive instant, grounded market insights across **7,600+ tech entities** — startups, products, arXiv papers, job openings, and breaking news signals.

---

## 🌟 Overview

**Aiagents** bridges deep ecosystem intelligence directly into everyday communication channels. Rather than requiring users to manually search dozens of platforms or navigate complex dashboards, Aiagents enables founders, investors, researchers, and engineers to query verified venture and technology intelligence through the chat channels they already use.

Built on top of the **Caspian SDK**, the agent uses a **single `on_message` handler** to answer inquiries identically and consistently across every connected channel.

---

## ✨ Key Capabilities

- **🚀 AI Startups & Funding Intelligence**:
  - Deep data on 2,500+ startups: team size, YC batches, business models, websites, and founder backgrounds.
- **🛠️ AI Products & Pricing**:
  - 2,500+ AI products categorized with clear pricing models (Free, Freemium, Paid, Enterprise).
- **📄 Research Papers & Breakthroughs**:
  - 2,500+ arXiv and Hugging Face papers with authors, code repository links, and impact metrics.
- **💼 Verified AI & Tech Job Openings**:
  - Live, 24-hour fresh openings from 5 job boards filtered by company, role family, and remote status.
- **📰 Curated Tech News Signals**:
  - Real-time headlines and analysis aggregated from TechCrunch, Wired, MIT Tech Review, Ars Technica, and AI News.
- **🔍 Grounded Responses & Zero Hallucinations**:
  - Powered by deterministic entity resolution, returning factual data from pre-indexed and continuously updated intelligence pipelines.

---

## 🌐 Multi-Channel Support

With Caspian's architecture, one agent is deployed across multiple communication touchpoints:

| Channel | Mode | Configuration |
| :--- | :--- | :--- |
| **Email** | Hosted | Active mailbox: `fernando@agents.trycaspianai.com` |
| **Discord** | Socket / Hosted | Connects via Bot Token or Webhook |
| **Slack** | Socket Mode / Webhook | Connects via Bot & App Tokens |
| **Telegram** | Hosted / Polling | Connects via BotFather Token |
| **X (Twitter)** | Hosted | Connects via Access Token & User ID |
| **SMS / Phone** | Hosted | Connects via Twilio / Telnyx |

---

## ⚙️ Architecture

```
                  ┌────────────────────────────────────────┐
                  │            Caspian Gateway             │
                  │   (Email / Slack / Discord / etc.)     │
                  └───────────────────┬────────────────────┘
                                      │ Inbound Event
                                      ▼
                        ┌───────────────────────────┐
                        │    caspian_agent.py       │
                        │    @cx.on_message()       │
                        │  (Single Unified Handler) │
                        └─────────────┬─────────────┘
                                      │ Query Lookup
                                      ▼
     ┌─────────────────────────────────────────────────────────────┐
     │                Aiagents Intelligence Engine                 │
     ├──────────────┬──────────────┬──────────────┬────────────────┤
     │   Startups   │   Products   │    Papers    │  Jobs & News   │
     │  (2,500 CSV) │  (2,500 CSV) │  (2,500 CSV) │  (Live Feeds)  │
     └──────────────┴──────────────┴──────────────┴────────────────┘
                                      │ Formatted Answer
                                      ▼
                        ┌───────────────────────────┐
                        │      thread.post()        │
                        │   (Reply to Originating   │
                        │         Channel)          │
                        └───────────────────────────┘
```

1. **Caspian SDK Core**: Orchestrates channel connections and manages gateway polling or socket listening.
2. **Unified Dispatcher**: The `@cx.on_message()` decorator receives incoming threads regardless of the originating platform.
3. **Knowledge Base Matching**: Queries the pre-resolved entity index and extracts relevant entity links, descriptions, and metadata.
4. **Thread Reply**: Posts structured markdown responses directly back to the active user thread with `thread.post()`.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Caspian SDK installed:
```bash
pip install caspian-sdk
```

### 2. Environment Setup
Add your credentials to `.env`:
```env
CASPIAN_API_KEY=your_caspian_api_key_here
CASPIAN_BASE_URL=https://api.trycaspianai.com
```

### 3. Running the Agent

#### Run on Email:
```bash
python src/caspian_agent.py --channel email --username assistant
```
*The agent will immediately start listening for inbound emails at `fernando@agents.trycaspianai.com`.*

#### Run on Discord or Slack:
```bash
# Discord
python src/caspian_agent.py --channel discord

# Slack
python src/caspian_agent.py --channel slack
```

---

## 🧪 Testing & Verification

Run the automated test suite to verify handlers and knowledge base queries:
```bash
python -m pytest tests/test_caspian_agent.py -v
```

Tests cover:
- Intent parsing & welcome greeting
- Startup intelligence lookups
- Active job queries
- Caspian client initialization
- Message dispatching via `thread.post()`

---

## 📂 Project Structure

```
Aiagents/
├── src/
│   ├── caspian_agent.py       # Caspian agent, unified on_message handler, and runner
│   ├── config.py              # Configuration & Caspian credentials
│   ├── crawler/               # Multi-source crawlers (YC, arXiv, HF, news, jobs)
│   ├── entity_resolution/     # Deterministic resolver & RapidFuzz matcher
│   ├── pipeline/              # Continuous monitoring & state store
│   └── schemas/               # Pydantic data schemas
├── data/                      # 7,600+ entity CSV datasets
├── tests/
│   └── test_caspian_agent.py  # Unit tests for Caspian integration
├── requirements.txt           # Python dependencies (includes caspian-sdk)
├── .env                       # Environment variables
└── README.md
```

---

## 📜 License
MIT License.

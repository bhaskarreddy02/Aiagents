"""
Caspian Communication Agent
One handler that answers every channel (Email, Slack, Discord, Telegram, X, SMS)
Integrated with Caspian SDK and GraphOne/Aiagents Data Intelligence
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from caspian import Caspian, Thread, Message, HandlerContext
from src.config import CASPIAN_API_KEY, CASPIAN_BASE_URL, DATA_DIR
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("CaspianAgent")


class KnowledgeBase:
    """Lightweight access to Aiagents datasets for automated query response."""
    def __init__(self):
        self.startups = self._load_csv("startups.csv")
        self.products = self._load_csv("products.csv")
        self.papers = self._load_csv("research_papers.csv")
        self.jobs = self._load_csv("jobs.csv")
        self.news = self._load_csv("news.csv")

    def _load_csv(self, filename: str) -> List[Dict[str, Any]]:
        path = DATA_DIR / filename
        if path.exists():
            try:
                return pd.read_csv(path).fillna("").to_dict(orient="records")
            except Exception as e:
                logger.warning(f"Failed to load {filename}: {e}")
        return []

    def answer_query(self, text: str) -> str:
        q = text.lower().strip()
        if not q or q in ["hi", "hello", "hey", "help"]:
            return (
                "Hello! I am the Aiagents Communication Agent powered by Caspian.\n\n"
                "I can answer questions about our real-time tech intelligence graph:\n"
                "- AI Startups & funding\n"
                "- New AI Products\n"
                "- arXiv Research Papers\n"
                "- Tech Job Openings\n"
                "- Industry News\n\n"
                f"Currently tracking {len(self.startups)} startups, {len(self.products)} products, "
                f"and {len(self.jobs)} jobs. How can I help you today?"
            )

        # Check for startup inquiry
        if any(w in q for w in ["startup", "company", "founder", "funded"]):
            matched = [s for s in self.startups if any(term in str(s.values()).lower() for term in q.split() if len(term) > 3)][:3]
            if matched:
                lines = ["Here are matching startups from the intelligence graph:"]
                for s in matched:
                    name = s.get("content.entityName") or s.get("name") or "Unknown"
                    desc = s.get("content.data.description") or s.get("description") or "N/A"
                    lines.append(f"- **{name}**: {desc[:150]}...")
                return "\n".join(lines)

        # Check for jobs inquiry
        if any(w in q for w in ["job", "hiring", "career", "role", "position"]):
            matched = [j for j in self.jobs if any(term in str(j.values()).lower() for term in q.split() if len(term) > 3)][:3]
            if matched:
                lines = ["Here are active job openings from the intelligence graph:"]
                for j in matched:
                    title = j.get("content.data.title") or j.get("title") or "Role"
                    company = j.get("content.entityName") or j.get("company") or "Company"
                    lines.append(f"- **{title}** at {company}")
                return "\n".join(lines)

        # Check for research papers
        if any(w in q for w in ["paper", "research", "arxiv", "study"]):
            matched = [p for p in self.papers if any(term in str(p.values()).lower() for term in q.split() if len(term) > 3)][:3]
            if matched:
                lines = ["Here are relevant research papers from the intelligence graph:"]
                for p in matched:
                    title = p.get("content.data.title") or p.get("title") or "Research"
                    lines.append(f"- **{title}**")
                return "\n".join(lines)

        # General intelligence status summary
        return (
            f"Aiagents Intelligence Graph Report:\n"
            f"- Startups Tracked: {len(self.startups)}\n"
            f"- AI Products: {len(self.products)}\n"
            f"- Research Papers: {len(self.papers)}\n"
            f"- Active Jobs: {len(self.jobs)}\n"
            f"- News Articles: {len(self.news)}\n\n"
            f"Query received: \"{text}\".\n"
            f"For deep entity exploration, explore our web dashboard or ask specific questions!"
        )


# Initialize Knowledge Base
kb = KnowledgeBase()

# Initialize Caspian SDK
api_key = CASPIAN_API_KEY or os.environ.get("CASPIAN_API_KEY", "")
base_url = CASPIAN_BASE_URL or os.environ.get("CASPIAN_BASE_URL", "https://api.trycaspianai.com")

if not api_key:
    logger.error("CASPIAN_API_KEY not found in environment or config!")

cx = Caspian(api_key=api_key, base_url=base_url)


def connect_channel(channel: str = "email", **kwargs):
    """
    Connect a channel dynamically.
    - email: username='assistant' -> assistant@agents.trycaspianai.com
    - discord: via='self-host', bot_token='...' or hosted
    - slack: via='self-host', bot_token='...', app_token='...'
    - telegram: bot_token='...'
    """
    logger.info(f"Connecting Caspian channel: {channel} with params: {kwargs}")
    conn = cx.channels.add(channel, **kwargs)
    logger.info(f"Channel {channel} connected: {conn}")
    return conn


# SINGLE HANDLER THAT ANSWERS EVERY CHANNEL
@cx.on_message()
def handle_message(thread: Thread, msg: Message, ctx: HandlerContext) -> None:
    """
    Unified Caspian message handler.
    Answers incoming inquiries across all connected channels (Email, Slack, Discord, etc.)
    """
    incoming_text = getattr(msg, "text", "") or ""
    channel = getattr(ctx, "channel", "unknown") if ctx else "unknown"
    logger.info(f"[Inbound Message via {channel}]: {incoming_text}")

    # Generate response from knowledge base
    response = kb.answer_query(incoming_text)

    # Post reply on thread
    logger.info(f"[Outbound Reply via {channel}]: {response[:80]}...")
    thread.post(response)


def listen(channel: Optional[str] = None):
    """
    Listens for incoming messages.
    - For self-hosted socket channels (e.g. Discord, Slack): calls cx.listen(channel)
    - For hosted channels (Email, Telegram, etc.): calls cx.run() to poll gateway events
    """
    # If a socket-based channel is specified and configured for self-host
    socket_channels = ["discord", "slack"]
    if channel and channel.lower() in socket_channels:
        try:
            owner = cx.channels.inbound_owner(channel)
            if owner == "local":
                logger.info(f"Starting socket listener for {channel} via cx.listen()...")
                return cx.listen(channel)
        except Exception as e:
            logger.warning(f"cx.listen({channel}) fallback to cx.run(): {e}")

    logger.info("Starting Caspian hosted listener loop (cx.run())...")
    logger.info("Listening for inbound events across all channels...")
    return cx.run()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Caspian Communication Agent")
    parser.add_argument("--channel", type=str, default="email", help="Channel to connect (default: email)")
    parser.add_argument("--username", type=str, default="assistant", help="Mailbox username for email (default: assistant)")
    parser.add_argument("--listen", action="store_true", default=True, help="Run listen() after connect")
    args = parser.parse_args()

    # Connect channel
    if args.channel == "email":
        conn = connect_channel("email", username=args.username)
        print(f"\nConnected to Caspian Email: {getattr(conn, 'address', 'active')}")
    else:
        conn = connect_channel(args.channel)
        print(f"\nConnected to Caspian channel: {args.channel}")

    print("\nCaspian Communication Agent is ready. Unified on_message handler active.")
    if args.listen:
        listen(args.channel)

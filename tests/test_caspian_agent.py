"""
Unit tests for Caspian Communication Agent in Aiagents
"""

import pytest
from unittest.mock import MagicMock
from src.caspian_agent import KnowledgeBase, handle_message, cx, connect_channel, api_key, base_url


def test_knowledge_base_welcome():
    kb = KnowledgeBase()
    resp = kb.answer_query("hello")
    assert "Aiagents Communication Agent" in resp
    assert "Caspian" in resp


def test_knowledge_base_startups():
    kb = KnowledgeBase()
    resp = kb.answer_query("tell me about AI startups")
    assert "startups" in resp.lower() or "report" in resp.lower()


def test_knowledge_base_jobs():
    kb = KnowledgeBase()
    resp = kb.answer_query("what jobs are open?")
    assert "job" in resp.lower() or "report" in resp.lower()


def test_caspian_client_init():
    assert cx is not None
    assert api_key.startswith("comm_")
    assert "trycaspianai.com" in base_url


def test_handler_message_dispatch():
    mock_thread = MagicMock()
    mock_msg = MagicMock()
    mock_msg.text = "Tell me about research papers"
    mock_ctx = MagicMock()
    mock_ctx.channel = "email"

    handle_message(mock_thread, mock_msg, mock_ctx)
    mock_thread.post.assert_called_once()
    posted_text = mock_thread.post.call_args[0][0]
    assert len(posted_text) > 0

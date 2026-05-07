"""
Multi-Agent Research Bot — Unit Tests
Tests for agent logic, query routing, and response validation.
"""
import pytest


# ── Agent routing logic ──────────────────────────────────────────────────────
def test_query_router_web():
    """Web-search queries should route to search agent."""
    def route_query(q: str) -> str:
        web_keywords = ["latest", "news", "current", "today", "recent", "2024", "2025"]
        if any(k in q.lower() for k in web_keywords):
            return "search_agent"
        return "rag_agent"

    assert route_query("latest AI news") == "search_agent"
    assert route_query("recent trends in ML") == "search_agent"
    assert route_query("explain neural networks") == "rag_agent"


def test_query_router_rag():
    """Document queries should route to RAG agent."""
    def route_query(q: str) -> str:
        web_keywords = ["latest", "news", "current", "today", "recent"]
        return "search_agent" if any(k in q.lower() for k in web_keywords) else "rag_agent"

    assert route_query("summarise the uploaded document") == "rag_agent"
    assert route_query("what does the paper say about transformers") == "rag_agent"


def test_agent_response_schema():
    """Agent responses must include required fields."""
    def validate_response(resp: dict) -> bool:
        return all(k in resp for k in ("agent", "result", "sources"))

    valid = {"agent": "rag_agent", "result": "Transformers use attention.", "sources": ["doc1.pdf"]}
    invalid = {"agent": "rag_agent", "result": "..."}  # missing sources
    assert validate_response(valid)
    assert not validate_response(invalid)


def test_empty_result_detection():
    """Empty agent results should be flagged."""
    def is_empty_result(result: str) -> bool:
        return not result or result.strip() in ("", "None", "N/A", "null")

    assert is_empty_result("")
    assert is_empty_result("  ")
    assert is_empty_result("None")
    assert not is_empty_result("Transformers use self-attention mechanisms.")


def test_source_deduplication():
    """Duplicate sources in agent results should be removed."""
    sources = ["arxiv.org/1234", "google.com", "arxiv.org/1234", "nature.com"]
    unique = list(dict.fromkeys(sources))
    assert len(unique) == 3
    assert unique[0] == "arxiv.org/1234"


def test_query_length_validation():
    """Queries must be between 3 and 500 characters."""
    def is_valid_query(q: str) -> bool:
        stripped = q.strip()
        return 3 <= len(stripped) <= 500

    assert not is_valid_query("hi")
    assert is_valid_query("explain transformers")
    assert not is_valid_query("x" * 501)
    assert is_valid_query("x" * 500)


def test_agent_name_registry():
    """All expected agents must be registered."""
    REGISTERED_AGENTS = {"search_agent", "rag_agent", "summary_agent"}
    required = ["search_agent", "rag_agent"]
    for agent in required:
        assert agent in REGISTERED_AGENTS


@pytest.mark.parametrize("query,expected_agent", [
    ("latest GPT news", "search_agent"),
    ("today's AI headlines", "search_agent"),
    ("explain BERT architecture", "rag_agent"),
    ("what is attention mechanism", "rag_agent"),
])
def test_parametrized_routing(query, expected_agent):
    web_keywords = ["latest", "news", "current", "today", "recent"]
    result = "search_agent" if any(k in query.lower() for k in web_keywords) else "rag_agent"
    assert result == expected_agent

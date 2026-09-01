from pathlib import Path

from aegis.memory import MemoryStore
from langchain_core.embeddings import Embeddings


class FakeEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return [[float(len(text)), 1.0] for text in texts]

    def embed_query(self, text):
        return [float(len(text)), 1.0]


def test_memory_persists_and_reloads(tmp_path: Path):
    first = MemoryStore(tmp_path / "memory", FakeEmbeddings(), top_k=2)
    first.add("WATCHLIST:AAPL", {"type": "watchlist"})
    first.save()

    second = MemoryStore(tmp_path / "memory", FakeEmbeddings(), top_k=2)

    assert second.index_exists
    assert second.search("watchlist", 1)



    import pytest
from pydantic import ValidationError

from aegis.models import ResearchSummary


def test_research_summary_validates_schema():
    result = ResearchSummary(
        ticker="aapl",
        summary="Example summary",
        recent_headlines=["Headline"],
        recommendation="HOLD",
        confidence=0.75,
    )

    assert result.ticker == "AAPL"
    assert result.confidence == 0.75


def test_research_summary_rejects_invalid_confidence():
    with pytest.raises(ValidationError):
        ResearchSummary(
            ticker="AAPL",
            summary="Example",
            recommendation="BUY",
            confidence=1.5,
        )





        from pathlib import Path

import pytest

from langchain_core.embeddings import Embeddings

from aegis.memory import MemoryStore
from aegis.tools import build_custom_tools


class FakeEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return [[float(len(text)), 1.0] for text in texts]

    def embed_query(self, text):
        return [float(len(text)), 1.0]


def make_tools(tmp_path):
    memory = MemoryStore(tmp_path / "memory", FakeEmbeddings())
    tools = build_custom_tools(memory)
    return {tool.name: tool for tool in tools}


def test_add_and_list_watchlist(tmp_path: Path):
    tools = make_tools(tmp_path)

    assert "AAPL" in tools["add_to_watchlist"].invoke(
        {"ticker": "aapl"}
    )

    assert "AAPL" in tools["list_watchlist"].invoke({})


def test_position_size_rejects_negative_inputs(tmp_path: Path):
    tools = make_tools(tmp_path)

    with pytest.raises(ValueError):
        tools["calculate_position_size"].invoke(
            {
                "capital": -100000,
                "risk_pct": 1,
                "entry": 200,
                "stop": 190,
            }
        )


def test_position_size_rejects_equal_prices(tmp_path: Path):
    tools = make_tools(tmp_path)

    with pytest.raises(ValueError):
        tools["calculate_position_size"].invoke(
            {
                "capital": 100000,
                "risk_pct": 1,
                "entry": 200,
                "stop": 200,
            }
        )

from __future__ import annotations

import re

from langchain_core.tools import tool

from .memory import MemoryStore


_TICKER_RE = re.compile(r"^[A-Za-z][A-Za-z0-9.\-]{0,9}$")


def _validate_ticker(ticker: str) -> str:
    ticker = ticker.strip().upper()
    if not _TICKER_RE.fullmatch(ticker):
        raise ValueError("Invalid ticker. Use a simple market ticker such as AAPL or MSFT.")
    return ticker


def build_custom_tools(memory: MemoryStore):
    @tool
    def add_to_watchlist(ticker: str) -> str:
        """Validate and persist a ticker in the analyst watchlist."""
        symbol = _validate_ticker(ticker)
        existing = memory.search("watchlist ticker", k=100)
        if any(f"WATCHLIST:{symbol}" in item for item in existing):
            return f"{symbol} is already on the watchlist."
        memory.add(f"WATCHLIST:{symbol}", {"type": "watchlist", "ticker": symbol})
        memory.save()
        return f"Added {symbol} to the watchlist."

    @tool
    def list_watchlist() -> str:
        """Retrieve all tracked tickers from long-term memory."""
        if memory.vector_store is None:
            return "Watchlist is empty."
        # FAISS does not expose a business-level query API, so inspect stored documents.
        docs = getattr(memory.vector_store.docstore, "_dict", {})
        tickers = sorted({
            doc.page_content.split(":", 1)[1]
            for doc in docs.values()
            if doc.page_content.startswith("WATCHLIST:")
        })
        return ", ".join(tickers) if tickers else "Watchlist is empty."

    @tool
    def calculate_position_size(capital: float, risk_pct: float, entry: float, stop: float) -> str:
        """Calculate position size while rejecting unsafe/invalid inputs."""
        values = {"capital": capital, "risk_pct": risk_pct, "entry": entry, "stop": stop}
        if any(v < 0 for v in values.values()):
            raise ValueError("capital, risk_pct, entry, and stop must not be negative.")
        if capital == 0:
            raise ValueError("capital must be greater than zero.")
        if risk_pct == 0:
            raise ValueError("risk_pct must be greater than zero.")
        if entry <= 0 or stop <= 0:
            raise ValueError("entry and stop prices must be greater than zero.")
        if entry == stop:
            raise ValueError("entry and stop prices must differ.")

        risk_amount = capital * (risk_pct / 100.0)
        per_share_risk = abs(entry - stop)
        shares = int(risk_amount // per_share_risk)
        notional = shares * entry
        return (
            f"Position size: {shares} shares; risk amount: {risk_amount:.2f}; "
            f"risk/share: {per_share_risk:.2f}; estimated notional: {notional:.2f}."
        )

    return [add_to_watchlist, list_watchlist, calculate_position_size]

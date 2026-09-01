from __future__ import annotations

import json
import re

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

from .config import Settings
from .external_tools import get_stock_news, get_stock_price, search_wikipedia
from .memory import MemoryStore
from .models import ResearchSummary
from .prompts import DIRECT_PROMPT, RESEARCH_PROMPT
from .tools import build_custom_tools


class AegisAssistant:
    """Orchestrates prompts, Azure OpenAI, tools, short-term history
    and long-term memory.
    """

    def __init__(self, settings: Settings):
        self.settings = settings

        # Azure OpenAI chat model.
        # Do not pass temperature because some Azure deployments
        # do not support the temperature parameter.
        self.llm = AzureChatOpenAI(
            azure_deployment=settings.azure_chat_deployment,
            azure_endpoint=settings.azure_endpoint,
            api_version=settings.azure_api_version,
            api_key=settings.azure_api_key,
        )

        # Azure OpenAI embeddings for FAISS long-term memory.
        self.embeddings = AzureOpenAIEmbeddings(
            azure_deployment=settings.azure_embedding_deployment,
            azure_endpoint=settings.azure_endpoint,
            api_version=settings.azure_api_version,
            api_key=settings.azure_api_key,
        )

        self.memory = MemoryStore(
            settings.memory_path,
            self.embeddings,
            settings.memory_top_k,
        )

        # Custom tools.
        self.custom_tools = build_custom_tools(self.memory)

        # External tools.
        self.external_tools = [
            search_wikipedia,
            get_stock_news,
            get_stock_price,
        ]

        self.all_tools = self.custom_tools + self.external_tools
        self.tool_map = {tool.name: tool for tool in self.all_tools}

        # Structured output parser.
        self.parser = PydanticOutputParser(
            pydantic_object=ResearchSummary
        )

    # ------------------------------------------------------------------
    # SHORT-TERM MEMORY
    # ------------------------------------------------------------------

    def _history_messages(self):
        """Return current-session conversation history."""
        return self.memory.session_history.messages

    def _remember(self, user_text: str, answer: str) -> None:
        """Store the current interaction in short-term memory."""
        self.memory.session_history.add_message(
            HumanMessage(content=user_text)
        )
        self.memory.session_history.add_message(
            AIMessage(content=answer)
        )

    # ------------------------------------------------------------------
    # LONG-TERM MEMORY
    # ------------------------------------------------------------------

    def save(self) -> None:
        """Persist FAISS long-term memory to disk."""
        self.memory.save()

    def _memory_context(self, query: str) -> str:
        """Retrieve semantically relevant long-term memories."""
        hits = self.memory.search(
            query,
            self.settings.memory_top_k,
        )

        if not hits:
            return "No relevant long-term memory found."

        return "\n".join(f"- {hit}" for hit in hits)

    def add_memory(self, text: str) -> str:
        """Save an analyst fact into persistent memory."""
        self.memory.add(
            text,
            {"type": "analyst_fact"},
        )
        self.memory.save()

        return "Saved to long-term memory."

    # ------------------------------------------------------------------
    # DIRECT LLM RESPONSE
    # ------------------------------------------------------------------

    def _invoke_direct(self, user_text: str) -> str:
        """Generate a normal response using memory and session history."""
        messages = DIRECT_PROMPT.format_messages(
            memory_context=self._memory_context(user_text),
            history=self._history_messages(),
            input=user_text,
        )

        response = self.llm.invoke(messages)

        answer = (
            response.content
            if isinstance(response.content, str)
            else str(response.content)
        )

        self._remember(user_text, answer)

        return answer

    # ------------------------------------------------------------------
    # TICKER EXTRACTION
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_ticker(text: str) -> str | None:
        """Extract a stock ticker from natural-language input."""

        patterns = [
            # Add AAPL to my watchlist
            r"\badd\s+\$?([A-Za-z]{1,5}(?:\.[A-Za-z]{1,2})?)\b",

            # Remove AAPL from my watchlist
            r"\bremove\s+\$?([A-Za-z]{1,5}(?:\.[A-Za-z]{1,2})?)\b",

            # ticker: AAPL
            # ticker = AAPL
            # symbol: AAPL
            r"\b(?:ticker|symbol)\s*[:=]?\s*\$?"
            r"([A-Za-z]{1,5}(?:\.[A-Za-z]{1,2})?)\b",

            # for AAPL
            # of AAPL
            # on AAPL
            r"\b(?:for|of|on)\s+\$?"
            r"([A-Za-z]{1,5}(?:\.[A-Za-z]{1,2})?)\b",

            # $AAPL
            r"\$([A-Za-z]{1,5}(?:\.[A-Za-z]{1,2})?)\b",

            # Research AAPL
            r"\bresearch\s+\$?"
            r"([A-Za-z]{1,5}(?:\.[A-Za-z]{1,2})?)\b",
        ]

        for pattern in patterns:
            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            )

            if match:
                return match.group(1).upper()

        return None

    # ------------------------------------------------------------------
    # TOOL EXECUTION
    # ------------------------------------------------------------------

    def _call_tool(self, name: str, **kwargs) -> str:
        """Call a tool safely and return a readable result."""
        tool = self.tool_map[name]

        try:
            result = tool.invoke(kwargs)
            return str(result)

        except Exception as exc:
            return f"{name} failed safely: {exc}"

    # ------------------------------------------------------------------
    # RESEARCH PIPELINE
    # ------------------------------------------------------------------

    def research(self, ticker: str) -> ResearchSummary | str:
        """Run stock research and return validated structured output."""

        ticker = ticker.strip().upper()

        if not ticker:
            return "Ticker is required for research."

        evidence = []

        tools_to_call = [
            (
                "get_stock_price",
                {"ticker": ticker},
            ),
            (
                "get_stock_news",
                {"ticker": ticker},
            ),
            (
                "search_wikipedia",
                {"topic": ticker},
            ),
        ]

        for name, args in tools_to_call:
            evidence.append(
                f"{name}:\n"
                f"{self._call_tool(name, **args)}"
            )

        research_context = "\n\n".join(evidence)

        format_instructions = self.parser.get_format_instructions()

        last_error = None

        # First attempt + one corrective retry.
        for attempt in range(2):
            prompt = RESEARCH_PROMPT.format_messages(
                memory_context=self._memory_context(ticker),
                history=self._history_messages(),
                ticker=ticker,
                research_context=research_context,
                format_instructions=format_instructions,
            )

            if attempt == 1:
                prompt.append(
                    HumanMessage(
                        content=(
                            "Correct your previous response. "
                            "Output ONLY valid JSON matching the schema. "
                            "Do not add markdown fences or commentary."
                        )
                    )
                )

            try:
                raw = self.llm.invoke(prompt)

                content = (
                    raw.content
                    if isinstance(raw.content, str)
                    else json.dumps(raw.content)
                )

                result = self.parser.parse(content)

                self._remember(
                    f"Research {ticker}",
                    result.model_dump_json(),
                )

                return result

            except Exception as exc:
                last_error = exc

        return (
            "Structured research parsing failed after one "
            f"corrective retry: {last_error}"
        )

    # ------------------------------------------------------------------
    # WATCHLIST HELPERS
    # ------------------------------------------------------------------

    def _is_list_watchlist_request(self, lower: str) -> bool:
        """Recognize natural-language watchlist listing requests."""

        commands = {
            "list watchlist",
            "show watchlist",
            "list my watchlist",
            "show my watchlist",
            "what companies do i track",
            "what stocks do i track",
            "what companies are on my watchlist",
            "what stocks are on my watchlist",
            "my watchlist",
        }

        if lower in commands:
            return True

        if (
            "list" in lower
            and "watchlist" in lower
        ):
            return True

        if (
            "show" in lower
            and "watchlist" in lower
        ):
            return True

        return False

    def _is_add_watchlist_request(self, lower: str) -> bool:
        """Recognize requests to add a ticker."""

        return (
            "add" in lower
            and "watchlist" in lower
        )

    def _is_remove_watchlist_request(self, lower: str) -> bool:
        """Recognize requests to remove a ticker."""

        return (
            "remove" in lower
            and "watchlist" in lower
        )

    # ------------------------------------------------------------------
    # MAIN ROUTER
    # ------------------------------------------------------------------

    def handle(self, user_text: str) -> str:
        """Route free-text user requests to the correct capability."""

        text = user_text.strip()
        lower = text.lower()

        if not text:
            return "Please enter a request."

        # --------------------------------------------------------------
        # Explicit long-term memory action
        # --------------------------------------------------------------

        if lower.startswith("remember that "):
            memory_text = text[len("remember that "):].strip()

            if not memory_text:
                return "Please provide something to remember."

            return self.add_memory(memory_text)

        # --------------------------------------------------------------
        # WATCHLIST: LIST
        # --------------------------------------------------------------

        if self._is_list_watchlist_request(lower):
            answer = self._call_tool(
                "list_watchlist"
            )

            self._remember(text, answer)

            return answer

        # --------------------------------------------------------------
        # WATCHLIST: ADD
        # --------------------------------------------------------------

        if self._is_add_watchlist_request(lower):
            ticker = self._extract_ticker(text)

            if not ticker:
                return (
                    "Please provide a ticker, for example: "
                    "Add AAPL to my watchlist."
                )

            answer = self._call_tool(
                "add_to_watchlist",
                ticker=ticker,
            )

            self._remember(text, answer)

            return answer

        # --------------------------------------------------------------
        # WATCHLIST: REMOVE
        # --------------------------------------------------------------

        if self._is_remove_watchlist_request(lower):
            ticker = self._extract_ticker(text)

            if not ticker:
                return (
                    "Please provide a ticker, for example: "
                    "Remove AAPL from my watchlist."
                )

            # The project currently exposes add/list tools.
            # If remove_to_watchlist exists, use it.
            if "remove_from_watchlist" in self.tool_map:
                answer = self._call_tool(
                    "remove_from_watchlist",
                    ticker=ticker,
                )

                self._remember(text, answer)

                return answer

            return (
                "The remove-watchlist operation is not currently "
                "implemented."
            )

        # --------------------------------------------------------------
        # STRUCTURED RESEARCH
        # --------------------------------------------------------------

        if any(
            word in lower
            for word in [
                "structured summary",
                "research summary",
                "return json",
                "research ",
            ]
        ):
            ticker = self._extract_ticker(text)

            # Last-resort extraction for:
            # Research AAPL
            if not ticker:
                match = re.search(
                    r"\bresearch\s+\$?"
                    r"([A-Za-z]{1,5})\b",
                    text,
                    flags=re.IGNORECASE,
                )

                if match:
                    ticker = match.group(1).upper()

            if ticker:
                result = self.research(ticker)

                if isinstance(result, ResearchSummary):
                    return result.model_dump_json(indent=2)

                return result

        # --------------------------------------------------------------
        # EXTERNAL TOOL: STOCK PRICE
        # --------------------------------------------------------------

        ticker = self._extract_ticker(text)

        if any(
            keyword in lower
            for keyword in [
                "latest price",
                "stock price",
                "closing price",
                "share price",
            ]
        ):
            if not ticker:
                return (
                    "Please provide a ticker, for example: "
                    "What is the latest price of MSFT?"
                )

            answer = self._call_tool(
                "get_stock_price",
                ticker=ticker,
            )

            self._remember(text, answer)

            return answer

        # --------------------------------------------------------------
        # EXTERNAL TOOL: NEWS
        # --------------------------------------------------------------

        if any(
            keyword in lower
            for keyword in [
                "latest news",
                "recent news",
                "headlines",
                "recent headlines",
            ]
        ):
            if not ticker:
                return (
                    "Please provide a ticker, for example: "
                    "Give me the latest news for AAPL."
                )

            answer = self._call_tool(
                "get_stock_news",
                ticker=ticker,
            )

            self._remember(text, answer)

            return answer

        # --------------------------------------------------------------
        # EXTERNAL TOOL: WIKIPEDIA
        # --------------------------------------------------------------

        if (
            "wikipedia" in lower
            or lower.startswith("what is ")
            or "background" in lower
        ):
            topic = text

            answer = self._call_tool(
                "search_wikipedia",
                topic=topic,
            )

            self._remember(text, answer)

            return answer

        # --------------------------------------------------------------
        # POSITION SIZE
        # --------------------------------------------------------------

        if "position size" in lower:
            nums = re.findall(
                r"-?\d+(?:\.\d+)?",
                text,
            )

            if len(nums) >= 4:
                capital, risk_pct, entry, stop = map(
                    float,
                    nums[:4],
                )

                answer = self._call_tool(
                    "calculate_position_size",
                    capital=capital,
                    risk_pct=risk_pct,
                    entry=entry,
                    stop=stop,
                )

                self._remember(text, answer)

                return answer

            return (
                "Provide capital, risk %, entry, and stop. "
                "Example: capital 100000, risk 1%, "
                "entry 200, stop 190."
            )

        # --------------------------------------------------------------
        # DEFAULT DIRECT RESPONSE
        # --------------------------------------------------------------

        return self._invoke_direct(text)

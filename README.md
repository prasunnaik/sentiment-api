from __future__ import annotations

import json
import re

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

from .config import Settings
from .external_tools import (
    get_stock_news,
    get_stock_price,
    search_wikipedia,
)
from .memory import MemoryStore
from .models import ResearchSummary
from .prompts import DIRECT_PROMPT, RESEARCH_PROMPT
from .tools import build_custom_tools


class AegisAssistant:
    """Aegis research assistant.

    Combines:
    - Azure OpenAI
    - short-term conversation memory
    - persistent FAISS long-term memory
    - custom tools
    - external research tools
    - structured Pydantic output
    """

    def __init__(self, settings: Settings):
        self.settings = settings

        # --------------------------------------------------------------
        # Azure OpenAI Chat Model
        # --------------------------------------------------------------
        # Do NOT pass temperature here.
        # Some Azure OpenAI deployments/models reject the parameter.
        self.llm = AzureChatOpenAI(
            azure_deployment=settings.azure_chat_deployment,
            azure_endpoint=settings.azure_endpoint,
            api_version=settings.azure_api_version,
            api_key=settings.azure_api_key,
        )

        # --------------------------------------------------------------
        # Azure OpenAI Embeddings
        # --------------------------------------------------------------
        self.embeddings = AzureOpenAIEmbeddings(
            azure_deployment=settings.azure_embedding_deployment,
            azure_endpoint=settings.azure_endpoint,
            api_version=settings.azure_api_version,
            api_key=settings.azure_api_key,
        )

        # --------------------------------------------------------------
        # Persistent FAISS Memory
        # --------------------------------------------------------------
        self.memory = MemoryStore(
            settings.memory_path,
            self.embeddings,
            settings.memory_top_k,
        )

        # --------------------------------------------------------------
        # Custom Tools
        # --------------------------------------------------------------
        self.custom_tools = build_custom_tools(self.memory)

        # --------------------------------------------------------------
        # External Tools
        # --------------------------------------------------------------
        self.external_tools = [
            search_wikipedia,
            get_stock_news,
            get_stock_price,
        ]

        self.all_tools = (
            self.custom_tools + self.external_tools
        )

        self.tool_map = {
            tool.name: tool
            for tool in self.all_tools
        }

        # --------------------------------------------------------------
        # Structured Output Parser
        # --------------------------------------------------------------
        self.parser = PydanticOutputParser(
            pydantic_object=ResearchSummary
        )

    # ==================================================================
    # SHORT-TERM MEMORY
    # ==================================================================

    def _history_messages(self):
        """Return current-session conversation history."""
        return self.memory.session_history.messages

    def _remember(
        self,
        user_text: str,
        answer: str,
    ) -> None:
        """Store the interaction in short-term memory."""

        self.memory.session_history.add_message(
            HumanMessage(content=user_text)
        )

        self.memory.session_history.add_message(
            AIMessage(content=answer)
        )

    # ==================================================================
    # LONG-TERM MEMORY
    # ==================================================================

    def save(self) -> None:
        """Persist FAISS memory to disk."""
        self.memory.save()

    def _memory_context(
        self,
        query: str,
    ) -> str:
        """Retrieve relevant persistent memories."""

        hits = self.memory.search(
            query,
            self.settings.memory_top_k,
        )

        if not hits:
            return "No relevant long-term memory found."

        return "\n".join(
            f"- {hit}"
            for hit in hits
        )

    def add_memory(
        self,
        text: str,
    ) -> str:
        """Store an analyst fact in long-term memory."""

        if not text.strip():
            return "Please provide something to remember."

        self.memory.add(
            text.strip(),
            {
                "type": "analyst_fact",
            },
        )

        self.memory.save()

        return "Saved to long-term memory."

    # ==================================================================
    # DIRECT LLM RESPONSE
    # ==================================================================

    def _invoke_direct(
        self,
        user_text: str,
    ) -> str:
        """Generate a normal response."""

        messages = DIRECT_PROMPT.format_messages(
            memory_context=self._memory_context(
                user_text
            ),
            history=self._history_messages(),
            input=user_text,
        )

        response = self.llm.invoke(messages)

        answer = (
            response.content
            if isinstance(response.content, str)
            else str(response.content)
        )

        self._remember(
            user_text,
            answer,
        )

        return answer

    # ==================================================================
    # TICKER EXTRACTION
    # ==================================================================

    @staticmethod
    def _extract_ticker(
        text: str,
    ) -> str | None:
        """Extract a stock ticker from natural-language text."""

        patterns = [
            # ----------------------------------------------------------
            # Add AAPL to my watchlist
            # ----------------------------------------------------------
            r"\badd\s+\$?"
            r"([A-Za-z]{1,5}(?:\.[A-Za-z]{1,2})?)\b",

            # ----------------------------------------------------------
            # Remove AAPL from my watchlist
            # ----------------------------------------------------------
            r"\bremove\s+\$?"
            r"([A-Za-z]{1,5}(?:\.[A-Za-z]{1,2})?)\b",

            # ----------------------------------------------------------
            # ticker: AAPL
            # ticker = AAPL
            # symbol: AAPL
            # ----------------------------------------------------------
            r"\b(?:ticker|symbol)"
            r"\s*[:=]?\s*\$?"
            r"([A-Za-z]{1,5}(?:\.[A-Za-z]{1,2})?)\b",

            # ----------------------------------------------------------
            # for AAPL
            # of AAPL
            # on AAPL
            # ----------------------------------------------------------
            r"\b(?:for|of|on)\s+\$?"
            r"([A-Za-z]{1,5}(?:\.[A-Za-z]{1,2})?)\b",

            # ----------------------------------------------------------
            # $AAPL
            # ----------------------------------------------------------
            r"\$([A-Za-z]{1,5}(?:\.[A-Za-z]{1,2})?)\b",

            # ----------------------------------------------------------
            # Research AAPL
            # ----------------------------------------------------------
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

    # ==================================================================
    # TOOL EXECUTION
    # ==================================================================

    def _call_tool(
        self,
        name: str,
        **kwargs,
    ) -> str:
        """Call a registered tool safely."""

        if name not in self.tool_map:
            return f"Tool '{name}' is not available."

        tool = self.tool_map[name]

        try:
            result = tool.invoke(kwargs)
            return str(result)

        except Exception as exc:
            return (
                f"{name} failed safely: {exc}"
            )

    # ==================================================================
    # WATCHLIST
    # ==================================================================

    def _is_list_watchlist_request(
        self,
        lower: str,
    ) -> bool:
        """Detect requests to list the watchlist."""

        exact_commands = {
            "list watchlist",
            "show watchlist",
            "list my watchlist",
            "show my watchlist",
            "my watchlist",
            "what is my watchlist",
            "what's my watchlist",
            "what companies do i track",
            "what stocks do i track",
            "what companies are on my watchlist",
            "what stocks are on my watchlist",
        }

        if lower in exact_commands:
            return True

        if (
            "watchlist" in lower
            and (
                "list" in lower
                or "show" in lower
                or "display" in lower
            )
        ):
            return True

        return False

    def _is_add_watchlist_request(
        self,
        lower: str,
    ) -> bool:
        """Detect requests to add a ticker."""

        return (
            "add" in lower
            and "watchlist" in lower
        )

    def _is_remove_watchlist_request(
        self,
        lower: str,
    ) -> bool:
        """Detect requests to remove a ticker."""

        return (
            "remove" in lower
            and "watchlist" in lower
        )

    # ==================================================================
    # RESEARCH
    # ==================================================================

    def research(
        self,
        ticker: str,
    ) -> ResearchSummary | str:
        """Run research and return validated structured output."""

        ticker = ticker.strip().upper()

        if not ticker:
            return "Ticker is required for research."

        evidence = []

        # --------------------------------------------------------------
        # Stock price
        # --------------------------------------------------------------
        evidence.append(
            "get_stock_price:\n"
            + self._call_tool(
                "get_stock_price",
                ticker=ticker,
            )
        )

        # --------------------------------------------------------------
        # Stock news
        # --------------------------------------------------------------
        evidence.append(
            "get_stock_news:\n"
            + self._call_tool(
                "get_stock_news",
                ticker=ticker,
            )
        )

        # --------------------------------------------------------------
        # Wikipedia
        # --------------------------------------------------------------
        evidence.append(
            "search_wikipedia:\n"
            + self._call_tool(
                "search_wikipedia",
                topic=ticker,
            )
        )

        research_context = "\n\n".join(
            evidence
        )

        format_instructions = (
            self.parser.get_format_instructions()
        )

        last_error = None

        # Requirement:
        # If parsing fails, retry once with corrective prompt.
        for attempt in range(2):

            messages = RESEARCH_PROMPT.format_messages(
                memory_context=self._memory_context(
                    ticker
                ),
                history=self._history_messages(),
                ticker=ticker,
                research_context=research_context,
                format_instructions=format_instructions,
            )

            if attempt == 1:
                messages.append(
                    HumanMessage(
                        content=(
                            "Your previous response could not be "
                            "parsed. Correct it now.\n\n"
                            "Return ONLY valid JSON matching "
                            "the required schema.\n"
                            "Do not use markdown fences.\n"
                            "Do not add explanations."
                        )
                    )
                )

            try:
                response = self.llm.invoke(
                    messages
                )

                content = (
                    response.content
                    if isinstance(
                        response.content,
                        str,
                    )
                    else json.dumps(
                        response.content
                    )
                )

                result = self.parser.parse(
                    content
                )

                self._remember(
                    f"Research {ticker}",
                    result.model_dump_json(),
                )

                return result

            except Exception as exc:
                last_error = exc

        return (
            "Structured research parsing failed "
            "after one corrective retry: "
            f"{last_error}"
        )

    # ==================================================================
    # MAIN ROUTER
    # ==================================================================

    def handle(
        self,
        user_text: str,
    ) -> str:
        """Route free-text input to the appropriate capability."""

        text = user_text.strip()
        lower = text.lower()

        if not text:
            return "Please enter a request."

        # ==============================================================
        # REMEMBER
        # ==============================================================

        if lower.startswith("remember that "):
            memory_text = text[
                len("remember that "):
            ].strip()

            return self.add_memory(
                memory_text
            )

        # ==============================================================
        # WATCHLIST - LIST
        # ==============================================================

        if self._is_list_watchlist_request(
            lower
        ):
            answer = self._call_tool(
                "list_watchlist"
            )

            self._remember(
                text,
                answer,
            )

            return answer

        # ==============================================================
        # WATCHLIST - ADD
        # ==============================================================

        if self._is_add_watchlist_request(
            lower
        ):
            ticker = self._extract_ticker(
                text
            )

            if not ticker:
                return (
                    "Please provide a ticker, "
                    "for example: "
                    "Add AAPL to my watchlist."
                )

            answer = self._call_tool(
                "add_to_watchlist",
                ticker=ticker,
            )

            self._remember(
                text,
                answer,
            )

            return answer

        # ==============================================================
        # WATCHLIST - REMOVE
        # ==============================================================

        if self._is_remove_watchlist_request(
            lower
        ):
            ticker = self._extract_ticker(
                text
            )

            if not ticker:
                return (
                    "Please provide a ticker, "
                    "for example: "
                    "Remove AAPL from my watchlist."
                )

            if (
                "remove_from_watchlist"
                in self.tool_map
            ):
                answer = self._call_tool(
                    "remove_from_watchlist",
                    ticker=ticker,
                )

                self._remember(
                    text,
                    answer,
                )

                return answer

            return (
                "The remove-watchlist operation "
                "is not currently implemented."
            )

        # ==============================================================
        # RESEARCH / STRUCTURED OUTPUT
        # ==============================================================

        is_research_request = any(
            phrase in lower
            for phrase in [
                "research ",
                "research summary",
                "structured summary",
                "return json",
                "analyze stock",
                "analyse stock",
            ]
        )

        if is_research_request:

            ticker = self._extract_ticker(
                text
            )

            # Explicit fallback for:
            # Research AAPL
            if not ticker:
                match = re.search(
                    r"\b(?:research|analyze|analyse)"
                    r"\s+\$?"
                    r"([A-Za-z]{1,5})\b",
                    text,
                    flags=re.IGNORECASE,
                )

                if match:
                    ticker = (
                        match.group(1).upper()
                    )

            if ticker:
                result = self.research(
                    ticker
                )

                if isinstance(
                    result,
                    ResearchSummary,
                ):
                    return result.model_dump_json(
                        indent=2
                    )

                return result

        # ==============================================================
        # STOCK PRICE
        # ==============================================================

        ticker = self._extract_ticker(
            text
        )

        if any(
            phrase in lower
            for phrase in [
                "latest price",
                "stock price",
                "closing price",
                "share price",
                "current price",
            ]
        ):

            if not ticker:
                return (
                    "Please provide a ticker, "
                    "for example: "
                    "What is the latest price of MSFT?"
                )

            answer = self._call_tool(
                "get_stock_price",
                ticker=ticker,
            )

            self._remember(
                text,
                answer,
            )

            return answer

        # ==============================================================
        # STOCK NEWS
        # ==============================================================

        if any(
            phrase in lower
            for phrase in [
                "latest news",
                "recent news",
                "headlines",
                "recent headlines",
                "stock news",
            ]
        ):

            if not ticker:
                return (
                    "Please provide a ticker, "
                    "for example: "
                    "Give me the latest news for AAPL."
                )

            answer = self._call_tool(
                "get_stock_news",
                ticker=ticker,
            )

            self._remember(
                text,
                answer,
            )

            return answer

        # ==============================================================
        # WIKIPEDIA / BACKGROUND
        # ==============================================================

        if (
            "wikipedia" in lower
            or lower.startswith("what is ")
            or "background" in lower
        ):

            answer = self._call_tool(
                "search_wikipedia",
                topic=text,
            )

            self._remember(
                text,
                answer,
            )

            return answer

        # ==============================================================
        # POSITION SIZE
        # ==============================================================

        if "position size" in lower:

            numbers = re.findall(
                r"-?\d+(?:\.\d+)?",
                text,
            )

            if len(numbers) >= 4:

                capital = float(numbers[0])
                risk_pct = float(numbers[1])
                entry = float(numbers[2])
                stop = float(numbers[3])

                answer = self._call_tool(
                    "calculate_position_size",
                    capital=capital,
                    risk_pct=risk_pct,
                    entry=entry,
                    stop=stop,
                )

                self._remember(
                    text,
                    answer,
                )

                return answer

            return (
                "Provide capital, risk %, entry, "
                "and stop. Example: "
                "capital 100000, risk 1%, "
                "entry 200, stop 190."
            )

        # ==============================================================
        # DEFAULT DIRECT RESPONSE
        # ==============================================================

        return self._invoke_direct(
            text
        )

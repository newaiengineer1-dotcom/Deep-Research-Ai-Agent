from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from ddgs import DDGS

class SearchInput(BaseModel):
    query: str = Field(..., description="A focused web search query for the research topic.")

class DuckDuckGoResearchTool(BaseTool):
    name: str = "duckduckgo_web_search"
    description: str = "Search the public web using DuckDuckGo and return titles, snippets, and URLs."
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        try:
            results = DDGS().text(
                query,
                region="us-en",
                safesearch="moderate",
                max_results=6,
            )
            if not results:
                return "No search results were returned."
            output = []
            for i, item in enumerate(results, 1):
                output.append(
                    f"[{i}] {item.get('title', 'Untitled')}\n"
                    f"URL: {item.get('href', '')}\n"
                    f"Snippet: {item.get('body', '')}"
                )
            return "\n\n".join(output)
        except Exception as exc:
            return f"Web search error: {exc}"

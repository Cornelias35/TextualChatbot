from fastapi import FastAPI
from pydantic import BaseModel
from langchain_tavily import TavilySearch
from langchain_core.tools import tool


@tool
def web_search_summary(query: str):
    """
    Performs a web search and returns results. Use this tool to find up-to-date or publicly available information.
    Args:
        request: SearchRequest containing the query string.
    """
    try:
        tool = TavilySearch(max_results=2)
        response = tool.invoke(query)
        results = response.get("results", [])
        if not results:
            return "No results found."
        summary = " ".join([r["content"] for r in results if r.get("content")])
        return summary[:300]  # trim if too long
    except Exception as e:
        return f"Error during web search: {str(e)}"
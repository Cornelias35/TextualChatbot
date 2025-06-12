from fastapi import FastAPI
from pydantic import BaseModel
from langchain_tavily import TavilySearch
from langchain_core.tools import tool


class SearchRequest(BaseModel):
    query: str

@tool
def web_search_summary(request: SearchRequest):
    """
    Performs a web search and returns results. Use this tool to find up-to-date or publicly available information.
    Args:
        request: SearchRequest containing the query string.
    """
    tool = TavilySearch(max_results=2)
    response = tool.invoke(request.query)

    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in response
        ]
    )

    return formatted_search_docs
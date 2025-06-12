# 🔍 Web Search Summary Tool

A lightweight Python tool that performs a live web search using TavilySearch and returns a concise summary of the top results. This tool is designed to be integrated into AI agent frameworks (like LangChain) to provide up-to-date public information in natural language queries.

---

## 📦 Features

- Performs live web searches using [Tavily](https://www.tavily.com/)
- Extracts and summarizes content from the top search results
- Useful for Retrieval-Augmented Generation (RAG) workflows
- Handles errors and missing content gracefully
- Can be integrated as a `@tool` function in agent-based systems (e.g. LangChain, CrewAI, AutoGPT, etc.)

---

## 🧠 Example Use Case

```python
summary = web_search_summary("Who is the president of France?")
print(summary)
```

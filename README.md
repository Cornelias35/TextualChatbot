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

Output
Emmanuel Macron is the President of France. He was elected in 2017 and re-elected in 2022...

🛠️ Installation
Clone the repository:

git clone https://github.com/your-username/web-search-summary-tool.git

Set .env file in root directory. It must contain these keys:

- OPENAI_API_KEY= your_openai_api_key
- LANGSMITH_API_KEY= your_langsmith_key
- TAVILY_API_KEY= your_tavily_api_key

You can either build project by using "docker compose up --build" or "PYTHONPATH=app fastapi dev app/main.py"

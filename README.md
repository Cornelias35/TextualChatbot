# LangGraph RAG & Web Search Chatbot

This project is a **LangGraph-based AI assistant** that uses Retrieval-Augmented Generation (RAG) and web search (via Tavily) to answer questions. The assistant is constrained to only respond using tool outputs, making it deterministic, safe, and grounded.

---

## Features

- **RAG Integration**: Retrieves answers from internal documentation (e.g. LangChain, Python, FastAPI).
- **Web Search Tool**: Uses Tavily API to fetch and summarize up-to-date web content.
- **LangGraph Workflow**: Modular, deterministic flow between system message, tool usage, and final response.
- **Tool-Only Agent**: Model is restricted to tool responses only — no hallucination or fallback to model knowledge.

---

## Project Structure

--- .  
├── app  
│ ├── api_functions  
│ │ ├── **init**.py  
│ │ └── web_search_summary.py  
│ ├── **init**.py  
│ ├── LLM_models.py  
│ ├── LLM_system.py  
│ ├── main.py  
│ └── rag  
│ └── rag_retriever.py  
├── docker-compose.yml  
├── Dockerfile  
├── README.md  
└── requirements.txt

---

## Available Tools

| Tool         | Description                                                              |
| ------------ | ------------------------------------------------------------------------ |
| `rag_data`   | Retrieves relevant internal documentation and summarizes it using RAG.   |
| `web_search` | Uses Tavily API to fetch recent or public information from the internet. |

---

## Example Use Cases

| Query                               | Tool Used    |
| ----------------------------------- | ------------ |
| "What is LangGraph?"                | `rag_data`   |
| "Who is President of United States" | `web_search` |
| "Explain FastAPI routing"           | `rag_data`   |
| "Latest news about AI chips"        | `web_search` |

---

## How to Run

Set .env file in root directory. It must contain these keys:

- OPENAI_API_KEY= your_openai_api_key
- LANGSMITH_API_KEY= your_langsmith_key
- TAVILY_API_KEY= your_tavily_api_key

You can either build project by using "docker compose up --build" or "PYTHONPATH=app fastapi dev app/main.py"

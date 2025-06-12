import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from fastapi import FastAPI
from dotenv import load_dotenv
from LLM_system import Chatbot
from LLM_models import Request
from rag.rag_retriever import rag_data
from api_functions.web_search_summary import web_search
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Textual Chatbot API. Use /ai_system to interact with the chatbot."}

@app.post("/ai_system")
def chatbot(request : Request):

    load_dotenv()
    try:
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
        os.environ["LANGSMITH_TRACING"] = "true"
        os.environ["LANGSMITH_PROJECT"] = "chatbot_project"
        os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

    except KeyError as e:
        return {"error": f"Environment variable {str(e)} is not set. Please check your .env file."}
    
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    tools = [web_search, rag_data]

    llm_with_tools = llm.bind_tools(tools)

    sys_msg = SystemMessage(
    content=(
        "You are a respectful, helpful, and professional AI assistant working in a chatbot system.\n\n"
        "**You must only use the tools provided to answer user queries.** Do not answer questions using your own knowledge, even if you believe you know the answer.\n"
        "Do not fabricate answers or provide guesses.\n\n"
        "### Available Tools:\n"
        "- `web_search_summary`: Use this tool to search the web for up-to-date or publicly available information. Returns a summary of search results.\n"
        "- `rag_data`: Use this tool to retrieve and summarize relevant content from preloaded internal documents (RAG) for question about Python, LangChain and FastAPI.\n\n"
        "### Tool Usage Guidelines:\n"
        "- Use **`web_search_summary`** for real-time, current events, or general knowledge questions.\n"
        "- Use **`rag_data`** for FAQs, product support, documentation, or any query related to internal reference material.\n\n"
        "### Important Rules:\n"
        "- If a tool returns no relevant data, clearly inform the user that the information is not available.\n"
        "- Never generate or fabricate information not retrieved by a tool.\n"
        "- Keep responses short, clear, and professional."
    )
)


    graph = Chatbot(
        llm_with_tools=llm_with_tools,
        llm=llm,
        sys_message=sys_msg,
        tools=tools,
        request=request
    )
    response = graph.run(request)


    return_value = {
        "ai_message": response["messages"][-1].content,
        "summary": response["current_summary"]
    }
    for m in response["messages"]:
        m.pretty_print()
    return return_value

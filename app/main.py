import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from fastapi import FastAPI
from dotenv import load_dotenv
from LLM_system import Chatbot
from LLM_models import Request
from rag.rag_retriever import rag_data
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

    except KeyError as e:
        return {"error": f"Environment variable {str(e)} is not set. Please check your .env file."}
    
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    tools = [rag_data]

    llm_with_tools = llm.bind_tools(tools)

    sys_msg = SystemMessage(
        content=(
            "You are a respectful, helpful, and professional AI assistant working in live customer support in .\n\n"
            "**You must only use the provided tools to answer questions.** Do not answer using your own knowledge, even if you think you know the answer.\n"


            "### Tool Usage Instructions:\n"

            "- Use `search_rag` for all other general or informational questions.\n\n"

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

    return return_value

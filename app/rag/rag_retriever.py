from langchain_community.document_loaders import WebBaseLoader
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool

# Sıkça sorulan sorular rag datası ile değiştirilecektir.
urls = [
    "",
    "",
    "",
]
@tool
def rag_data(rag_query : str):
    """
    Use this function to get FAQ data. It returns related document as string and briefly summarize it to user.
    This is RAG retriever. Make sure you are sending related query as following user needs.
    Args:
        rag_query : str
    """
    docs = [WebBaseLoader(url).load() for url in urls]

    docs_list = [item for sublist in docs for item in sublist]

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=100,
        chunk_overlap = 50
    )

    docs_splits = text_splitter.split_documents(docs_list)

    vectorstore = InMemoryVectorStore.from_documents(
        documents=docs_splits,
        embedding=OpenAIEmbeddings()
    )
    retriever = vectorstore.as_retriever()

    retriever_tool = create_retriever_tool(
        retriever,
        "gamesatis_faq",
        "Search and return information about Gamesatış-frequently asked questions.",
    )

    response = retriever_tool.invoke({"query": f"{rag_query}"})

    return response






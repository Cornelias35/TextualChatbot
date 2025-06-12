from langchain_community.document_loaders import WebBaseLoader
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool

urls = [
    "https://python.langchain.com/docs/introduction/",
    "https://docs.python.org/3/tutorial/index.html",
    "https://fastapi.tiangolo.com/tutorial/",
]
@tool
def rag_data(rag_query : str) -> str:
    """
    RAG retriever to get relevant document content and summarize it.
    Args:
        rag_query: str
    Returns:
        Relevant chunk of text
    """
    all_docs = []
    for url in urls:
        loader = WebBaseLoader(url)
        try:
            docs = loader.load()
            all_docs.extend(docs)
        except Exception as e:
            print(f"Error loading {url}: {e}")

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=100,
        chunk_overlap = 50
    )

    docs_splits = text_splitter.split_documents(all_docs)

    vectorstore = InMemoryVectorStore.from_documents(
        documents=docs_splits,
        embedding=OpenAIEmbeddings()
    )
    retriever = vectorstore.as_retriever()

    result_docs = retriever.invoke(rag_query)

    response_text = "\n---\n".join([doc.page_content for doc in result_docs[:2]])

    return f"Top matching content:\n{response_text}"






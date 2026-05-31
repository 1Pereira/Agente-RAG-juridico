from typing import List
from typing_extensions import TypedDict
from langchain_core.documents import Document

# define a "memoria" de curto prazo que viajará entre os nós do grafo
class AgentState(TypedDict):
    question: str
    documents: List[Document]
    relevant_documents: List[Document]
    answer: str
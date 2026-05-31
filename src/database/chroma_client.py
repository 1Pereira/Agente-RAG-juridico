import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def obter_banco_vetorial():
    """Inicializa e retorna a ligação com o ChromaDB"""
    
    # instancia de modelo de embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # pasta 'chroma_db' no diretório raiz do projeto
    diretorio_db = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../chroma_db"))
    
    return Chroma(
        persist_directory=diretorio_db,
        embedding_function=embeddings,
    )
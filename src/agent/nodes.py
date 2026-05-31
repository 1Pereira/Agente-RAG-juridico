import os
import sys
import logging
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# carregar variáveis de ambiente
load_dotenv()

# ponte para acessar o banco de dados na pasta vizinha
caminho_database = os.path.abspath(os.path.join(os.path.dirname(__file__), "../database"))
sys.path.append(caminho_database)
from chroma_client import obter_banco_vetorial

from state import AgentState

# estrutura para forçar o LLM a retornar um JSON escrito 
class GraderOutput(BaseModel):
    is_relevant: str = Field(description="O documento é relevante para a pergunta? Responda 'sim' ou 'nao'")
    
def retrieve(state: AgentState):
    """Nó 1: Busca documentos no banco vetorial usando Filtro Híbrido."""
    logging.info("Nó 1: Buscando documentos relevantes...")
    question = state["question"]
    
    vector_store = obter_banco_vetorial() # conectar com o banco
    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 3,
            "filter": {"status": "ativo"}
        }
    )
    docs = retriever.invoke(question)
    
    return {"documents": docs}

def grade_documents(state: AgentState):
    """Nó 2: Filtra os framgmentos, removendo os irrelevantes"""
    logging.info("Nó 2: Avaliando a qualidade do contexto recuperado...")
    question = state["question"]
    documents = state["documents"]
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    structured_llm = llm.with_structured_output(GraderOutput)
    
    system_prompt = """Você é um auditor jurídico estrito. Avalie se o documento contém informações relevantes para responder à pergunta.
    Se contiver as palavras-chave ou o conceito semântico, responda 'sim'. Caso contrário, responda 'nao'."""
    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "Documento: {context}\n\nPergunta: {question}")])
    grader_chain = prompt | structured_llm
    
    relevant_docs = []
    for odc in documents:
        score = grader_chain.invoke({"context": odc.page_content, "question": question})
        if score.is_relevant.lower() == "sim":
            relevant_docs.append(odc)
    
    logging.info(f"   -> {len(relevant_docs)} de {len(documents)} documentos passaram pelo crivo.")
    return {"relevant_documents": relevant_docs}

def generate(state: AgentState):
    """Nó 3: Gera a resposta final usando apenas os documentos aprovados."""
    logging.info("Nó 3: Gerando resposta baseada em fatos...")
    question = state["question"]
    documents = state.get("relevant_documents", [])
    
    # se todos os documentos forem reprovados
    if not documents:
        return {"answer": "A informação não consta no documento."}
    
    context = "\n\n".join(doc.page_content for doc in documents) # transformar a lista de fragmentos num texto corrido para a LLM ler
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    template = """Você é um assistente jurídico sênior. Responda estritamente com base no contexto abaixo.
    Contexto: {context}
    
    Pergunta: {question}
    Resposta:"""
    
    chain = ChatPromptTemplate.from_template(template) | llm
    res = chain.invoke({"context": context, "question": question})
    
    return {"answer": res.content}
    
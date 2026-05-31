import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

import sys
caminho_database = os.path.abspath(os.path.join(os.path.dirname(__file__), "../database"))
sys.path.append(caminho_database)
from chroma_client import obter_banco_vetorial

load_dotenv()

def configurar_chain_rag():
    
    vector_store = obter_banco_vetorial() # conectar com o banco
    
    retriever = vector_store.as_retriever(search_kwargs={"k": 3}) # configurar o retriever para buscar os 3 documentos mais relevantes
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0) # configurar o modelo de linguagem
    
    template = """Você é um assistente jurídico sênior e direto.
    Use APENAS o contexto abaixo para responder à pergunta. Não use conhecimento externo.
    Se a resposta não estiver no contexto, diga "A informação não consta no documento."
    Sempre que possível, cite a "Cláusula" ou o "Parágrafo" que embasou sua resposta.
    
    Contexto do Documento:
    {context}
    
    Pergunta do Usuário: {question}
    
    Resposta Jurídica:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    def formatar_documentos(docs):
        
        return "\n\n".join(doc.page_content for doc in docs) # transformar a lista de fragmentos num texto corrido para a LLM ler
    
    rag_chain = (
        {"context": retriever | formatar_documentos, "question": RunnablePassthrough()} 
        | prompt 
        | llm 
        | StrOutputParser()
    )
    
    return rag_chain

if __name__ == "__main__":
    print("Iniciando o RAG Chain...")
    sistema_rag = configurar_chain_rag()
    
    while True:
        pergunta_usuario = input("\nFaça uma pergunta sobre o contrato (ou digite 'sair): ")
        
        if pergunta_usuario.lower() == "sair":
            print("Encerrando o sistema. Até mais!")
            break
        
        print("\nAnalisando base de dados...\n")
        resposta = sistema_rag.invoke(pergunta_usuario)
        print("RESPOSTA:")
        print(resposta)
        print("-" * 50)
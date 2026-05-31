import os
import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chroma_client import obter_banco_vetorial

def processar_lote_contratos():
    pasta_dados = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../dados"))
    arquivos_pdf = glob.glob(f"{pasta_dados}/*.pdf")
    
    if not arquivos_pdf:
        print("Nenhum PDF encontrado na pasta 'dados'.")
        return

    print(f"Iniciando processamento em lote de {len(arquivos_pdf)} arquivo(s)...")
    
    documentos_totais = []
    
    for caminho_pdf in arquivos_pdf:
        nome_arquivo = os.path.basename(caminho_pdf)
        print(f"Lendo: {nome_arquivo}...")
        
        loader = PyPDFLoader(caminho_pdf)
        docs = loader.load()
        
        for doc in docs:
            doc.metadata["arquivo_origem"] = nome_arquivo
            doc.metadata["tipo_documento"] = "prestacao_servicos" if "prestacao" in nome_arquivo.lower() else "geral"
            doc.metadata["status"] = "ativo" # Simulando que todos que estão na pasta são vigentes
            
        documentos_totais.extend(docs)
        
    print(f"Extraídas {len(documentos_totais)} páginas no total. A fragmentar...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    fragmentos = text_splitter.split_documents(documentos_totais)
    print(f"Gerados {len(fragmentos)} fragmentos indexáveis.")
    
    print("A gerar embeddings e a guardar no ChromaDB...")
    vector_store = obter_banco_vetorial()
    vector_store.add_documents(fragmentos)
    
    print("Pipeline de Ingestão concluído com sucesso!")

if __name__ == "__main__":
    processar_lote_contratos()
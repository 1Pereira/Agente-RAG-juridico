import os
import sys
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# configuração do log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

caminho_agente = os.path.abspath(os.path.join(os.path.dirname(__file__), "agent"))
sys.path.append(caminho_agente)

from graph import app_agente

app = FastAPI(
    title="API do Agente RAG Jurídico",
    description="Motor de análise autónoma de contratos com LangGraph",
    version="1.0.0"
)

class PerguntaRequest(BaseModel):
    pergunta: str

@app.post("/perguntar")
async def fazer_pergunta(request: PerguntaRequest):
    logger.info(f"Nova requisição recebida: '{request.pergunta}'")
    
    try:
        logger.info("Iniciando a execução do LangGraph...")
        resultado = app_agente.invoke({"question": request.pergunta})
        
        logger.info("Resposta gerada com sucesso.")
        return {
            "pergunta": request.pergunta,
            "resposta": resultado["answer"]
        }
    except Exception as e:
        logger.error(f"Falha crítica ao processar o LangGraph: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="O serviço de IA está temporariamente indisponível. Tente novamente em breve."
        )

if __name__ == "__main__":
    logger.info("🚀 Iniciando o servidor da API na porta 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi.testclient import TestClient
import sys
import os

# Adiciona o caminho da raiz do projeto para importar o app do main.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.main import app

# simula um navegador ou um Postman
client = TestClient(app)

def test_rota_perguntar_deve_retornar_200():
    """Testa se a API responde corretamente a uma pergunta válida."""
    
    response = client.post(
        "/perguntar",
        json={"pergunta": "Qual a porcentagem da multa de rescisão?"}
    )
    
    # garantias básicas para validar a resposta
    assert response.status_code == 200 # garante que não deu erro 500
    dados = response.json()
    assert "pergunta" in dados # garante que a chave pergunta voltou no JSON
    assert "resposta" in dados # garante que a chave resposta voltou no JSON
    assert type(dados["resposta"]) == str
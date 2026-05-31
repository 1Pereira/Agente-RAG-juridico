# API de Agente RAG Jurídico
 
> Agente de IA autônomo para análise de contratos jurídicos com arquitetura baseada em grafos de estado.
 
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-LangChain-1C3C3C?style=flat-square)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vetorial-orange?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-Google_AI-4285F4?style=flat-square&logo=google&logoColor=white)
 
---
## Descrição do Projeto

Este projeto implementa uma API RESTful corporativa que atua como um Agente de Inteligência Artificial especializado na análise de contratos jurídicos.

Diferente de pipelines RAG (Retrieval-Augmented Generation) lineares tradicionais, este sistema utiliza uma arquitetura baseada em Grafos de Estado (LangGraph) para conceder autonomia lógica ao LLM. O agente atua como um auditor rigoroso, avaliando a relevância dos documentos recuperados antes de gerar a resposta, bloqueando ativamente alucinações caso a informação solicitada não conste na base de dados.

O sistema possui um pipeline de ingestão em lote com processamento de metadados, permitindo buscas híbridas (vetorial + filtros SQL-like), e está totalmente conteinerizado para deploy em ambientes de produção.

---

# Arquitetura e Tecnologias Utilizadas

* **Linguagem Principal:** Python 3.11+
* **Framework de API:** FastAPI e Uvicorn
* **Orquestração de Agentes:** LangChain e LangGraph
* **Banco de Dados Vetorial:** ChromaDB (Local)

## Modelos de IA

* **Embeddings:** HuggingFace (Open-source)
* **LLM:** Google Gemini 2.5 Flash

## Infraestrutura

* Docker

## Qualidade e Testes

* Pytest
* Logging nativo do Python

---

# Estrutura do Projeto

```plaintext
.
├── chroma_db/               # Banco de dados vetorial persistente (gerado automaticamente)
├── dados/                   # Diretório fonte para os arquivos PDF em formato bruto
├── src/                     # Código fonte principal
│   ├── agent/               # Lógica do Agente Autônomo
│   │   ├── graph.py         # Definição do fluxo LangGraph (Roteamento)
│   │   ├── nodes.py         # Funções de execução (Recuperação, Avaliação, Geração)
│   │   └── state.py         # Definição do estado global do agente
│   ├── database/            # Pipeline de Dados e Persistência
│   │   ├── chroma_client.py # Conexão e configuração do banco vetorial
│   │   └── ingestion.py     # Script de processamento em lote e extração de metadados
│   └── main.py              # Ponto de entrada da API e configuração de rotas
├── tests/                   # Suite de testes automatizados
│   ├── __init__.py
│   └── test_api.py          # Testes de integração da rota principal
├── .env                     # Variáveis de ambiente (não versionado)
├── .dockerignore            # Regras de exclusão para o build da imagem Docker
├── Dockerfile               # Receita de infraestrutura para conteinerização
└── requirements.txt         # Dependências do projeto
```

---

# Fluxo Lógico do Agente (LangGraph)

O processamento cognitivo da API segue três etapas rigorosas de avaliação:

## 1. Nó de Recuperação (Retrieve)

Realiza uma busca híbrida no ChromaDB, cruzando:

* Similaridade vetorial da pergunta
* Metadados extraídos no pipeline de ingestão

Exemplos de metadados:

* Status do contrato
* Tipo de documento
* Categoria jurídica

---

## 2. Nó de Avaliação (Grade Documents)

O LLM atua como um juiz interno.

Ele recebe os fragmentos recuperados e avalia, de forma binária (`sim/não`), se os textos contêm informações suficientes para responder à pergunta.

* Fragmentos úteis → aprovados
* Fragmentos irrelevantes → descartados

---

## 3. Nó de Geração (Generate)

Recebe apenas o contexto aprovado pela etapa anterior.

### Cenários possíveis

#### Caso exista contexto válido:

O agente formula a resposta jurídica estruturada.

#### Caso o contexto esteja vazio:

A trava de segurança é acionada e o sistema retorna que a informação não consta na base de dados.

---

# Como Executar Localmente (Ambiente de Desenvolvimento)

## 1. Pré-requisitos

* Python 3.11 ou superior
* Conta no Google AI Studio para geração da API Key

---

## 2. Instalação e Configuração

Clone o repositório:

```bash
git clone https://github.com/1Pereira/Agente-RAG-juridico.git
cd Agente-RAG-juridico
```

Crie e ative um ambiente virtual:

### Windows

```bash
python -m venv venv
source venv/Scripts/activate
```

### Linux/macOS

```bash
python -m venv venv
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY=sua_chave_aqui
```

---

# 3. Ingestão de Dados

Adicione os arquivos `.pdf` dentro da pasta `dados/`.

Depois execute o pipeline de ingestão:

```bash
cd src/database
python ingestion.py
```

O script irá:

* Processar os PDFs
* Extrair metadados
* Gerar embeddings
* Popular o ChromaDB

---

# 4. Iniciando a API

Volte para a raiz do projeto:

```bash
cd ../..
python src/main.py
```

A API ficará disponível em:

```plaintext
http://localhost:8000
```

---

# Como Executar via Docker (Ambiente de Produção)

O projeto possui um `Dockerfile` configurado para garantir execução isolada e reproduzível.

## Construindo a imagem

```bash
docker build -t agente-rag-api .
```

## Executando o container

```bash
docker run -p 8000:8000 --env-file .env agente-rag-api
```

---

# Referência da API

## Endpoint Principal

### `POST /perguntar`

---

## Corpo da Requisição

```json
{
  "pergunta": "Qual a porcentagem da multa de rescisão?"
}
```

---

## Exemplo de Resposta

```json
{
  "pergunta": "Qual a porcentagem da multa de rescisão?",
  "resposta": "A multa de rescisão descrita no contrato de prestação de serviços é de 5% sobre o valor total remanescente."
}
```

---

# Swagger UI

A documentação interativa pode ser acessada em:

```plaintext
http://localhost:8000/docs
```

---

# Suite de Testes

O projeto utiliza `pytest` para validação das rotas e comportamento da API.

Os testes simulam:

* Requisições HTTP completas
* Validação do JSON de saída
* Tempo de resposta
* Integridade das chaves retornadas

## Executando os testes

```bash
pytest -q --disable-warnings
```

---

# Monitoramento e Logs

A aplicação possui um sistema de logging nativo configurado.

Os seguintes eventos são registrados:

* Requisições recebidas
* Transições entre nós do LangGraph
* Erros críticos de infraestrutura
* Exceções tratadas via `try/except`

## Saídas de log

* Console em tempo real
* Arquivo persistente:

```plaintext
app.log
```

Isso permite rastreabilidade, auditoria e monitoramento operacional do agente.

---

# Características Técnicas do Projeto

* Arquitetura baseada em agentes autônomos
* Proteção contra alucinações do LLM
* Busca híbrida vetorial + metadados
* Pipeline de ingestão automatizado
* Persistência vetorial local
* API RESTful corporativa
* Conteinerização com Docker
* Estrutura modular e escalável
* Logging e observabilidade
* Testes automatizados

---
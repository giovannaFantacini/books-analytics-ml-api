# 📚 Books Analytics & ML API  
**Tech Challenge – Pós Tech | Machine Learning Engineering (Fase 1)**

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Objetivos do Projeto](#-objetivos-do-projeto)
- [Fonte de Dados](#-fonte-de-dados)
- [Arquitetura](#-arquitetura)
- [Pipeline de Dados](#-pipeline-de-dados)
- [Modelo de Machine Learning](#-modelo-de-machine-learning)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Tecnologias Utilizadas](#️-tecnologias-utilizadas)
- [Instalação e Execução](#-instalação-e-execução)
- [Autenticação JWT](#-autenticação-jwt)
- [Endpoints da API](#-endpoints-da-api)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Deploy](#-deploy)
- [Vídeo de Apresentação](#-vídeo-de-apresentação)
- [Referências](#-referências)

---

## 📌 Visão Geral

Este projeto implementa uma **API pública RESTful** para coleta, processamento, análise e disponibilização de dados de livros, utilizando como fonte o site **[Books to Scrape](https://books.toscrape.com/)**.

A solução foi desenvolvida como parte do **Tech Challenge da Pós Tech em Machine Learning Engineering (Fase 1)**, contemplando um **pipeline completo de dados**, desde **web scraping**, armazenamento estruturado, **análises estatísticas**, até **preparação e consumo de dados para Machine Learning**, incluindo **predição de avaliação de livros**.

A API foi construída com **FastAPI**, seguindo boas práticas de organização, escalabilidade e documentação automática (Swagger/OpenAPI).

---

## 🎯 Objetivos do Projeto

### Requisitos Obrigatórios Atendidos

| # | Requisito | Status |
|---|-----------|--------|
| 1 | Construir um **pipeline de dados end-to-end** | ✅ |
| 2 | Extrair dados via **web scraping** de fonte pública | ✅ |
| 3 | Disponibilizar os dados por meio de uma **API pública** | ✅ |
| 4 | Criar **endpoints analíticos** (insights e estatísticas) | ✅ |
| 5 | Preparar a base para **consumo por modelos de Machine Learning** | ✅ |
| 6 | Implementar **autenticação JWT** para rotas sensíveis | ✅ |
| 7 | Realizar **deploy** da API em ambiente de produção | ✅ |
| 8 | Documentação completa no **README** | ✅ |
| 9 | **Vídeo de apresentação** demonstrando a solução | ✅ |

---

## 📊 Fonte de Dados

**Site:** [Books to Scrape](https://books.toscrape.com/)

O Books to Scrape é um site de demonstração criado especificamente para práticas de web scraping. Ele simula uma livraria online com aproximadamente **500 livros** distribuídos em **50 categorias**.

### Dados Extraídos

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `Título` | Nome do livro | "A Light in the Attic" |
| `Preço` | Preço em libras (£) | 51.77 |
| `Avaliação` | Rating de 1 a 5 estrelas | "Three" (3) |
| `Disponibilidade` | Status de estoque | "In stock" |
| `Categoria` | Gênero/categoria do livro | "Poetry" |
| `Imagem` | URL da capa do livro | https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg |

---

## 🧱 Arquitetura

![Diagrama de Arquitetura](docs/images/DiagramaProjeto.png)

---

## 🔄 Pipeline de Dados

![Pipeline de Dados](docs/images/PipelineDados.png)

### Etapas do Pipeline

| Etapa | Descrição | Arquivo/Módulo |
|-------|-----------|----------------|
| **1. Extração** | Web scraping do site Books to Scrape | `src/scraping/scraping.py` |
| **2. Armazenamento** | Dados salvos em CSV estruturado | `data/books.csv` |
| **3. Transformação** | Limpeza e padronização dos dados | `src/features/extract_features.py` |
| **4. Feature Engineering** | Extração de features para ML | `src/features/extract_features.py` |
| **5. Treinamento** | Modelo Random Forest para classificação | `src/training/train_model.py` |
| **6. Disponibilização** | API REST com FastAPI | `src/book_api/api/main.py` |

---

## 🤖 Modelo de Machine Learning

### Objetivo
Predizer a **avaliação (rating)** de um livro com base em suas características.

### Algoritmo
**Random Forest Classifier** (Scikit-learn)

### Features Utilizadas

| Feature | Tipo | Descrição |
|---------|------|-----------|
| `Preço` | Numérica | Preço do livro (£) |
| `Disponibilidade` | Binária | 1 = Em estoque, 0 = Fora de estoque |
| `Categoria` | Categórica | Gênero/categoria do livro |

### Target
`Avaliação` - Classificação de 1 a 5 estrelas (One, Two, Three, Four, Five)

### Pipeline de Preprocessamento

```python
# Transformações aplicadas:
1. StandardScaler - Normalização das features numéricas (Preço, Disponibilidade)
2. OneHotEncoder - Codificação das features categóricas (Categoria)
3. RandomForestClassifier - Modelo de classificação (100 estimadores)
```

### Métricas do Modelo

| Métrica | Valor |
|---------|-------|
| Acurácia | ~20% |
| Split de Treino/Teste | 80/20 |

### ⚠️ Limitações do Modelo

> **Importante:** O modelo apresenta acurácia baixa (~20%) devido às características dos dados utilizados:
>
> 1. **Dados sintéticos/aleatórios:** O site Books to Scrape é um ambiente de demonstração onde os preços, avaliações e categorias foram gerados de forma **aleatória**, sem relação real entre as variáveis.
>
> 2. **Ausência de padrões:** Não existe correlação significativa entre as features (preço, categoria, disponibilidade) e o target (avaliação), tornando impossível para qualquer modelo de ML aprender padrões preditivos.
>
> 3. **Volume limitado de dados:** Com apenas ~500 livros distribuídos em 50 categorias, há poucos exemplos por categoria para o modelo generalizar.
>
> **Em um cenário real**, com dados de uma livraria verdadeira onde existem padrões reais (ex: livros de categorias específicas tendem a ter faixas de preço definidas, avaliações refletem qualidade percebida), o modelo teria performance significativamente melhor.

> **Nota:** Execute `python -m src.training.train_model` para retreinar o modelo e atualizar as métricas.

---

## 📁 Estrutura do Projeto

```bash
books-analytics-ml-api/
│
├── 📂 data/
│   └── books.csv                    # Dataset com livros extraídos via scraping
│
├── 📂 docs/
│   └── images/                      # Imagens e diagramas da documentação
│       └── DiagramaProjeto.png
│       └── PipelineDados.png
│
├── 📂 models/
│   └── modelo_avaliacao_books.joblib  # Modelo de ML treinado (Random Forest)
│
├── 📂 src/
│   ├── __init__.py
│   ├── index.py
│   │
│   ├── 📂 auth/
│   │   ├── __init__.py
│   │   └── authentication.py        # Lógica de autenticação JWT
│   │
│   ├── 📂 scraping/
│   │   └── scraping.py              # Web scraping do Books to Scrape
│   │
│   ├── 📂 book_api/
│   │   └── 📂 api/
│   │       ├── __init__.py
│   │       ├── main.py              # Aplicação FastAPI principal
│   │       ├── deps.py              # Dependências e helpers
│   │       ├── 📂 core/
│   │       │   └── settings.py      # Configurações da aplicação
│   │       └── 📂 routers/
│   │           ├── auth.py          # Rotas de autenticação
│   │           ├── books.py         # Rotas de livros (CRUD)
│   │           ├── categories.py    # Rotas de categorias
│   │           ├── health.py        # Health check
│   │           ├── ml.py            # Rotas de Machine Learning
│   │           ├── scraping.py      # Rota para trigger do scraping
│   │           └── stats.py         # Rotas de estatísticas
│   │
│   ├── 📂 features/
│   │   ├── __init__.py
│   │   └── extract_features.py      # Extração de features para ML
│   │
│   ├── 📂 schema/
│   │   └── PredictRequest.py        # Schema Pydantic para predição
│   │
│   ├── 📂 scripts/
│   │   ├── __init__.py
│   │   └── data_analysis.py         # Scripts de análise exploratória
│   │
│   └── 📂 training/
│       ├── __init__.py
│       └── train_model.py           # Treinamento do modelo de ML
│
├── .env.example                      # Exemplo de variáveis de ambiente
├── requirements.txt                  # Dependências Python
└── README.md                        # Esta documentação
```


## ⚙️ Tecnologias Utilizadas

### Backend & API
| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| Python | 3.10+ | Linguagem principal |
| FastAPI | 0.124+ | Framework para construção da API REST |
| Uvicorn | - | Servidor ASGI para rodar a aplicação |
| Pydantic | 2.12+ | Validação de dados e schemas |

### Data Processing & Machine Learning
| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| Pandas | 2.3+ | Manipulação e análise de dados |
| NumPy | 2.3+ | Computação numérica |
| Scikit-learn | - | Algoritmos de Machine Learning |
| Joblib | 1.5+ | Serialização do modelo treinado |

### Web Scraping
| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| BeautifulSoup4 | 4.14+ | Parsing de HTML |
| Requests | - | Requisições HTTP |

### Autenticação & Segurança
| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| python-jose | - | Geração e validação de tokens JWT |
| Passlib | 1.7+ | Hashing de senhas (bcrypt) |

### Documentação
| Tecnologia | Descrição |
|------------|-----------|
| Swagger UI | Documentação interativa automática |
| ReDoc | Documentação alternativa |
| OpenAPI | Especificação da API |

---

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Git

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/seu-usuario/books-analytics-ml-api.git
cd books-analytics-ml-api
```

### 2️⃣ Criar ambiente virtual
```bash
# Linux / Mac
python -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Windows (CMD)
python -m venv .venv
.venv\Scripts\activate.bat
```

### 3️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Executar o Web Scraping (opcional - dados já incluídos)
```bash
python -c "from src.scraping.scraping import scrape_books; scrape_books()"
```

### 6️⃣ Treinar o modelo de ML (opcional - modelo já incluído)
```bash
python -m src.training.train_model
```

### 7️⃣ Executar a API localmente
```bash
uvicorn src.book_api.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 📍 URLs Disponíveis (Local)

| Recurso | URL |
|---------|-----|
| 📘 **Swagger UI** (Documentação Interativa) | http://localhost:8000/docs |
| 📕 **ReDoc** (Documentação Alternativa) | http://localhost:8000/redoc |
| 🔗 **OpenAPI JSON** | http://localhost:8000/openapi.json |
| ❤️ **Health Check** | http://localhost:8000/api/v1/health |

---


## 🔐 Autenticação (JWT)

A API utiliza **JSON Web Tokens (JWT)** para autenticação. Algumas rotas são públicas, enquanto outras requerem token válido.

### Fluxo de Autenticação

```
1. POST /api/v1/auth/login → Recebe access_token + refresh_token
2. Usar access_token no header Authorization
3. Quando expirar, usar refresh_token para renovar
```

### Endpoint de Login

**POST** `/api/v1/auth/login`

**Request** (x-www-form-urlencoded):
```
username=admin
password=admin123
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Usando o Token

Adicione o header em todas as requisições protegidas:
```bash
Authorization: Bearer <access_token>
```

**Exemplo com cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/scraping/trigger" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Configuração dos Tokens

| Parâmetro | Valor Padrão |
|-----------|--------------|
| Access Token Expiration | 30 minutos |
| Refresh Token Expiration | 24 horas (1440 min) |
| Algoritmo | HS256 |

---

## 📚 Endpoints da API

### Resumo dos Endpoints

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/api/v1/auth/login` | Autenticação e obtenção de tokens | ❌ |
| POST | `/api/v1/auth/refresh` | Renovar access token | 🔄 |
| GET | `/api/v1/books` | Listar todos os livros | ❌ |
| GET | `/api/v1/books/{id}` | Detalhes de um livro | ❌ |
| GET | `/api/v1/books/search` | Buscar livros | ❌ |
| GET | `/api/v1/books/top-rated` | Livros melhor avaliados | ❌ |
| GET | `/api/v1/books/price-range` | Filtrar por preço | ❌ |
| GET | `/api/v1/categories` | Listar categorias | ❌ |
| GET | `/api/v1/health` | Status da API | ❌ |
| GET | `/api/v1/stats/overview` | Estatísticas gerais | ❌ |
| GET | `/api/v1/stats/categories/{category}` | Stats por categoria | ❌ |
| POST | `/api/v1/scraping/trigger` | Executar scraping | 🔐 |
| GET | `/api/v1/ml/features` | Features para ML | ❌ |
| GET | `/api/v1/ml/training-data` | Dados de treino/teste | ❌ |
| POST | `/api/v1/ml/predict` | Predição de avaliação | ❌ |

> **Legenda:** ❌ = Não requer auth | 🔐 = Requer JWT | 🔄 = Requer refresh token

---

### 📘 Books

#### Listar todos os livros
```http
GET /api/v1/books
```
**Response:** Lista com todos os livros disponíveis.

#### Detalhes de um livro
```http
GET /api/v1/books/{id}
```
**Parâmetros:** `id` (int) - Índice do livro

#### Buscar livros
```http
GET /api/v1/books/search?title={titulo}&category={categoria}
```
**Query params:**
- `title` (opcional): Filtro por título
- `category` (opcional): Filtro por categoria

#### Livros mais bem avaliados
```http
GET /api/v1/books/top-rated
```
**Response:** Lista dos livros com avaliação 4-5 estrelas.

#### Filtrar por faixa de preço
```http
GET /api/v1/books/price-range?min={min}&max={max}
```
**Query params:**
- `min`: Preço mínimo (£)
- `max`: Preço máximo (£)

---

### 🗂 Categories

#### Listar todas as categorias
```http
GET /api/v1/categories
```
**Response:** Lista de todas as categorias disponíveis (50 categorias).

---

### ❤️ Health

#### Verificar status da API
```http
GET /api/v1/health
```
**Response:**
```json
{
  "status": "healthy",
  "books_loaded": 517
}
```

---

### 📊 Stats & Insights

#### Estatísticas gerais
```http
GET /api/v1/stats/overview
```
**Response:** Quantidade de livros, preço médio, distribuição de avaliações, etc.

#### Estatísticas por categoria
```http
GET /api/v1/stats/categories/{category}
```
**Parâmetros:** `category` (string) - Nome da categoria

---

### 🕷 Scraping (Admin)

#### Executar web scraping
```http
POST /api/v1/scraping/trigger
Authorization: Bearer <access_token>
```
**Response:**
```json
{
  "message": "Scraping concluído e dados salvos em 'data/books.csv'"
}
```
> ⚠️ **Endpoint protegido:** Requer autenticação JWT com role `admin`.

---

### 🤖 Machine Learning

#### Obter features para ML
```http
GET /api/v1/ml/features
```
**Response:** Dados formatados para uso como features em modelos de ML.

#### Obter dados de treino/teste
```http
GET /api/v1/ml/training-data
```
**Response:**
```json
{
  "train": [...],  // 80% dos dados
  "test": [...]    // 20% dos dados
}
```

#### Predição de avaliação
```http
POST /api/v1/ml/predict
Content-Type: application/json

{
  "preco": 25.99,
  "disponibilidade": 1,
  "categoria": "Science"
}
```
**Response:**
```json
{
  "predicted_rating": "Three"
}
```

---

## 💡 Exemplos de Uso

### Exemplo 1: Buscar livros de uma categoria

```bash
# Buscar livros da categoria "Science Fiction"
curl -X GET "http://localhost:8000/api/v1/books/search?category=Science%20Fiction"
```

### Exemplo 2: Obter estatísticas gerais

```bash
curl -X GET "http://localhost:8000/api/v1/stats/overview"
```

### Exemplo 3: Fluxo completo com autenticação (Scraping)

```bash
# 1. Fazer login
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" | jq -r '.access_token')

# 2. Executar scraping (rota protegida)
curl -X POST "http://localhost:8000/api/v1/scraping/trigger" \
  -H "Authorization: Bearer $TOKEN"
```

### Exemplo 4: Predição de avaliação 

```bash
curl -X POST "http://localhost:8000/api/v1/ml/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "preco": 35.50,
    "disponibilidade": 1,
    "categoria": "Mystery"
  }'
```
---

## 🌐 Deploy

### Ambiente de Produção

A API está hospedada no **Render** (PaaS gratuito para projetos Python).

🔗 **Link da API em produção:**  
https://books-analytics-ml-api.onrender.com/docs

### URLs de Produção

| Recurso | URL |
|---------|-----|
| 📘 Swagger UI | https://books-analytics-ml-api.onrender.com/docs |
| 📕 ReDoc | https://books-analytics-ml-api.onrender.com/redoc |
| ❤️ Health Check | https://books-analytics-ml-api.onrender.com/api/v1/health |

---

## 🎥 Vídeo de Apresentação

🎬 **Link do vídeo de demonstração:**  
![Video Demonstração](https://drive.google.com/file/d/167Vd0sjpq6HpIP1WafptSH50XMkKNEXE/view?usp=sharing)

---

## 📖 Referências

### Documentação das Tecnologias

- [FastAPI - Documentação Oficial](https://fastapi.tiangolo.com/)
- [Scikit-learn - User Guide](https://scikit-learn.org/stable/user_guide.html)
- [BeautifulSoup - Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [JWT - Introduction](https://jwt.io/introduction)
- [Pydantic - Documentation](https://docs.pydantic.dev/)

### Fonte de Dados

- [Books to Scrape](https://books.toscrape.com/) - Site de demonstração para práticas de web scraping

---

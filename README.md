# 🏛️ Captura de Dados EPROC - TJMG

Aplicação desenvolvida em **Python** para realizar a **captura automática de dados de processos judiciais** no sistema **eproc** do **TJMG (Tribunal de Justiça de Minas Gerais)**.

A aplicação expõe uma **API REST** construída com **FastAPI**, que consulta nomes de partes no sistema eproc, armazena os resultados em um **banco SQLite** e atualiza automaticamente os dados quando uma nova consulta é feita.

---

## 🚀 Funcionalidades

* ✅ Consulta automática de processos no eproc-TJMG
* ✅ Armazena os dados localmente em banco SQLite
* ✅ Atualiza automaticamente os processos de um nome já consultado
* ✅ Retorna dados via API REST (JSON)
* ✅ Health check para monitoramento da aplicação
* ✅ Documentação interativa automática (Swagger/ReDoc)
* ✅ Arquitetura modular e escalável

---

## ⚙️ Requisitos

* Python **3.8+**
* Google Chrome instalado
* Sistema operacional Windows, Linux ou macOS

---

## 🧩 Instalação e Execução

### 1️⃣ Clonar o projeto

```bash
git clone https://github.com/douglas-filipe/eproc-api
cd eproc-api
```

### 2️⃣ Criar e ativar o ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instalar as dependências

```bash
pip install -r requirements.txt
```

### 6️⃣ Executar a aplicação

```bash
uvicorn main:app --reload
```

## 🌐 Acessando a API

Com a aplicação rodando, acesse:

| Recurso | URL |
|---------|-----|
| 📝 **Swagger UI** | http://127.0.0.1:8000/docs |
| 📘 **ReDoc** | http://127.0.0.1:8000/redoc |
| 🏠 **Home** | http://127.0.0.1:8000/ |
| 💚 **Health Check** | http://127.0.0.1:8000/health |

## 🧠 Como Funciona

### Fluxo de Execução

1. **Requisição**: Cliente faz requisição para `/processos/{nome}`
2. **Validação**: Nome é normalizado (uppercase e trim)
3. **Scraping**: Selenium acessa o site do TJMG
4. **Extração**: Dados são extraídos das tabelas HTML
5. **Persistência**: Dados salvos no SQLite e JSON
6. **Resposta**: JSON formatado é retornado ao cliente

## 🧪 Testando a API

### Via Swagger UI (Recomendado)
1. Acesse http://127.0.0.1:8000/docs
2. Clique no endpoint `/processos/{nome}`
3. Clique em "Try it out"
4. Digite um nome (ex: ADILSON DA SILVA)
5. Clique em "Execute"

---

## 🧪 Testes Unitários

A aplicação possui uma suíte completa de **testes unitários** para os models, garantindo a qualidade e confiabilidade do código.

### 📦 Estrutura de Testes

```
tests/
├── __init__.py
├── conftest.py                      # Fixtures e configurações
├── test_models_parte.py             # Testes do model Parte
├── test_models_processo.py          # Testes do model Processo
├── test_models_relacionamento.py    # Testes de relacionamentos
└── test_models_validacoes.py        # Testes de validações
```

### 🚀 Executando os Testes

```bash
pytest
```

---

## 🧰 Tecnologias Utilizadas

| Tecnologia | Uso |
|------------|-----|
| **Python 3.8+** | Linguagem principal |
| **FastAPI** | Framework web moderno |
| **Selenium** | Web scraping |
| **SQLAlchemy** | ORM para banco de dados |
| **SQLite** | Banco de dados relacional |
| **Uvicorn** | Servidor ASGI |
| **Pydantic** | Validação de dados |
| **WebDriver Manager** | Gerenciamento do ChromeDriver |
| **Pytest** | Framework de testes |
| **Pytest-cov** | Cobertura de testes |

## 📝 Boas Práticas Implementadas

✅ **Separação de responsabilidades** (Routes, Models, Services)  
✅ **Documentação automática** (Swagger/ReDoc)  
✅ **Type hints** em todo código  
✅ **Tratamento de erros** robusto  
✅ **Health checks** para monitoramento  
✅ **Timestamps automáticos** nos registros  
✅ **Cascading deletes** no relacionamento ORM  
✅ **CORS configurado** para integrações  
✅ **Testes unitários** com alta cobertura  

---

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

---

## 🧑‍💻 Autor

Desenvolvido por **Douglas Filipe**.
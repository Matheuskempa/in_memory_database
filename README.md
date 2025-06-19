# IN MEMORY DATABASE PROJECT

[![Python](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/) 
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95-green.svg)](https://fastapi.tiangolo.com/)
[![Redis](https://img.shields.io/badge/Redis-7.0-orange.svg)](https://redis.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)

---

## 📝 Descrição

Projeto para gerenciamento simples de perguntas e respostas, utilizando FastAPI com Redis como banco primário para armazenamento em memória e Redis Streams para eventos, além de persistência em PostgreSQL via worker que consome o stream.

O sistema permite criar, consultar e deletar perguntas e respostas, registrando cada resposta recebida no Redis Stream para processamento assíncrono e armazenamento em banco relacional.

---

## ⚙️ Funcionalidades

- CRUD básico para perguntas (`question`) e respostas (`answer`)
- Armazenamento em Redis usando hashes
- Registro de eventos em Redis Streams (`stream_dados`)
- Worker em Python para consumir eventos do stream e persistir no PostgreSQL
- API RESTful implementada com FastAPI
- Monitoramento básico da saúde da API

---

## 🛠 Tecnologias utilizadas

- Python 3.10+
- FastAPI
- Redis (incluindo RedisGears)
- PostgreSQL 15
- Docker & Docker Compose
- psycopg2 (driver PostgreSQL para Python)
- redis-py (cliente Redis para Python)

---

## 🚀 Como rodar localmente

### Pré-requisitos

- Docker e Docker Compose instalados na sua máquina

### Passos

1. Clone este repositório:

```bash
git clone https://github.com/Matheuskempa/in_memory_database.git
cd in_memory_database


2. Rode os containers com Docker Compose (certifique-se que o arquivo docker-compose.yml está configurado):
```bash
docker compose up --build


3. Acesse a API em:
```bash
docker compose up --build
http://localhost:8000

```

# 📦 Endpoints principais da API

## Health check

- `GET /`  
  Retorna mensagem simples confirmando que a API está online.

## Perguntas (question)

- `POST /question`  
  Cria uma pergunta. Envia a pergunta para o Redis e registra o evento no stream.

- `GET /questions`  
  Lista todas as perguntas.

- `GET /question/{question_id}`  
  Consulta uma pergunta específica.

- `DELETE /question/{question_id}`  
  Deleta uma pergunta.

- `DELETE /questions`  
  Deleta todas as perguntas.

## Respostas (answer)

- `POST /answer`  
  Cria uma resposta, grava no Redis e adiciona evento no stream.

- `GET /answers`  
  Lista todas as respostas com indicação se estão corretas.

- `DELETE /answers`  
  Deleta todas as respostas.

# 🧱 Estrutura dos dados

## Redis

- Perguntas e respostas são armazenadas em **Hashes**, com chaves no formato:

  - `question:{question_id}`

  - `answer:{usuario}:{question_id}:{nro_tentativa}`

- Eventos de criação de perguntas e respostas são enviados para o **Stream Redis** chamado `stream_dados`.

## PostgreSQL

- Tabela `dados` que armazena os eventos consumidos do stream, com campos:

  - `id` (serial)

  - `metodo` (texto, ex: `create_question` ou `create_answer`)

  - `conteudo` (jsonb, com os dados da pergunta ou resposta)

  - `criado_em` (timestamp automático)

# ⚙️ Worker de processamento

- Script Python (`worker.py`) conecta no Redis e PostgreSQL.

- Consome eventos do stream `stream_dados`.

- Persiste eventos no PostgreSQL para garantir durabilidade e análises futuras.

# 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

# 🙋‍♂️ Contato

Matheus Kempa  
[https://github.com/Matheuskempa](https://github.com/Matheuskempa)

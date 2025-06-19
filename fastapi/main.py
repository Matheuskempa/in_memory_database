from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import redis
from typing import List
import uuid
import datetime
import json

app = FastAPI()

class Question(BaseModel):
    question_text: str
    question_id: int
    alternativa_a: str
    alternativa_b: str  
    alternativa_c: str
    alternativa_d: str
    alternativa_correta: str
    dificuldade: str
    assunto: str

class Answer(BaseModel):
    question_id: int
    alternativa_escolhida: str
    datahora: str
    usuario: str
    nro_tentativa: int

IP_CONTAINER = "redis"  


def get_redis_connection():
    try:
        return redis.Redis(host=IP_CONTAINER, port=6379, decode_responses=True)
    except redis.RedisError:
        raise HTTPException(status_code=500, detail="Could not connect to Redis")


@app.get("/", tags=["health check"])
def read_root():
    return {"Hello": "API de teste com Redis e RedisGears"}

# --- Question ---

@app.post("/question", tags=["question"])
def create_question(question: Question):
    r = get_redis_connection()
    key = f"question:{question.question_id}"
    if r.exists(key):
        raise HTTPException(status_code=400, detail="Question already exists")
    
    r.hset(key, mapping=question.dict())

    # Adiciona no stream
    r.xadd("stream_dados", {
        "data": json.dumps({
            "metodo": "create_question",
            "conteudo": question.dict()
        })
    })

    return {"message": "Question created"}

@app.get("/questions", tags=["question"])
def get_all_questions():
    r = get_redis_connection()
    keys = r.keys("question:*")
    return [r.hgetall(k) for k in keys]

@app.get("/question/{question_id}", tags=["question"])
def get_question(question_id: int):
    r = get_redis_connection()
    key = f"question:{question_id}"
    if not r.exists(key):
        raise HTTPException(status_code=404, detail="Question not found")
    return r.hgetall(key)

@app.delete("/question/{question_id}", tags=["question"])
def delete_question(question_id: int):
    r = get_redis_connection()
    key = f"question:{question_id}"
    if not r.exists(key):
        raise HTTPException(status_code=404, detail="Question not found")
    r.delete(key)
    return {"message": "Question deleted"}

@app.delete("/questions", tags=["question"])
def delete_all_questions():
    r = get_redis_connection()
    keys = r.keys("question:*")
    for k in keys:
        r.delete(k)
    return {"message": f"{len(keys)} questions deleted"}

# --- Answer ---

@app.post("/answer", tags=["answer"])
def create_answer(answer: Answer):
    r = get_redis_connection()
    key = f"answer:{answer.usuario}:{answer.question_id}:{answer.nro_tentativa}"
    if r.exists(key):
        raise HTTPException(status_code=400, detail="Answer already exists")

    r.hset(key, mapping=answer.dict())

    # escreve para RedisGears com estrutura compatível com PostgreSQL
    # r.set(str(uuid.uuid4()), {
    #     "metodo": "create_answer",
    #     "conteudo": answer.dict()
    # })

    r.xadd("stream_dados", {
    "data": json.dumps({
        "metodo": "create_answer",
        "conteudo": answer.dict()
    })
})

    return {"message": "Answer created"}

@app.get("/answers", tags=["answer"])
def get_all_answers():
    r = get_redis_connection()
    keys = r.keys("answer:*")
    answers = []
    for k in keys:
        a = r.hgetall(k)
        question_id = a.get("question_id")
        if question_id:
            q = r.hgetall(f"question:{question_id}")
            a['is_correct'] = a.get("alternativa_escolhida") == q.get("alternativa_correta")
        answers.append(a)
    return answers

@app.delete("/answers", tags=["answer"])
def delete_all_answers():
    r = get_redis_connection()
    keys = r.keys("answer:*")
    for k in keys:
        r.delete(k)
    return {"message": f"{len(keys)} answers deleted"}

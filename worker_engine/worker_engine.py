import time
import requests

# Endpoint da sua API FastAPI
API_URL = "http://localhost:8000"

# Perguntas
questions = [
  {
    "question_text": "Qual a capital da França?",
    "question_id": 1,
    "alternativa_a": "Londres",
    "alternativa_b": "Berlim",
    "alternativa_c": "Paris",
    "alternativa_d": "Roma",
    "alternativa_correta": "c",
    "dificuldade": "facil",
    "assunto": "geografia"
  },
  {
    "question_text": "Qual é o resultado de 2 + 2?",
    "question_id": 2,
    "alternativa_a": "3",
    "alternativa_b": "4",
    "alternativa_c": "5",
    "alternativa_d": "22",
    "alternativa_correta": "b",
    "dificuldade": "facil",
    "assunto": "matematica"
  },
  {
    "question_text": "Quem escreveu 'Dom Quixote'?",
    "question_id": 3,
    "alternativa_a": "Miguel de Cervantes",
    "alternativa_b": "William Shakespeare",
    "alternativa_c": "José Saramago",
    "alternativa_d": "Machado de Assis",
    "alternativa_correta": "a",
    "dificuldade": "medio",
    "assunto": "literatura"
  },
  {
    "question_text": "Qual o planeta mais próximo do Sol?",
    "question_id": 4,
    "alternativa_a": "Terra",
    "alternativa_b": "Vênus",
    "alternativa_c": "Marte",
    "alternativa_d": "Mercúrio",
    "alternativa_correta": "d",
    "dificuldade": "facil",
    "assunto": "astronomia"
  },
  {
    "question_text": "Qual a fórmula química da água?",
    "question_id": 5,
    "alternativa_a": "H2O",
    "alternativa_b": "CO2",
    "alternativa_c": "O2",
    "alternativa_d": "NaCl",
    "alternativa_correta": "a",
    "dificuldade": "facil",
    "assunto": "quimica"
  },
  {
    "question_text": "Em que ano o Brasil foi descoberto?",
    "question_id": 6,
    "alternativa_a": "1492",
    "alternativa_b": "1500",
    "alternativa_c": "1822",
    "alternativa_d": "1889",
    "alternativa_correta": "b",
    "dificuldade": "medio",
    "assunto": "historia"
  },
  {
    "question_text": "Qual o maior animal terrestre?",
    "question_id": 7,
    "alternativa_a": "Elefante africano",
    "alternativa_b": "Girafa",
    "alternativa_c": "Hipopótamo",
    "alternativa_d": "Rinoceronte",
    "alternativa_correta": "a",
    "dificuldade": "facil",
    "assunto": "biologia"
  },
  {
    "question_text": "Quem pintou a Mona Lisa?",
    "question_id": 8,
    "alternativa_a": "Pablo Picasso",
    "alternativa_b": "Leonardo da Vinci",
    "alternativa_c": "Vincent van Gogh",
    "alternativa_d": "Michelangelo",
    "alternativa_correta": "b",
    "dificuldade": "facil",
    "assunto": "arte"
  },
  {
    "question_text": "Qual a velocidade da luz no vácuo?",
    "question_id": 9,
    "alternativa_a": "300.000 km/s",
    "alternativa_b": "150.000 km/s",
    "alternativa_c": "1.000 km/s",
    "alternativa_d": "3.000 km/s",
    "alternativa_correta": "a",
    "dificuldade": "medio",
    "assunto": "fisica"
  },
  {
    "question_text": "Qual é o símbolo químico do ouro?",
    "question_id": 10,
    "alternativa_a": "Au",
    "alternativa_b": "Ag",
    "alternativa_c": "Pb",
    "alternativa_d": "Fe",
    "alternativa_correta": "a",
    "dificuldade": "facil",
    "assunto": "quimica"
  }
]

# Respostas
answers = [
  {"question_id":1, "alternativa_escolhida":"c", "datahora":"2024-01-01T10:00:00", "usuario":"user1", "nro_tentativa":1},
  {"question_id":1, "alternativa_escolhida":"a", "datahora":"2024-01-01T10:05:00", "usuario":"user2", "nro_tentativa":1},
  {"question_id":1, "alternativa_escolhida":"c", "datahora":"2024-01-01T10:10:00", "usuario":"user3", "nro_tentativa":1},
  {"question_id":1, "alternativa_escolhida":"d", "datahora":"2024-01-01T10:15:00", "usuario":"user4", "nro_tentativa":1},

  {"question_id":2, "alternativa_escolhida":"b", "datahora":"2024-01-02T10:00:00", "usuario":"user1", "nro_tentativa":1},
  {"question_id":2, "alternativa_escolhida":"b", "datahora":"2024-01-02T10:05:00", "usuario":"user2", "nro_tentativa":1},
  {"question_id":2, "alternativa_escolhida":"c", "datahora":"2024-01-02T10:10:00", "usuario":"user3", "nro_tentativa":1},
  {"question_id":2, "alternativa_escolhida":"a", "datahora":"2024-01-02T10:15:00", "usuario":"user4", "nro_tentativa":1},

  {"question_id":3, "alternativa_escolhida":"a", "datahora":"2024-01-03T10:00:00", "usuario":"user1", "nro_tentativa":1},
  {"question_id":3, "alternativa_escolhida":"b", "datahora":"2024-01-03T10:05:00", "usuario":"user2", "nro_tentativa":1},
  {"question_id":3, "alternativa_escolhida":"a", "datahora":"2024-01-03T10:10:00", "usuario":"user3", "nro_tentativa":1},
  {"question_id":3, "alternativa_escolhida":"d", "datahora":"2024-01-03T10:15:00", "usuario":"user4", "nro_tentativa":1},

  {"question_id":4, "alternativa_escolhida":"d", "datahora":"2024-01-04T10:00:00", "usuario":"user1", "nro_tentativa":1},
  {"question_id":4, "alternativa_escolhida":"b", "datahora":"2024-01-04T10:05:00", "usuario":"user2", "nro_tentativa":1},
  {"question_id":4, "alternativa_escolhida":"d", "datahora":"2024-01-04T10:10:00", "usuario":"user3", "nro_tentativa":1},
  {"question_id":4, "alternativa_escolhida":"a", "datahora":"2024-01-04T10:15:00", "usuario":"user4", "nro_tentativa":1},

  {"question_id":5, "alternativa_escolhida":"a", "datahora":"2024-01-05T10:00:00", "usuario":"user1", "nro_tentativa":1},
  {"question_id":5, "alternativa_escolhida":"d", "datahora":"2024-01-05T10:05:00", "usuario":"user2", "nro_tentativa":1},
  {"question_id":5, "alternativa_escolhida":"a", "datahora":"2024-01-05T10:10:00", "usuario":"user3", "nro_tentativa":1},
  {"question_id":5, "alternativa_escolhida":"c", "datahora":"2024-01-05T10:15:00", "usuario":"user4", "nro_tentativa":1},

  {"question_id":6, "alternativa_escolhida":"b", "datahora":"2024-01-06T10:00:00", "usuario":"user1", "nro_tentativa":1},
  {"question_id":6, "alternativa_escolhida":"a", "datahora":"2024-01-06T10:05:00", "usuario":"user2", "nro_tentativa":1},
  {"question_id":6, "alternativa_escolhida":"b", "datahora":"2024-01-06T10:10:00", "usuario":"user3", "nro_tentativa":1},
  {"question_id":6, "alternativa_escolhida":"d", "datahora":"2024-01-06T10:15:00", "usuario":"user4", "nro_tentativa":1},

  {"question_id":7, "alternativa_escolhida":"a", "datahora":"2024-01-07T10:00:00", "usuario":"user1", "nro_tentativa":1},
  {"question_id":7, "alternativa_escolhida":"c", "datahora":"2024-01-07T10:05:00", "usuario":"user2", "nro_tentativa":1},
  {"question_id":7, "alternativa_escolhida":"a", "datahora":"2024-01-07T10:10:00", "usuario":"user3", "nro_tentativa":1},
  {"question_id":7, "alternativa_escolhida":"b", "datahora":"2024-01-07T10:15:00", "usuario":"user4", "nro_tentativa":1},

  {"question_id":8, "alternativa_escolhida":"b", "datahora":"2024-01-08T10:00:00", "usuario":"user1", "nro_tentativa":1},
  {"question_id":8, "alternativa_escolhida":"a", "datahora":"2024-01-08T10:05:00", "usuario":"user2", "nro_tentativa":1},
  {"question_id":8, "alternativa_escolhida":"b", "datahora":"2024-01-08T10:10:00", "usuario":"user3", "nro_tentativa":1},
  {"question_id":8, "alternativa_escolhida":"d", "datahora":"2024-01-08T10:15:00", "usuario":"user4", "nro_tentativa":1},

  {"question_id":9, "alternativa_escolhida":"a", "datahora":"2024-01-09T10:00:00", "usuario":"user1", "nro_tentativa":1},
  {"question_id":9, "alternativa_escolhida":"d", "datahora":"2024-01-09T10:05:00", "usuario":"user2", "nro_tentativa":1},
  {"question_id":9, "alternativa_escolhida":"a", "datahora":"2024-01-09T10:10:00", "usuario":"user3", "nro_tentativa":1},
  {"question_id":9, "alternativa_escolhida":"b", "datahora":"2024-01-09T10:15:00", "usuario":"user4", "nro_tentativa":1},

  {"question_id":10, "alternativa_escolhida":"a", "datahora":"2024-01-10T10:00:00", "usuario":"user1", "nro_tentativa":1},
  {"question_id":10, "alternativa_escolhida":"b", "datahora":"2024-01-10T10:05:00", "usuario":"user2", "nro_tentativa":1},
  {"question_id":10, "alternativa_escolhida":"a", "datahora":"2024-01-10T10:10:00", "usuario":"user3", "nro_tentativa":1},
  {"question_id":10, "alternativa_escolhida":"d", "datahora":"2024-01-10T10:15:00", "usuario":"user4", "nro_tentativa":1}
]

# Envia perguntas
print("Enviando perguntas...")
for q in questions:
    try:
        res = requests.post(f"{API_URL}/question", json=q)
        print(f"[Pergunta {q['question_id']}] Status: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"Erro ao enviar pergunta {q['question_id']}: {e}")
    time.sleep(1)

# Envia respostas
print("Enviando respostas...")
for a in answers:
    try:
        res = requests.post(f"{API_URL}/answer", json=a)
        print(f"[Resposta Q{a['question_id']} de {a['usuario']}] Status: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"Erro ao enviar resposta: {e}")
    time.sleep(1)

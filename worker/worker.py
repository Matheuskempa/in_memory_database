import redis
import psycopg2
import json
import time

IP_CONTAINER_REDIS = "redis"
IP_CONTAINER_POSTGRES = "postgres"

# Conectar Redis
while True:
    try:
        redis_client = redis.Redis(host=IP_CONTAINER_REDIS, port=6379, decode_responses=True)
        if redis_client.ping():
            print("Conectado ao Redis!")
            break 
    except Exception as e:
        print(f"Erro ao conectar no Redis: {e}. Tentando novamente em 3s...")
    time.sleep(3)

# Conectar Postgres
while True:
    try:
        conn_postgres = psycopg2.connect(
            host=IP_CONTAINER_POSTGRES,
            port=5432,
            user='admin',
            password='admin',
            dbname='app_db'
        )
        conn_postgres.autocommit = True
        print("Conectado ao Postgres!")
        break
    except Exception as e:
        print(f"Erro ao conectar no Postgres: {e}. Tentando novamente em 3s...")
    time.sleep(3)

print("Iniciando consumo do stream...")
last_id = '0-0'

while True:
    print("loop")
    try:
        response = redis_client.xread({'stream_dados': last_id}, count=10, block=1000)
        
        if response:
            for stream_name, messages in response:
                for message_id, message_data in messages:
                    last_id = message_id
                    data_json = message_data.get("data")  # já é str
                    data = json.loads(data_json)

                    with conn_postgres.cursor() as cur:
                        cur.execute(
                            "INSERT INTO dados (metodo, conteudo) VALUES (%s, %s)",
                            (data.get('metodo'), json.dumps(data.get('conteudo')))
                        )
                    print(f"Registrado {data.get('metodo')} no Postgres.")
        else:
            time.sleep(1)
    except Exception as e:
        print(f"Erro no processamento da stream: {e}. Tentando continuar...")
        time.sleep(1)

import json
import psycopg2

# Configuração do banco Postgres
conn = psycopg2.connect(
    host='postgres',
    port=5432,
    user='admin',
    password='admin',
    dbname='app_db'
)
conn.autocommit = True  # Para evitar commit manual

GB = GearsBuilder('KeysReader')

def salvar_no_postgres(record):
    try:
        r = record['value']
        if not isinstance(r, str) or not r.startswith('{'):
            return

        data = json.loads(r)

        with conn.cursor() as cur:
            # Ajuste a query e os campos conforme seu schema
            cur.execute(
                "INSERT INTO dados (metodo, conteudo) VALUES (%s, %s)",
                (data.get('metodo'), json.dumps(data.get('conteudo')))
            )

    except Exception as e:
        # Pode salvar erro num key Redis
        record.execute('SET', 'erro:gears', str(e))

GB.map(salvar_no_postgres).register('*')

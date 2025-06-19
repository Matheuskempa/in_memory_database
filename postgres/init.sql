CREATE TABLE IF NOT EXISTS dados (
    id SERIAL PRIMARY KEY,
    metodo varchar(100),
    conteudo JSONB
);

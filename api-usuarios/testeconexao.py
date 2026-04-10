import psycopg2

print("Iniciando teste...")

CONN_STR = "postgresql://neondb_owner:npg_HYPB1jJa0Xpw@ep-dark-paper-acegdo2q-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require"

try:
    print("Tentando conectar...")
    conexao = psycopg2.connect(CONN_STR, connect_timeout=10)
    print("Conexão com o banco realizada com sucesso!")
    conexao.close()
    print("Fim do teste.")
except Exception as e:
    print("Erro ao conectar:")
    print(repr(e))
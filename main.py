from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2

app = FastAPI()

DB_HOST = "ep-sparkling-resonance-acjth5op-pooler.sa-east-1.aws.neon.tech"
DB_NAME = "neondb"
DB_USER = "neondb_owner"
DB_PASSWORD = "npg_Q5ZK9VIHxfvq"
DB_PORT = 5432


def conectar():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        sslmode="require"
    )


class AlunoCreate(BaseModel):
    nome: str
    nota: float


@app.get("/")
def home():
    return {"mensagem": "API funcionando"}


@app.get("/alunos")
def listar_alunos():
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome, nota FROM alunos ORDER BY id")
        alunos = cursor.fetchall()
        conexao.close()

        return [{"id": a[0], "nome": a[1], "nota": float(a[2])} for a in alunos]
    except Exception as e:
        return {"erro": str(e)}


@app.get("/alunos/buscar")
def buscar_alunos(nome: str):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id, nome, nota FROM alunos WHERE nome ILIKE %s ORDER BY id",
            (f"%{nome}%",)
        )
        alunos = cursor.fetchall()
        conexao.close()

        return [{"id": a[0], "nome": a[1], "nota": float(a[2])} for a in alunos]
    except Exception as e:
        return {"erro": str(e)}


@app.post("/alunos")
def cadastrar_aluno(aluno: AlunoCreate):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT id FROM alunos WHERE nome = %s", (aluno.nome,))
        existe = cursor.fetchone()

        if existe:
            conexao.close()
            return {"erro": "Aluno já cadastrado."}

        cursor.execute(
            "INSERT INTO alunos (nome, nota) VALUES (%s, %s)",
            (aluno.nome, aluno.nota)
        )
        conexao.commit()
        conexao.close()

        return {"mensagem": "Aluno cadastrado com sucesso."}
    except Exception as e:
        return {"erro": str(e)}
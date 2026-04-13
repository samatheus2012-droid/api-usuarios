from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

DB_HOST = "ep-dark-paper-acegdo2q-pooler.sa-east-1.aws.neon.tech"
DB_NAME = "neondb"
DB_USER = "neondb_owner"
DB_PASSWORD = "npg_HYPB1jJa0Xpw"
DB_PORT = 5432

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=false,
    allow_methods=["*"],
    allow_headers=["*"],
)

def conectar():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        sslmode="require"
    )

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str

class LoginCreate(BaseModel):
    nome: str
    email: str
    senha: str

class AlunoCreate(BaseModel):
    nome: str
    nota: float

#TESTE CORS
@app.get("/")
def home():
    return {"mensagem": "API funcionando"}

@app.get("/home")
def get_home():
    return {"mensagem": "Bem-vindo à API da escola"}

@app.get("/home/alunos")
def get_home_alunos():
    return {"mensagem": "Área de alunos"}

@app.get("/home/alunos/doc")
def get_home_alunos_doc():
    return {"mensagem": "Documentação dos alunos"}

@app.post("/usuarios")
def cadastrar_usuario(usuario: UsuarioCreate):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (usuario.email,))
        existe = cursor.fetchone()

        if existe:
            return {"erro": "Usuário já cadastrado."}

        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
            (usuario.nome, usuario.email, usuario.senha)
        )
        conexao.commit()

        return {"mensagem": "Usuário cadastrado com sucesso."}

    except Exception as e:
        return {"erro": str(e)}

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

@app.post("/login")
def login(usuario: LoginCreate):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT id, nome, email FROM usuarios WHERE nome = %s AND email = %s AND senha = %s",
            (usuario.nome, usuario.email, usuario.senha)
        )
        usuario_encontrado = cursor.fetchone()

        if not usuario_encontrado:
            return {"erro": "Nome, e-mail ou senha inválidos."}

        return {
            "mensagem": "Login realizado com sucesso.",
            "usuario": {
                "id": usuario_encontrado[0],
                "nome": usuario_encontrado[1],
                "email": usuario_encontrado[2]
            }
        }

    except Exception as e:
        return {"erro": str(e)}

    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

@app.post("/alunos")
def cadastrar_aluno(aluno: AlunoCreate):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT id FROM alunos WHERE nome = %s", (aluno.nome,))
        existe = cursor.fetchone()

        if existe:
            return {"erro": "Aluno já cadastrado."}

        cursor.execute(
            "INSERT INTO alunos (nome, nota) VALUES (%s, %s)",
            (aluno.nome, aluno.nota)
        )
        conexao.commit()

        return {"mensagem": "Aluno cadastrado com sucesso."}

    except Exception as e:
        return {"erro": str(e)}

    finally:
        if cursor:
            cursor.close()

        if conexao:
            conexao.close()

@app.get("/alunos/buscar")
def buscar_aluno(nome: str):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT nome, nota FROM alunos WHERE nome ILIKE %s",
            (f"%{nome}%",)
        )
        resultados = cursor.fetchall()

        alunos = []
        for aluno in resultados:
            alunos.append({
                "nome": aluno[0],
                "nota": float(aluno[1])
            })

        return alunos

    except Exception as e:
        return {"erro": str(e)}

    finally:


        if cursor:
            cursor.close()

        if conexao:
            conexao.close()








# suas rotas abaixo
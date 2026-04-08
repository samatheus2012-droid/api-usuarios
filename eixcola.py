import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import requests

API_URL = "https://api-escola-ma08.onrender.com"

janela = ttk.Window(themename="superhero")
janela.title("Banco Escolar")
janela.geometry("1000x700")

def cadastro():
    limpar_tela()

    label1 = ttk.Label(janela, text = "Cadastro", font = ("Arial", 30))
    label1.place(x=230, Y=20)

    l_cd = ttk.Label(janela, text = "Digite seu e-mail:", )
    l_cd.place(x=480, y=180)

    e_cd = ttk.Entry(janela, show = "*")
    e_cd.place(x=480, y=200)

def limpar_tela():
    for widget in janela.winfo_children():
        widget.place_forget()

def tela_inicial():
    limpar_tela()

    texto_0 = ttk.Label(janela, text="O que deseja fazer?", font=("Arial", 30))
    texto_0.place(x=190, y=20)

    bt_cadastrar = ttk.Button(janela, text="Cadastrar aluno", command=perguntas, padx=30)
    bt_cadastrar.place(x=299, y=100)

    bt_procurar = ttk.Button(janela, text="Procurar aluno", command=procurar, padx=30)
    bt_procurar.place(x=300, y=150)

    bt_sair = ttk.Button(janela, text="Sair", command=fechar, padx=30)
    bt_sair.place(x=330, y=200)

def voltar():
    tela_inicial()

def salvar_aluno():
    nome = pergunta1.get().strip()
    nota_texto = pergunta2.get().strip()

    if not nome:
        aviso = ttk.Label(janela, text="Digite o nome do aluno!")
        aviso.place(x=280, y=330)
        return

    try:
        nota = float(nota_texto)
    except ValueError:
        aviso = ttk.Label(janela, text="Digite uma nota válida!")
        aviso.place(x=280, y=330)
        return

    try:
        resposta = requests.post(f"{API_URL}/alunos",json={"nome": nome, "nota": nota},timeout=10)

        dados = resposta.json()

        if resposta.status_code == 200 or resposta.status_code == 201:
            aviso = ttk.Label(janela, text="Aluno cadastrado com sucesso!")
            aviso.place(x=250, y=330)
        else:
            mensagem = dados.get("erro", "Erro ao cadastrar aluno.")
            aviso = ttk.Label(janela, text=mensagem)
            aviso.place(x=220, y=330)
    except requests.exceptions.RequestException:
        aviso = ttk.Label(janela, text="Erro ao conectar com a API!")
        aviso.place(x=240, y=330)

def perguntas():
    global pergunta1, pergunta2

    limpar_tela()

    texto_1 = ttk.Label(janela, text="Cadastro", font=("Arial", 30))
    texto_1.place(x=275, y=40)

    texto1 = ttk.Label(janela, text="Nome do aluno:")
    texto1.place(x=295, y=130)
    pergunta1 = ttk.Entry(janela)
    pergunta1.place(x=295, y=150)

    texto2 = ttk.Label(janela, text="Nota do aluno:")
    texto2.place(x=295, y=200)
    pergunta2 = ttk.Entry(janela)
    pergunta2.place(x=295, y=220)

    bt_salvar = ttk.Button(janela, text = "Cadastrar aluno", command = salvar_aluno, relief = "solid")
    bt_salvar.place(x=310, y=260)

    bt_voltar = ttk.Button(janela, text = "Voltar", command = voltar, padx = 40, bootstyle = secondary)
    bt_voltar.place(x=295, y=300)

def fechar():
    janela.destroy()

def procurar():
    global pergunta3

    limpar_tela()

    texto_2 = ttk.Label(janela, text="Procurar Aluno", font=("Arial", 30))
    texto_2.place(x=220, y=20)

    texto3 = ttk.Label(janela, text="Nome do aluno:")
    texto3.place(x=280, y=130)

    pergunta3 = ttk.Entry(janela)
    pergunta3.place(x=280, y=150)

    bt_p = ttk.Button(janela, text="Procurar aluno", command=procurar2, relief="solid")
    bt_p.place(x=295, y=220)

    bt_voltar = ttk.Button(janela, text="Voltar", command=voltar, padx=40, relief="solid")
    bt_voltar.place(x=280, y=260)

def procurar2():
    nome_digitado = pergunta3.get().strip()

    if not nome_digitado:
        aviso = ttk.Label(janela, text="Digite um nome para pesquisar!")
        aviso.place(x=240, y=300)
        return

    try:
        resposta = requests.get(
            f"{API_URL}/alunos/buscar",
            params={"nome": nome_digitado},
            timeout=10
        )

        dados = resposta.json()

        y = 60

        if isinstance(dados, list) and dados:
            aviso = ttk.Label(janela, text="Resultados encontrados")
            aviso.place(x=20, y=20)

            for aluno in dados:
                label = ttk.Label(janela, text=f"{aluno['nome']} - Nota: {aluno['nota']}")
                label.place(x=20, y=y)
                y += 30
        else:
            sem_resultado = ttk.Label(janela, text="Aluno não encontrado!")
            sem_resultado.place(x=280, y=180)

    except requests.exceptions.RequestException:
        erro_api = ttk.Label(janela, text="Erro ao conectar com a API!")
        erro_api.place(x=240, y=180)


texto_3 = ttk.Label(janela, text = "já tem uma conta?", font = ("Arial", 30))
texto_3.place(x=300, y=20)

bt_1 = ttk.Button(janela, text = "Cadastrar", command = cadastro, width=30, padding=10)
bt_1.place(x=380, y=120)

bt_2 = ttk.Button(janela, text = "Log in", width=30, padding=10)
bt_2.place(x=380, y=190)


janela.mainloop()
import customtkinter as ctk
import requests

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

API_URL = "https://api-escola-ma08.onrender.com"

janela = ctk.CTk()
janela.title("Banco Escolar")
janela.geometry("800x500")


def fazer_login():
    global entry_email_login, entry_senha_login, entry_nome

    limpar_tela()

    label_entrar = ctk.CTkLabel(janela, text="Entrar", font=("Arial", 30))
    label_entrar.place(x=300, y=20)

    label_email = ctk.CTkLabel(janela, text="Digite seu e-mail:")
    entry_email_login = ctk.CTkEntry(janela)
    label_email.place(x=300, y=140)
    entry_email_login.place(x=300, y=160)

    label_nome = ctk.CTkLabel(janela, text="Digite seu nome:")
    entry_nome = ctk.CTkEntry(janela)
    label_nome.place(x=300, y=220)
    entry_nome.place(x=300, y=240)

    label_senha = ctk.CTkLabel(janela, text="Digite sua senha:")
    entry_senha_login = ctk.CTkEntry(janela, show="*")
    label_senha.place(x=300, y=300)
    entry_senha_login.place(x=300, y=320)

    botao_entrar = ctk.CTkButton(janela, text="Entrar", command=login)
    botao_entrar.place(x=300, y=380)

    botao_voltar = ctk.CTkButton(janela, text="Voltar", command=tela_inicial1)
    botao_voltar.place(x=300, y=420)

def entrar():

    global entry_nome_cadastro, entry_email_cadastro, entry_senha_cadastro

    limpar_tela()

    label_titulo_login = ctk.CTkLabel(janela, text="Cadastro", font=("Arial", 30))
    label_titulo_login.place(x=300, y=20)

    label_nome = ctk.CTkLabel(janela, text="Digite seu nome:")
    entry_nome_cadastro = ctk.CTkEntry(janela)
    label_nome.place(x=350, y=120)
    entry_nome_cadastro.place(x=350, y=140)

    label_login = ctk.CTkLabel(janela, text="Digite seu e-mail:")
    entry_email_cadastro = ctk.CTkEntry(janela)
    label_login.place(x=350, y=180)
    entry_email_cadastro.place(x=350, y=200)

    label1_login = ctk.CTkLabel(janela, text="Digite sua senha:")
    entry_senha_cadastro = ctk.CTkEntry(janela, show="*")
    label1_login.place(x=350, y=240)
    entry_senha_cadastro.place(x=350, y=260)

    entry2_login = ctk.CTkButton(janela, text="Cadastrar", command=cadastrar_usuario)
    entry2_login.place(x=350, y=300)

    botao_voltar = ctk.CTkButton(janela, text="Voltar", command=tela_inicial1)
    botao_voltar.place(x=350, y=340)

def cadastrar_usuario():
    nome = entry_nome_cadastro.get().strip()
    email = entry_email_cadastro.get().strip()
    senha = entry_senha_cadastro.get().strip()

    if not nome or not email or not senha:
        aviso = ctk.CTkLabel(janela, text="Preencha nome, e-mail e senha!")
        aviso.place(x=280, y=380)
        return

    try:
        resposta = requests.post(f"{API_URL}/usuarios", json={"nome": nome,"email": email,"senha": senha},timeout=10)

        dados = resposta.json()

        if resposta.status_code == 200 or resposta.status_code == 201:
            aviso = ctk.CTkLabel(janela, text="Usuário cadastrado com sucesso!")
            aviso.place(x=270, y=380)
        else:
            mensagem = dados.get("erro", "Erro ao cadastrar usuário.")
            aviso = ctk.CTkLabel(janela, text=mensagem)
            aviso.place(x=250, y=380)

    except requests.exceptions.RequestException:
        aviso = ctk.CTkLabel(janela, text="Erro ao conectar com a API!")
        aviso.place(x=260, y=380)

def login():
    nome = entry_nome.get().strip()
    email = entry_email_login.get().strip()
    senha = entry_senha_login.get().strip()

    if not nome or not email or not senha:
        aviso = ctk.CTkLabel(janela, text="Preencha nome, e-mail e senha!")
        aviso.place(x=260, y=440)
        return

    try:
        resposta = requests.post(
            f"{API_URL}/login",
            json={"nome": nome, "email": email, "senha": senha},
            timeout=10
        )

        dados = resposta.json()

        if resposta.status_code == 200 and "erro" not in dados:
            tela_inicial()
        else:
            mensagem = dados.get("erro", "Nome, e-mail ou senha inválidos.")
            aviso = ctk.CTkLabel(janela, text=mensagem)
            aviso.place(x=230, y=440)

    except requests.exceptions.RequestException:
        aviso = ctk.CTkLabel(janela, text="Erro ao conectar com a API!")
        aviso.place(x=260, y=440)

def tela_inicial1():

    limpar_tela()

    label_ti = ctk.CTkLabel(janela, text = "Já tem uma conta?", font = ("Arial", 30))
    entry1 = ctk.CTkButton(janela, text = "Fazer login", command = fazer_login)
    entry2 = ctk.CTkButton(janela, text = "Entrar",command = entrar)

    label_ti.place(x=300, y=20)
    entry1.place(x=380, y=120)
    entry2.place(x=380, y=190)

def limpar_tela():
    for widget in janela.winfo_children():
        widget.destroy()

def tela_inicial():
    limpar_tela()

    label_telainicial = ctk.CTkLabel(janela, text="O que deseja fazer?", font=("Arial", 30))
    buton_ti = ctk.CTkButton(janela, text="Cadastrar aluno", command=perguntas, width=180)
    buton1_ti = ctk.CTkButton(janela, text="Procurar aluno", command=procurar, width=180)
    buton_s = ctk.CTkButton(janela, text="Sair", command=fechar, width=180)

    label_telainicial.place(x=190, y=20)
    buton_ti.place(x=299, y=100)
    buton1_ti.place(x=300, y=150)
    buton_s.place(x=330, y=200)

def salvar_aluno():
    nome = entry_p.get().strip()
    nota_texto = entry1_p.get().strip()

    if not nome:
        aviso = ctk.CTkLabel(janela, text="Digite o nome do aluno!")
        aviso.place(x=280, y=330)
        return

    try:
        nota = float(nota_texto)
    except ValueError:
        aviso = ctk.CTkLabel(janela, text="Digite uma nota válida!")
        aviso.place(x=280, y=330)
        return

    try:
        resposta = requests.post(f"{API_URL}/alunos",json={"nome": nome, "nota": nota},timeout=10)

        dados = resposta.json()

        if resposta.status_code == 200 or resposta.status_code == 201:
            aviso = ctk.CTkLabel(janela, text="Aluno cadastrado com sucesso!")
            aviso.place(x=250, y=330)
        else:
            mensagem = dados.get("erro", "Erro ao cadastrar aluno.")
            aviso = ctk.CTkLabel(janela, text=mensagem)
            aviso.place(x=220, y=330)
    except requests.exceptions.RequestException:
        aviso = ctk.CTkLabel(janela, text="Erro ao conectar com a API!")
        aviso.place(x=240, y=330)

def perguntas():
    global entry_p, entry1_p

    limpar_tela()

    label_perguntas = ctk.CTkLabel(janela, text="Cadastro", font=("Arial", 30))
    label_perguntas.place(x=275, y=40)

    label_p = ctk.CTkLabel(janela, text="Nome do aluno:")
    entry_p = ctk.CTkEntry(janela)
    label_p.place(x=295, y=130)
    entry_p.place(x=295, y=150)

    label1_p = ctk.CTkLabel(janela, text="Nota do aluno:")
    entry1_p = ctk.CTkEntry(janela)
    label1_p.place(x=295, y=200)
    entry1_p.place(x=295, y=220)

    bt_salvar = ctk.CTkButton(janela, text = "Cadastrar aluno", command = salvar_aluno)
    bt_salvar.place(x=310, y=260)

    bt_voltar = ctk.CTkButton(janela, text = "Voltar", command = tela_inicial)
    bt_voltar.place(x=295, y=300)

def fechar():
    janela.destroy()

def procurar():
    global entry_pr

    limpar_tela()

    
    label_procurar = ctk.CTkLabel(janela, text ="Procurar Aluno", font = ("Arial", 30))
    
    label_pr1 = ctk.CTkLabel(janela, text ="Nome do aluno:")
    entry_pr = ctk.CTkEntry(janela)
    buton_pr = ctk.CTkButton(janela, text = "Procurar aluno", command = procurar2)
    buton_vt = ctk.CTkButton(janela, text = "Voltar", command = tela_inicial)
    label_procurar.place(x=220, y=20)
    label_pr1.place(x=280, y=130)
    entry_pr.place(x=280, y=150)
    buton_pr.place(x=295, y=220)
    buton_vt.place(x=280, y=260)

def procurar2():
    nome_digitado = entry_pr.get().strip()

    if not nome_digitado:
        aviso = ctk.CTkLabel(janela, text="Digite um nome para pesquisar!")
        aviso.place(x=240, y=300)
        return

    try:
        resposta = requests.get(f"{API_URL}/alunos/buscar",params={"nome": nome_digitado},timeout=10)

        dados = resposta.json()

        y = 60

        if isinstance(dados, list) and dados:
            aviso = ctk.CTkLabel(janela, text="Resultados encontrados")

            aviso.place(x=20, y=20)

            for aluno in dados:
                label = ctk.CTkLabel(janela, text=f"{aluno['nome']} - Nota: {aluno['nota']}")
                label.place(x=20, y=y)
                y += 30
        else:
            sem_resultado = ctk.CTkLabel(janela, text="Aluno não encontrado!")
            sem_resultado.place(x=280, y=180)

    except requests.exceptions.RequestException:
        erro_api = ctk.CTkLabel(janela, text="Erro ao conectar com a API!")
        erro_api.place(x=240, y=180)




label3 = ctk.CTkLabel(janela, text = "já tem uma conta?", font = ("Arial", 30))
entry1 = ctk.CTkButton(janela, text = "Fazer login", command = fazer_login)
entry2 = ctk.CTkButton(janela, text = "Entrar",command = entrar)

label3.place(x=300, y=20)
entry1.place(x=300, y=120)
entry2.place(x=300, y=190)



janela.mainloop()
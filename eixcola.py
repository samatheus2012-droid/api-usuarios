import customtkinter as ctk
import requests

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

API_URL = "https://api-escola-ma08.onrender.com"

janela = ctk.CTk()
janela.title("Banco Escolar")
janela.geometry("800x500")

def cadastro():
    limpar_tela()

    label1 = ctk.CTkLabel(janela, text = "Cadastro", font = ("Arial", 30))
    label1.place(x=230, y=20)

    l_cd = ctk.CTkLabel(janela, text = "Digite seu e-mail:", )
    l_cd.place(x=480, y=180)
    e_cd = ctk.CTkEntry(janela)
    e_cd.place(x=480, y=200)

    l_cds = ctk.CTkLabel(janela, text = "Digite sua senha:")
    l_cds.place(x=480, y=240)
    e_cds = ctk.CTkEntry(janela,show = "*")
    e_cds.place(x=480, y=260)

def log_in():

    limpar_tela()

    label2 = ctk.CTkLabel(janela, text = "Log in", font = ("Arial", 30))
    label2.place(x=230, y=20)

    l_cd1 = ctk.CTkLabel(janela, text = "Digite seu e-mail:", )
    e_cd1 = ctk.CTkEntry(janela)
    l_cd1.place(x=480, y=180)
    e_cd1.place(x=480, y=200)

    l_cds1 = ctk.CTkLabel(janela, text = "Digite sua senha:")
    e_cds1 = ctk.CTkEntry(janela,show = "*")
    l_cds1.place(x=480, y=240)
    e_cds1.place(x=480, y=260)

def limpar_tela():
    for widget in janela.winfo_children():
        widget.place_forget()

def tela_inicial():
    limpar_tela()

    texto_0 = ctk.CTkLabel(janela, text="O que deseja fazer?", font=("Arial", 30))
    texto_0.place(x=190, y=20)

    bt_cadastrar = ctk.CTkButton(janela, text="Cadastrar aluno", command=perguntas, width=180)
    bt_cadastrar.place(x=299, y=100)

    bt_procurar = ctk.CTkButton(janela, text="Procurar aluno", command=procurar, width=180)
    bt_procurar.place(x=300, y=150)

    bt_sair = ctk.CTkButton(janela, text="Sair", command=fechar, width=180)
    bt_sair.place(x=330, y=200)

def voltar():
    tela_inicial()

def salvar_aluno():
    nome = pergunta1.get().strip()
    nota_texto = pergunta2.get().strip()

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
    global pergunta1, pergunta2

    limpar_tela()

    texto_1 = ctk.CTkLabel(janela, text="Cadastro", font=("Arial", 30))
    texto_1.place(x=275, y=40)

    texto1 = ctk.CTkLabel(janela, text="Nome do aluno:")
    texto1.place(x=295, y=130)
    pergunta1 = ctk.CTkEntry(janela)
    pergunta1.place(x=295, y=150)

    texto2 = ctk.CTkLabel(janela, text="Nota do aluno:")
    texto2.place(x=295, y=200)
    pergunta2 = ctk.CTkEntry(janela)
    pergunta2.place(x=295, y=220)

    bt_salvar = ctk.CTkButton(janela, text = "Cadastrar aluno", command = salvar_aluno)
    bt_salvar.place(x=310, y=260)

    bt_voltar = ctk.CTkButton(janela, text = "Voltar", command = voltar)
    bt_voltar.place(x=295, y=300)

def fechar():
    janela.destroy()

def procurar():
    global pergunta3

    limpar_tela()

    texto_2 = ctk.CTkLabel(janela, text="Procurar Aluno", font=("Arial", 30))
    texto_2.place(x=220, y=20)

    texto3 = ctk.CTkLabel(janela, text="Nome do aluno:")
    texto3.place(x=280, y=130)

    pergunta3 = ctk.CTkEntry(janela)
    pergunta3.place(x=280, y=150)

    bt_p = ctk.CTkButton(janela, text="Procurar aluno", command=procurar2, relief="solid")
    bt_p.place(x=295, y=220)

    bt_voltar = ctk.CTkButton(janela, text="Voltar", command=voltar)
    bt_voltar.place(x=280, y=260)

def procurar2():
    nome_digitado = pergunta3.get().strip()

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


texto_3 = ctk.CTkLabel(janela, text = "já tem uma conta?", font = ("Arial", 30))
bt_1 = ctk.CTkButton(janela, text = "Cadastrar", command = cadastro)
bt_2 = ctk.CTkButton(janela, text = "Log in",command = log_in)

texto_3.place(x=300, y=20)
bt_1.place(x=380, y=120)
bt_2.place(x=380, y=190)



janela.mainloop()
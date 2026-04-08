import ttkbootstrap as ttk

app = ttk.Window(themename="superhero")
app.geometry("400x300")

entry = ttk.Entry(
    app,
    width=30,
    font=("Arial", 12),
    justify="center",
    bootstyle="info"
)
entry.pack(pady=10)

senha = ttk.Entry(
    app,
    width=30,
    show="*",
    font=("Arial", 12),
    bootstyle="warning"
)
senha.pack(pady=10)

botao = ttk.Button(
    app,
    text="Entrar",
    padding=10,
    bootstyle="success"
)
botao.pack(pady=20)

app.mainloop()
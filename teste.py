import customtkinter as ctk

ctk.set_appearance_mode("dark")  # dark ou light
ctk.set_default_color_theme("blue")  # tema base

app = ctk.CTk()
app.geometry("400x300")

botao = ctk.CTkButton(
    app,
    text="Entrar",
    fg_color="#00aa55",       # cor do botão
    hover_color="#8C3B57",    # cor ao passar o mouse
    corner_radius=20          # arredondamento
)

botao.pack(pady=50)

app.mainloop()



CTkButton = button
ctk.Button(app,texto = "ola, mundo", comand=etc)
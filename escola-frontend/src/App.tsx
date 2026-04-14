import React, { useState } from "react";

const API_URL = "https://api-escola-ma08.onrender.com";

type Tela =
  | "inicio"
  | "login"
  | "cadastroUsuario"
  | "menu"
  | "cadastroAluno"
  | "procurarAluno";

  const tituloStyle: React.CSSProperties = {color: "white",marginBottom: 20,};

type Aluno = {
  nome: string;
  nota: number;
};

export default function App() {
  const [tela, setTela] = useState<Tela>("inicio");
  const [mensagem, setMensagem] = useState("");

  const [loginNome, setLoginNome] = useState("");
  const [loginEmail, setLoginEmail] = useState("");
  const [loginSenha, setLoginSenha] = useState("");

  const [cadastroNome, setCadastroNome] = useState("");
  const [cadastroEmail, setCadastroEmail] = useState("");
  const [cadastroSenha, setCadastroSenha] = useState("");

  const [alunoNome, setAlunoNome] = useState("");
  const [alunoNota, setAlunoNota] = useState("");

  const [buscaNome, setBuscaNome] = useState("");
  const [resultados, setResultados] = useState<Aluno[]>([]);

  function limparMensagem() {
    setMensagem("");
  }

  function irPara(novaTela: Tela) {
    limparMensagem();
    setResultados([]);
    setTela(novaTela);
  }

  async function cadastrarUsuario() {
    const nome = cadastroNome.trim();
    const email = cadastroEmail.trim();
    const senha = cadastroSenha.trim();

    if (!nome || !email || !senha) {
      setMensagem("Preencha nome, e-mail e senha!");
      return;
    }

    try {
      const resposta = await fetch(`${API_URL}/usuarios`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ nome, email, senha }),
      });

      const dados = await resposta.json();

      if (resposta.ok) {
        setMensagem("Usuário cadastrado com sucesso!");
      } else {
        setMensagem(dados.erro || "Erro ao cadastrar usuário.");
      }
    } catch {
      setMensagem("Erro ao conectar com a API!");
    }
  }

  async function login() {
    const nome = loginNome.trim();
    const email = loginEmail.trim();
    const senha = loginSenha.trim();

    if (!nome || !email || !senha) {
      setMensagem("Preencha nome, e-mail e senha!");
      return;
    }

    try {
      const resposta = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ nome, email, senha }),
      });

      const dados = await resposta.json();

      if (resposta.ok && !dados.erro) {
        setMensagem("");
        setTela("menu");
      } else {
        setMensagem(dados.erro || "Nome, e-mail ou senha inválidos.");
      }
    } catch {
      setMensagem("Erro ao conectar com a API!");
    }
  }

  async function salvarAluno() {
    const nome = alunoNome.trim();
    const notaTexto = alunoNota.trim();

    if (!nome) {
      setMensagem("Digite o nome do aluno!");
      return;
    }

    const nota = Number(notaTexto);

    if (Number.isNaN(nota)) {
      setMensagem("Digite uma nota válida!");
      return;
    }

    try {
      const resposta = await fetch(`${API_URL}/alunos`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ nome, nota }),
      });

      const dados = await resposta.json();

      if (resposta.ok) {
        setMensagem("Aluno cadastrado com sucesso!");
      } else {
        setMensagem(dados.erro || "Erro ao cadastrar aluno.");
      }
    } catch {
      setMensagem("Erro ao conectar com a API!");
    }
  }

  async function procurarAluno() {
    const nomeDigitado = buscaNome.trim();

    if (!nomeDigitado) {
      setMensagem("Digite um nome para pesquisar!");
      return;
    }

    try {
      const resposta = await fetch(
        `${API_URL}/alunos/buscar?nome=${encodeURIComponent(nomeDigitado)}`
      );

      const dados = await resposta.json();

      if (Array.isArray(dados) && dados.length > 0) {
        setResultados(dados);
        setMensagem("Resultados encontrados");
      } else {
        setResultados([]);
        setMensagem("Aluno não encontrado!");
      }
    } catch {
      setMensagem("Erro ao conectar com a API!");
    }
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#1a1a1a",
        color: "white",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        fontFamily: "Arial, sans-serif",
        padding: 20,
      }}
    >
      <div
        style={{
          width: 500,
          backgroundColor: "#2b2b2b",
          padding: 30,
          borderRadius: 12,
          boxShadow: "0 0 10px rgba(0,0,0,0.4)",
        }}
      >
        {tela === "inicio" && (
          <>
            <h1 style={tituloStyle}>Já tem uma conta?</h1>
            <button onClick={() => irPara("login")} style={botaoStyle}>
              Fazer login
            </button>
            <button onClick={() => irPara("cadastroUsuario")} style={botaoStyle}>
              Entrar
            </button>
          </>
        )}

        {tela === "login" && (
          <>
            <h1 style={tituloStyle}>Entrar</h1>

            <label>Digite seu e-mail:</label>
            <input
              style={inputStyle}
              value={loginEmail}
              onChange={(e) => setLoginEmail(e.target.value)}
            />

            <label>Digite seu nome:</label>
            <input
              style={inputStyle}
              value={loginNome}
              onChange={(e) => setLoginNome(e.target.value)}
            />

            <label>Digite sua senha:</label>
            <input
              style={inputStyle}
              type="password"
              value={loginSenha}
              onChange={(e) => setLoginSenha(e.target.value)}
            />

            <button onClick={login} style={botaoStyle}>
              Entrar
            </button>
            <button onClick={() => irPara("inicio")} style={botaoStyle}>
              Voltar
            </button>
          </>
        )}

        {tela === "cadastroUsuario" && (
          <>
            <h1 style={tituloStyle}>Cadastro</h1>

            <label>Digite seu nome:</label>
            <input
              style={inputStyle}
              value={cadastroNome}
              onChange={(e) => setCadastroNome(e.target.value)}
            />

            <label>Digite seu e-mail:</label>
            <input
              style={inputStyle}
              value={cadastroEmail}
              onChange={(e) => setCadastroEmail(e.target.value)}
            />

            <label>Digite sua senha:</label>
            <input
              style={inputStyle}
              type="password"
              value={cadastroSenha}
              onChange={(e) => setCadastroSenha(e.target.value)}
            />

            <button onClick={cadastrarUsuario} style={botaoStyle}>
              Cadastrar
            </button>
            <button onClick={() => irPara("inicio")} style={botaoStyle}>
              Voltar
            </button>
          </>
        )}

        {tela === "menu" && (
          <>
            <h1>O que deseja fazer?</h1>

            <button onClick={() => irPara("cadastroAluno")} style={botaoStyle}>
              Cadastrar aluno
            </button>
            <button onClick={() => irPara("procurarAluno")} style={botaoStyle}>
              Procurar aluno
            </button>
            <button onClick={() => irPara("inicio")} style={botaoStyle}>
              Sair
            </button>
          </>
        )}

        {tela === "cadastroAluno" && (
          <>
            <h1>Cadastro</h1>

            <label>Nome do aluno:</label>
            <input
              style={inputStyle}
              value={alunoNome}
              onChange={(e) => setAlunoNome(e.target.value)}
            />

            <label>Nota do aluno:</label>
            <input
              style={inputStyle}
              value={alunoNota}
              onChange={(e) => setAlunoNota(e.target.value)}
            />

            <button onClick={salvarAluno} style={botaoStyle}>
              Cadastrar aluno
            </button>
            <button onClick={() => irPara("menu")} style={botaoStyle}>
              Voltar
            </button>
          </>
        )}

        {tela === "procurarAluno" && (
          <>
            <h1>Procurar Aluno</h1>

            <label>Nome do aluno:</label>
            <input
              style={inputStyle}
              value={buscaNome}
              onChange={(e) => setBuscaNome(e.target.value)}
            />

            <button onClick={procurarAluno} style={botaoStyle}>
              Procurar aluno
            </button>
            <button onClick={() => irPara("menu")} style={botaoStyle}>
              Voltar
            </button>

            {resultados.length > 0 && (
              <div style={{ marginTop: 20 }}>
                {resultados.map((aluno, index) => (
                  <div key={index} style={{ marginBottom: 10 }}>
                    {aluno.nome} - Nota: {aluno.nota}
                  </div>
                ))}
              </div>
            )}
          </>
        )}

        {mensagem && (
          <p style={{ marginTop: 20, color: "#ffcc00", fontWeight: "bold" }}>
            {mensagem}
          </p>
        )}
      </div>
    </div>
  );}

const inputStyle: React.CSSProperties = {width: "100%",padding: "10px",marginTop: 6,marginBottom: 16,borderRadius: 8,border: "1px solid #555",backgroundColor: "#3a3a3a",color: "white",boxSizing: "border-box",};

const botaoStyle: React.CSSProperties = {width: "100%",padding: "12px",marginTop: 10,border: "none",borderRadius: 8,backgroundColor: "#1f6aa5",color: "white",cursor: "pointer",fontSize: 16,};
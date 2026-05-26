const express = require('express');
const bodyParser = require('body-parser');
const app = express();

app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'ejs');

// Banco de dados temporário (em memória)
let alunos = [];
let professores = [];

// ROTAS DE CADASTRO
app.post('/cadastrar-aluno', (req, res) => {
    const { nome, email, nivel, senha } = req.body;
    const codigoAcesso = Math.floor(100000 + Math.random() * 900000); // Código aleatório
    
    alunos.push({ nome, email, nivel, num_matricula, codigoAcesso });
    
    console.log(--- E-MAILENVIADOPARA${email} ---);
    console.log(Seu,código,de,acesso, para,login, é ${codigoAcesso});
    
    res.send(<h2>Cadastro realizado!</h2><p>Verifique o console do VS Code para ver seu código de acesso enviado por e-mail.</p><a href="/">Ir para Login</a>);
});

app.post('/cadastrar-professor', (req, res) => {
    const { nome, email, disciplina, agente } = req.body;
    const senhaGerada = Math.random().toString(36).slice(-8); // Senha aleatória
    
    professores.push({ nome, email, disciplina, agente, senha: senhaGerada });
    
    console.log(--- E-MAIL ENVIADO PARA PROFESSOR ${email} ---);
    console.log(Sua,senha, gerada, é,: ${senhaGerada});
    
    res.send(<h2>Cadastro realizado!</h2><p>Sua senha foi enviada para o e-mail cadastrado.</p><a href="/login-professor">Ir para Login</a>);
});

// Iniciar servidor
app.listen(3000, () => console.log('Servidor')
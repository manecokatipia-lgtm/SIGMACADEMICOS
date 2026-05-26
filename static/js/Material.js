document.getElementById('materialForm').addEventListener('submit', function(e) {
    e.preventDefault();

    // Capturando os valores
    const nome = document.getElementById('nome').value;
    const turma = document.getElementById('turma').value;
    const materialId = document.getElementById('materialId').value;
    const categoria = document.getElementById('categoria').value;

    adicionarNaTabela(nome, turma, materialId, categoria);

    // Limpar o formulário
    this.reset();
});

function adicionarNaTabela(nome, turma, id, categoria) {
    const lista = document.getElementById('listaMateriais');
    const linha = document.createElement('tr');

    linha.innerHTML = `
        <td>${id}</td>
        <td>${nome}</td>
        <td>${turma}</td>
        <td><strong>${categoria}</strong></td>
        <td><button class="btn-delete" onclick="removerLinha(this)">Excluir</button></td>
    `;

    lista.appendChild(linha);
}

function removerLinha(botao) {
    if (confirm('Deseja remover este material?')) {
        botao.parentElement.parentElement.remove();
    }
}


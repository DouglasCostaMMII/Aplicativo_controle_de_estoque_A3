
// Botões que acionam modals
var modals = document.querySelectorAll('.modal');
var btnAdd = document.getElementById("add_categoria");
var btnEditar = document.getElementById("editar_categoria");
var btnDeletar = document.getElementById("inativar_categoria");
var btnCancelar = document.querySelectorAll('.btn-cancelar');

// Função para carregar mensagens ao usuário sobre as operações realizadas
window.onload = function () {
    const resultadoOk = document.getElementById('resultado_ok');
    const resultatoErro = document.getElementById('resultado_erro');
    const resultadoSemDados = document.getElementById('campos_Npreenchidos');
    const modal = document.getElementById('mensagem_resultado');

    // Verifica se existe uma mensagem de erro
    if (resultatoErro && resultatoErro.innerText.trim() !== '') {
        modal.style.display = 'block'; // Mostra o modal
        resultatoErro.style.display = 'block'; // Mostra a mensagem de erro
        // Redireciona após 3 segundos
        setTimeout(() => {
            window.location.href = "/categorias"; 
        }, 3000);
    }
    // Verifica se existe uma mensagem de sucesso
    else if (resultadoOk && resultadoOk.innerText.trim() !== '') {
        modal.style.display = 'block'; // Mostra o modal
        resultadoOk.style.display = 'block'; // Mostra a mensagem de sucesso
        // Redireciona após 3 segundos
        setTimeout(() => {
            window.location.href = "/categorias"; 
        }, 3000);
    }
    // Verifica se existe uma mensagem de sem dados
    else if (resultadoSemDados && resultadoSemDados.innerText.trim() !== '') {
        modal.style.display = 'block'; // Mostra o modal
        resultadoSemDados.style.display = 'block'; // Mostra a mensagem de sucesso
        // Redireciona após 3 segundos
        setTimeout(() => {
            window.location.href = "/categorias"; 
        }, 3000);
    }
};

// Função para selecionar linha da tabela    
var selectedRow = null;
document.getElementById("add_categoria").style.cursor = "pointer";
document.getElementById("editar_categoria").style.backgroundColor = "#a5a5a5";
document.getElementById("editar_categoria").style.cursor = "normal";
document.getElementById("inativar_categoria").style.backgroundColor = "#a5a5a5";
document.getElementById("inativar_categoria").style.cursor = "nomral";
document.getElementById('tabela-categorias').addEventListener('click', function (e) {
    var target = e.target;
    while (target && target.nodeName !== 'TR') {
        target = target.parentNode;
    }
    if (target && target.nodeName === 'TR') {
        if (selectedRow) {
            selectedRow.classList.remove('selected');
        }
        selectedRow = target;
        selectedRow.classList.add('selected');
        document.getElementById("editar_categoria").style.backgroundColor = "#ffffff";
        document.getElementById("editar_categoria").style.cursor = "pointer";
        document.getElementById("inativar_categoria").style.backgroundColor = "#ffffff";
        document.getElementById("inativar_categoria").style.cursor = "pointer";
    }
});

// Função para abrir Modal
function openModal(modalId) {
    var modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
    } else {
        console.error('Modal não encontrado: ' + modalId);
    }
}

// Função para fechar Modal
function closeModal(modal) {
    modal.style.display = "none";
    if (!(errorMessage && errorMessage.innerText.trim() == '') &&
        !(resultadoOk && resultadoOk.innerText.trim() == '')) {
        location.reload();
    }
}

// Função para fechar modais ao abrir a tela
modals.forEach(function (modal) {
    btnCancelar.onclick = function () {
        closeModal(modal);
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            closeModal(modal);
        }
    }
});

// Funções acioadas pelos botões:
// Adicionar produto
btnAdd.onclick = function () {
    openModal('adicionar_categoria');
}

// Editar produto
btnEditar.onclick = function () {
    if (selectedRow) {
        var categoriaid = selectedRow.children[0].textContent;
        var nome = selectedRow.children[1].children[0].textContent.trim();

        document.getElementById('editar-categoriaid').value = categoriaid;
        document.getElementById('editar-nome').value = nome;

        openModal('editar-categoria');
    } else {
        document.getElementById("nada_selecionado").style.display = 'block';
        openModal('mensagem_resultado')
    }
}

// Alterar status
btnDeletar.onclick = function () {
    if (selectedRow) {
        var categoriaid = selectedRow.children[0].textContent;
        document.getElementById('alterar_Status_selecionado').value = categoriaid;
        var nome = selectedRow.children[1].children[0].textContent.trim();
        document.getElementById('nomeCategoria').textContent = nome;
        var statusAtual = selectedRow.children[2].textContent.trim();
        var statusNovo = document.getElementById('statusNovo');
        if (statusAtual === "ATIVO") {
            statusNovo.textContent = 'Inativo'
        } else {
            statusNovo.textContent = 'Ativo'
        }
        openModal('alterar_Status');
    } else {
        document.getElementById("nada_selecionado").style.display = 'block';
        openModal('mensagem_resultado')
    }
}

// Função para filtrar a tabela conforme aquilo que for pesquisado
document.addEventListener("DOMContentLoaded", function () {
    // Captura os campos de pesquisa
    const categoriaIdInput = document.querySelector('#pesquisaCategoriaID');
    const categoriaNomeInput = document.querySelector('#pesquisaNome');
    const categoriaStatusInput = document.querySelector('#pesquisaStatus');

    // Captura a tabela, linhas da tabela e a mensagem de "nenhum item encontrado"
    const tabelaCategorias = document.querySelector('#tabela-categorias');
    const linhasCategorias = tabelaCategorias.querySelectorAll('tr');
    const noResultsMessage = document.querySelector('#no-results-message');
    // Função para filtrar as categorias
    function filtrarTabela() {
        const categoriaIdValue = categoriaIdInput.value.toLowerCase();
        const categoriaNomeValue = categoriaNomeInput.value.toLowerCase();
        const categoriaStatusValue = categoriaStatusInput.value.toLowerCase();

        let algumaCategoriaEncontrada = false; // Variável para verificar se encontra categorias

        // Percorre as linhas da tabela (ignora o cabeçalho)
        linhasCategorias.forEach(linha => {
            const colunas = linha.querySelectorAll('td');
            // Se houver colunas (linha não for cabeçalho)
            if (colunas.length > 0) {
                const CategoriaId = colunas[0].textContent.toLowerCase();
                const nomeCategoria = colunas[1].textContent.toLowerCase();
                const statusCategoria = colunas[2].textContent.toLowerCase().trim();

                // Verifica se todos os filtros correspondem
                const correspondeCategoriaId = categoriaIdValue === '' || CategoriaId.includes(categoriaIdValue);
                const correspondeCategoriaNome = categoriaNomeValue === '' || nomeCategoria.includes(categoriaNomeValue);

                // Lógica de status: verifica se começa com "a" ou "i"
                let correspondeStatus = false;
                if (categoriaStatusValue.startsWith("a")) {
                    correspondeStatus = statusCategoria === "ativo";
                } else if (categoriaStatusValue.startsWith("i")) {
                    correspondeStatus = statusCategoria === "inativo";
                } else if (categoriaStatusValue === '') {
                    correspondeStatus = true; // Se o campo de pesquisa estiver vazio, mostra todos os status
                }
                // Exibe ou esconde a linha com base no filtro
                if (correspondeCategoriaId && correspondeCategoriaNome && correspondeStatus) {
                    linha.style.display = ''; // Exibe a linha
                    algumaCategoriaEncontrada = true; // Encontrou pelo menos uma categoria
                } else {
                    linha.style.display = 'none'; // Esconde a linha
                }
            }
        });

        // Se nenhuma categoria foi encontrada, exibe a mensagem
        if (algumaCategoriaEncontrada) {
            noResultsMessage.style.display = 'none'; // Esconde a mensagem
        } else {
            noResultsMessage.style.display = 'block'; // Exibe a mensagem
        }
    }

    // Adiciona o evento de input diretamente aos campos de pesquisa
    categoriaIdInput.addEventListener('input', filtrarTabela);
    categoriaNomeInput.addEventListener('input', filtrarTabela);
    categoriaStatusInput.addEventListener('input', filtrarTabela);
});

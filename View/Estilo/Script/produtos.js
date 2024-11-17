// Botões que acionam modals
var modals = document.querySelectorAll('.modal');
var btnAdd = document.getElementById("add-produto");
var btnEditar = document.getElementById("editar-produto");
var btnMovimentar = document.getElementById("movimentar-produto");
var btnAlterarStatus = document.getElementById("alterarStatus-produto");
var btnCancelar = document.querySelectorAll('.btn-cancelar');

// Função para carregar mensagens ao usuário sobre as operações realizadas
window.onload = function () {
    const resultadoOk = document.getElementById('resultado_ok');
    const resultatoErro = document.getElementById('resultado_erro');
    const resultadoErroQnt = document.getElementById('quantidade_negativa');
    const resultadoSemDados = document.getElementById('campos_Npreenchidos');
    const modal = document.getElementById('mensagem_resultado');


    // Verifica se existe uma mensagem de erro
    if (resultatoErro && resultatoErro.innerText.trim() !== '') {
        modal.style.display = 'block'; // Mostra o modal
        resultatoErro.style.display = 'block'; // Mostra a mensagem de erro
        // Redireciona após 3 segundos
        setTimeout(() => {
            window.location.href = "/produtos"; // Altere para a URL desejada
        }, 3000);
    }
    // Verifica se existe uma mensagem de sucesso
    else if (resultadoOk && resultadoOk.innerText.trim() !== '') {
        modal.style.display = 'block'; // Mostra o modal
        resultadoOk.style.display = 'block'; // Mostra a mensagem de sucesso
        // Redireciona após 3 segundos
        setTimeout(() => {
            window.location.href = "/produtos"; // Altere para a URL desejada
        }, 3000);
    }
    // Verifica se existe uma mensagem de sem dados
    else if (resultadoSemDados && resultadoSemDados.innerText.trim() !== '') {
        modal.style.display = 'block'; // Mostra o modal
        resultadoSemDados.style.display = 'block'; // Mostra a mensagem de sucesso
        // Redireciona após 3 segundos
        setTimeout(() => {
            window.location.href = "/produtos"; // Altere para a URL desejada
        }, 3000);
    }
    // Verifica se existe uma mensagem de erro gerado por quantidade negativa
    else if (resultadoErroQnt && resultadoErroQnt.innerText.trim() !== '') {
        modal.style.display = 'block'; // Mostra o modal
        resultadoErroQnt.style.display = 'block'; // Mostra a mensagem de sucesso
        // Redireciona após 3 segundos
        setTimeout(() => {
            window.location.href = "/produtos"; // Altere para a URL desejada
        }, 3000);
    }
};

// Função para acionar alerta de estoque baixo
// Seleciona todas as linhas da tabela, exceto o cabeçalho
let linhas = document.querySelectorAll('#tabela-produtos tbody tr');
// Verifica se existem linhas
if (linhas.length !== 0) {
    linhas.forEach(linha => {
        // Seleciona as células da linha e faz verificações de existência
        let quantidadeElement = linha.children[1]?.querySelector('b i');
        let quantidadeMinimaElement = linha.children[5];
        let alerta = linha.querySelector('#alerta_hidden');

        if (quantidadeElement && quantidadeMinimaElement && alerta) {
            let quantidade = parseInt(quantidadeElement.textContent);
            let quantidadeMinima = parseInt(quantidadeMinimaElement.textContent);
            // Verifica se a quantidade está abaixo da quantidade mínima
            if (quantidade < quantidadeMinima) {
                // Exibe o alerta se a quantidade estiver baixa
                alerta.style.display = 'block';
            } else {
                // Garante que o alerta esteja oculto caso contrário
                alerta.style.display = 'none';
            }
        }
    });
}

// Função para selecionar linha da tabela    
var selectedRow = null;
document.getElementById("add-produto").style.cursor = "pointer";
document.getElementById("editar-produto").style.backgroundColor = "#a5a5a5";
document.getElementById("editar-produto").style.cursor = "normal";
document.getElementById("movimentar-produto").style.backgroundColor = "#a5a5a5";
document.getElementById("movimentar-produto").style.cursor = "nomral";
document.getElementById("alterarStatus-produto").style.backgroundColor = "#a5a5a5";
document.getElementById("alterarStatus-produto").style.cursor = "nomral";
document.getElementById('tabela-produtos').addEventListener('click', function (e) {
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
        document.getElementById("editar-produto").style.backgroundColor = "#ffffff";
        document.getElementById("editar-produto").style.cursor = "pointer";
        document.getElementById("movimentar-produto").style.backgroundColor = "#ffffff";
        document.getElementById("movimentar-produto").style.cursor = "pointer";
        document.getElementById("alterarStatus-produto").style.backgroundColor = "#ffffff";
        document.getElementById("alterarStatus-produto").style.cursor = "pointer";
    }
});

// Função para fechar Modal
function closeModal(modal) {
    modal.style.display = "none";
    if (!(errorMessage && errorMessage.innerText.trim() == '') &&
        !(resultadoOk && resultadoOk.innerText.trim() == '')) {
        location.reload();
    }
}

// Função para abrir Modal
function openModal(modalId) {
    var modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
    } else {
        console.error('Modal não encontrado: ' + modalId);
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
    openModal('adicionar_produto');
}
// Editar produto
btnEditar.onclick = function () {
    if (selectedRow) {
        var produtoid = selectedRow.children[0].textContent;
        var nome = selectedRow.children[1].children[0].textContent.trim();
        var categoria = selectedRow.children[2].textContent.trim(); 
        var preco = selectedRow.children[4].textContent;
        var quantidade = selectedRow.children[5].textContent;

        document.getElementById('editar-produtoid').value = produtoid;
        document.getElementById('editar-nome').value = nome;
        document.getElementById('editar-categoria').value = categoria;
        document.getElementById('editar-qnt_min').value = quantidade;
        document.getElementById('editar-preco').value = preco;

        openModal('editar_produto');
    } else {
        document.getElementById("nada_selecionado").style.display = 'block';
        openModal('mensagem_resultado')
    }
}
// Mover produto
btnMovimentar.onclick = function() {
    if (selectedRow) {
        var produtoid = selectedRow.children[0].textContent;
        var produtoStatus = selectedRow.children[3].textContent.trim();
        if (produtoStatus === "INATIVO"){                
            document.getElementById("Produto_inativo").style.display = 'block';
            openModal('mensagem_resultado')
        } else {                
            document.getElementById('mover-produtoid').value = produtoid;
            openModal('mover_produto');}
    } else {
        document.getElementById("nada_selecionado").style.display = 'block';
        openModal('mensagem_resultado')
    }
}
// Alterar status
btnAlterarStatus.onclick = function () {
    if (selectedRow) {
        var produtoid = selectedRow.children[0].textContent;
        document.getElementById('alterar_Status_selecionado').value = produtoid;
        var nome = selectedRow.children[1].children[0].textContent.trim();
        document.getElementById('nomeProduto').textContent = nome;
        var statusAtual = selectedRow.children[3].textContent.trim(); 
        var statusNovo = document.getElementById('statusNovo');
        if (statusAtual === "ATIVO") {
            statusNovo.textContent = 'Inativo';
        } else {
            statusNovo.textContent = 'Ativo';
        }

        openModal('alterar_Status');
    } else {
        document.getElementById("nada_selecionado").style.display = 'block';
        openModal('mensagem_resultado');
    }
}

// Função para filtrar a tabela conforme aquilo que for pesquisado
document.addEventListener("DOMContentLoaded", function () {
    // Captura os campos de pesquisa
    const produtoInput = document.querySelector('#pesquisaProdutoID');
    const descricaoInput = document.querySelector('#pesquisaNome');
    const categoriaInput = document.querySelector('#pesquisaCategoria');
    const statusInput = document.querySelector('#pesquisaStatus');

    // Captura a tabela, linhas da tabela e a mensagem de "nenhum produto encontrado"
    const tabelaProdutos = document.querySelector('#tabela-produtos');
    const linhasProdutos = tabelaProdutos.querySelectorAll('tr');
    const noResultsMessage = document.querySelector('#no-results-message');

    // Função para filtrar os produtos
    function filtrarTabela() {
        const produtoValue = produtoInput.value.toLowerCase();
        const descricaoValue = descricaoInput.value.toLowerCase();
        const categoriaValue = categoriaInput.value.toLowerCase();
        const statusValue = statusInput.value.toLowerCase();

        let algumProdutoEncontrado = false; // Variável para verificar se encontramos produtos

        // Percorre as linhas da tabela (ignora o cabeçalho)
        linhasProdutos.forEach(linha => {
            const colunas = linha.querySelectorAll('td');

            // Se houver colunas (linha não for cabeçalho)
            if (colunas.length > 0) {
                const produtoId = colunas[0].textContent.toLowerCase();
                const nomeProduto = colunas[1].textContent.toLowerCase();
                const categoria = colunas[2].textContent.toLowerCase();
                const status = colunas[3].textContent.toLowerCase();

                // Verifica se todos os filtros correspondem
                const correspondeProduto = produtoValue === '' || produtoId.includes(produtoValue);
                const correspondeDescricao = descricaoValue === '' || nomeProduto.includes(descricaoValue);
                const correspondeCategoria = categoria.includes(categoriaValue);

                // Lógica de status: verifica se começa com "a" ou "i"
                let correspondeStatus = false;
                if (statusValue.startsWith("a")) {
                    correspondeStatus = status === "ativo";
                } else if (statusValue.startsWith("i")) {
                    correspondeStatus = status === "inativo";
                } else if (statusValue === '') {
                    correspondeStatus = true; // Se o campo de pesquisa estiver vazio, mostra todos os status
                }

                // Exibe ou esconde a linha com base no filtro
                if (correspondeProduto && correspondeDescricao && correspondeCategoria && correspondeStatus) {
                    linha.style.display = ''; // Exibe a linha
                    algumProdutoEncontrado = true; // Encontrou pelo menos um produto
                } else {
                    linha.style.display = 'none'; // Esconde a linha
                }
            }
        });

        // Se nenhum produto foi encontrado, exibe a mensagem
        if (algumProdutoEncontrado) {
            noResultsMessage.style.display = 'none'; // Esconde a mensagem
        } else {
            noResultsMessage.style.display = 'block'; // Exibe a mensagem
        }
    }

    // Adiciona o evento de input diretamente aos campos de pesquisa
    produtoInput.addEventListener('input', filtrarTabela);
    descricaoInput.addEventListener('input', filtrarTabela);
    categoriaInput.addEventListener('input', filtrarTabela);
    statusInput.addEventListener('input', filtrarTabela);
});

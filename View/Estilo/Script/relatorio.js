// Seleciona elementos de entrada de pesquisa
let dataInicialInput = document.querySelector('#pesquisa_DataInicial input');
let dataFinalInput = document.querySelector('#pesquisa_DataFinal input');
let categoriaInput = document.querySelector('#pesquisa_SeletorCategoria input');
let produtoInput = document.querySelector('#pesquisa_SeletorProduto input');
let idInput = document.querySelector('#pesquisa_SeletorID input');
let radioMaior = document.querySelector('#pesquisa_RadioMaiorSaida input');
let radioMenor = document.querySelector('#pesquisa_RadioMenorSaida input');

// Seleciona as linhas da tabela
let linhasTabela = document.querySelectorAll('#tabela-categorias tbody tr');

// Adiciona eventos de input nos campos de pesquisa
[dataInicialInput, dataFinalInput, categoriaInput, produtoInput, idInput, radioMaior, radioMenor].forEach(input => {
    input.addEventListener('input', filtrarTabela);
});

// Função de filtragem
function filtrarTabela() {
    let dataInicialInput = document.querySelector('#pesquisa_DataInicial input');
    let dataFinalInput = document.querySelector('#pesquisa_DataFinal input');
    let categoriaInput = document.querySelector('#pesquisa_SeletorCategoria input');
    let produtoInput = document.querySelector('#pesquisa_SeletorProduto input');
    let idInput = document.querySelector('#pesquisa_SeletorID input');
    let radioMaior = document.querySelector('#maior');
    let radioMenor = document.querySelector('#menor');
    let linhasTabela = document.querySelectorAll('#tabela-categorias tbody tr');
    let noResultsMessage = document.querySelector('#no-results-message'); // Elemento para mensagem de "nenhum resultado encontrado"

    let dataInicial = dataInicialInput.value ? new Date(dataInicialInput.value) : null;
    let dataFinal = dataFinalInput.value ? new Date(dataFinalInput.value) : null;
    let categoria = categoriaInput.value.toLowerCase();
    let produto = produtoInput.value.toLowerCase();
    let id = idInput.value.toLowerCase();

    let algumProdutoEncontrado = false;

    linhasTabela.forEach(linha => {
        let dataText = linha.querySelector('td:nth-child(5) p').textContent; // Coluna de data
        let dataLinha = new Date(dataText.split('/').reverse().join('-')); // Formato dia/mês/ano para ano-mês-dia
        let categoriaLinha = linha.querySelector('td:nth-child(3) p').textContent.toLowerCase();
        let produtoLinha = linha.querySelector('td:nth-child(2) p').textContent.toLowerCase();
        let idLinha = linha.dataset.id.toLowerCase();

        let correspondeCategoria = !categoria || categoriaLinha.includes(categoria);
        let correspondeProduto = !produto || produtoLinha.includes(produto);
        let correspondeId = !id || idLinha.includes(id);
        let correspondeData = true;

        if (dataInicial && dataLinha < dataInicial) correspondeData = false;
        if (dataFinal && dataLinha > dataFinal) correspondeData = false;

        // Exibe ou esconde a linha com base no filtro
        if (correspondeProduto && correspondeCategoria && correspondeId && correspondeData) {
            linha.style.display = ''; // Exibe a linha
            algumProdutoEncontrado = true; // Encontrou pelo menos um produto
        } else {
            linha.style.display = 'none'; // Esconde a linha
        }
    });

    // Exibe ou esconde a mensagem "Nenhum resultado encontrado"
    if (algumProdutoEncontrado) {
        noResultsMessage.style.display = 'none'; // Esconde a mensagem
    } else {
        noResultsMessage.style.display = 'block'; // Exibe a mensagem
    }

    // Ordenação por maior ou menor saída
    if (radioMaior.checked || radioMenor.checked) {
        let linhasArray = Array.from(linhasTabela).filter(linha => linha.style.display !== 'none'); // Somente linhas visíveis
        linhasArray.sort((a, b) => {
            let quantidadeA = parseInt(a.querySelector('td:nth-child(4) p').textContent);
            let quantidadeB = parseInt(b.querySelector('td:nth-child(4) p').textContent);
            return radioMaior.checked ? quantidadeB - quantidadeA : quantidadeA - quantidadeB;
        });

        // Reanexa as linhas ordenadas ao corpo da tabela
        let tbody = document.querySelector('#tabela-categorias tbody');
        linhasArray.forEach(linha => tbody.appendChild(linha));
    }
}

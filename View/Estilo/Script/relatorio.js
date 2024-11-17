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
    let dataInicial = new Date(dataInicialInput.value);
    let dataFinal = new Date(dataFinalInput.value);
    let categoria = categoriaInput.value.toLowerCase();
    let produto = produtoInput.value.toLowerCase();
    let id = idInput.value.toLowerCase();
    
    linhasTabela.forEach(linha => {
        let dataText = linha.querySelector('td:nth-child(5) p').textContent; // Coluna de data
        let dataLinha = new Date(dataText.split('-').reverse().join('-')); // Converte para formato de data (dia-mês-ano)
        let categoriaLinha = linha.querySelector('td:nth-child(3) p').textContent.toLowerCase();
        let produtoLinha = linha.querySelector('td:nth-child(2) p').textContent.toLowerCase();
        let idLinha = linha.dataset.id.toLowerCase();

        let exibirLinha = true;

        // Verifica os filtros de data
        if (dataInicialInput.value && dataLinha < dataInicial) exibirLinha = false;
        if (dataFinalInput.value && dataLinha > dataFinal) exibirLinha = false;

        // Verifica os filtros de categoria, produto e ID
        if (categoria && !categoriaLinha.includes(categoria)) exibirLinha = false;
        if (produto && !produtoLinha.includes(produto)) exibirLinha = false;
        if (id && !idLinha.includes(id)) exibirLinha = false;

        // Exibe ou oculta a linha com base nos critérios
        linha.style.display = exibirLinha ? '' : 'none';
    });

    // Ordenação por maior ou menor saída (opcional)
    if (radioMaior.checked || radioMenor.checked) {
        let linhasArray = Array.from(linhasTabela);
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

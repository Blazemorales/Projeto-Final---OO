document.addEventListener("DOMContentLoaded", function () {
    // As variáveis 'userType', 'itens' e 'lojas' já existem globalmente.

    // Seleciona o novo container onde as listas serão exibidas.
    const listaContainer = document.getElementById('lista-container');

    function showAnimatedMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('animated-message');
        messageDiv.innerText = message;
        document.body.appendChild(messageDiv);
        setTimeout(() => document.body.removeChild(messageDiv), 2000);
    }

    /**
     * Exibe uma lista de itens (lojas ou produtos) no container da página.
     * @param {Array} lista - A lista de itens a ser exibida.
     * @param {string} tipo - O tipo de item (ex: 'loja', 'produto').
     */
    function mostrarItensCadastrados(lista, tipo) {
        // Limpa o conteúdo anterior do container.
        listaContainer.innerHTML = '';

        const container = document.createElement('div');
        container.classList.add('lista-itens');

        if (!lista || lista.length === 0) {
            const vazio = document.createElement('p');
            vazio.innerText = `Nenhum ${tipo} cadastrado.`;
            container.appendChild(vazio);
        } else {
            lista.forEach(item => {
                const itemDiv = document.createElement('div');
                // Lógica flexível: funciona se 'item' for um objeto com a chave 'nome' ou se for uma string.
                itemDiv.textContent = item.nome || item;
                itemDiv.classList.add('item');
                container.appendChild(itemDiv);
            });
        }

        // Adiciona a nova lista ao container dedicado.
        listaContainer.appendChild(container);
    }

    // Exibe a lista inicial de produtos se o usuário for do tipo "comum"
    if (userType === "comum") {
        showAnimatedMessage("Aqui estão os produtos cadastrados:");
        mostrarItensCadastrados(itens, "produto");
    }

    // --- CORREÇÃO PRINCIPAL: Adicionando listeners a TODOS os botões ---

    // Função para exibir lojas
    const exibirLojas = () => {
        showAnimatedMessage('Exibindo lojas cadastradas...');
        mostrarItensCadastrados(lojas, 'loja');
    };

    // Função para exibir produtos
    const exibirProdutos = () => {
        showAnimatedMessage('Exibindo produtos cadastrados...');
        mostrarItensCadastrados(itens, 'produto');
    };

    // Pega todos os botões que devem realizar a mesma ação
    const btnsLojas = [
        document.getElementById('btn-lojas'),
        document.getElementById('btn-lojas-mobile')
    ];
    const btnsProdutos = [
        document.getElementById('btn-produtos'),
        document.getElementById('btn-produtos-mobile')
    ];

    // Adiciona o evento a cada botão encontrado
    btnsLojas.forEach(btn => btn?.addEventListener('click', exibirLojas));
    btnsProdutos.forEach(btn => btn?.addEventListener('click', exibirProdutos));
});
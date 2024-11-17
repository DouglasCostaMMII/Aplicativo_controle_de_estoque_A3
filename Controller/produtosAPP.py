from flask import Blueprint, render_template, request, redirect, url_for
from Model.categoriasDAO import CategoriaDAO
from Model.produtosDAO import ProdutoDAO
from Model.conexaoDAO import ConexaoDAO
from Model.entradaDAO import EntradaDAO
from Model.saidaDAO import SaidaDAO
from datetime import datetime

# Criação do blueprint
produtos_blueprint = Blueprint('produtos', __name__, template_folder='View')

# Criação de objetos que serão utilizados
categoria_Obj = CategoriaDAO()
produtos_Obj = ProdutoDAO()
entrada_Obj = EntradaDAO()
saida_Obj = SaidaDAO()
conexao = ConexaoDAO()

# Função responsável por carregar o template de produtos
@produtos_blueprint.route('/produtos', methods=['GET', 'POST'])
def produtos():
    if conexao.banco_conectado():
        results_produtos = produtos_Obj.visualizar_produtos_DAO()
        results_categoria = categoria_Obj.visualizarCategoriaDAO()
        results_estoque = produtos_Obj.alerta_estoqueBaixoDAO()
        return render_template('produtos.html', produtos=results_produtos, categorias=results_categoria, alerta=results_estoque)
    else:
        return "Erro na conexão com o banco de dados"

# Função para adicionar produtos    
@produtos_blueprint.route('/add_produto', methods=['POST'])
def add_produto():
    nome = request.form.get('nome')
    status = request.form.get('status').upper()
    categoria = request.form.get('categoria')
    preco = request.form.get('preco')
    qnt_min = request.form.get('qnt_min')
    acao = request.form.get('DecisaoAdicionar')
    mensagem_alerta = "Todos os campos são obrigatórios"
    mensagem_erro = "Erro ao cadastrar produto"
    mensagem_alerta_duplicado = "Produto já cadastrado"
    mensagem_erro_categoria="Categoria selecionada não existe"
    mensagem_sucesso = "Produto cadastrado com sucesso"

    if acao == "cancelar":
        return redirect(url_for('produtos.produtos'))
   
    # tradamento de dados
    if "," in preco:
        preco = preco.replace(",", ".")

    if acao == "confirmar" and not (nome and status and categoria and preco and qnt_min):
        return render_template('produtos.html', mensagem_alerta=mensagem_alerta)  # Caso não sejam passados dados
    if acao == "confirmar" and nome in [produto['nome'] for produto in produtos_Obj.visualizar_produtos_DAO()]:
        return render_template('produtos.html', mensagem_alerta=mensagem_alerta_duplicado)  # Nao adicionar itens duplicados
    
    categorias = categoria_Obj.visualizarCategoriaDAO()    
    if any(categoria_return['nome'] == categoria for categoria_return in categorias):
        categoria = categoria_Obj.getCategoriaidDAO(categoria)
    else:
        return render_template('produtos.html', mensagem_erro=mensagem_erro_categoria)  # Caso categoria não exista
   
    if acao == "confirmar" and produtos_Obj.add_produto_DAO(nome, status, categoria, preco, qnt_min, acao)[0]:
        return render_template('produtos.html', mensagem_sucesso=mensagem_sucesso)  # Caso de sucesso no processo
    else:
        return render_template('produtos.html', mensagem_erro=mensagem_erro)  # Caso de erro no processo
   
# Função para editar produtos
@produtos_blueprint.route('/editar_produto', methods=['POST'])
def editar_produto():
    nome = request.form.get('editar-nome')
    status = request.form.get('editar-status').upper()
    categoria = request.form.get('editar-categoria')
    preco = request.form.get('editar-preco')
    qnt_min = request.form.get('editar-qnt_min')
    produtoid = request.form.get('editar-produtoid')
    acao = request.form.get('DecisaoEditar')
    mensagem_alerta = "Todos os campos são obrigatórios"
    mensagem_erro = "Erro ao alterar dados do produto"
    mensagem_sucesso = "Produto alterado com sucesso"

    if acao == "cancelar":
        return redirect(url_for('produtos.produtos'))

    if not (nome and status and categoria and preco and qnt_min) and acao == "confirmar":
        return render_template('produtos.html', mensagem_alerta=mensagem_alerta)  # Caso não sejam passados dados
   
    categorias = categoria_Obj.visualizarCategoriaDAO()    
    if any(categoria_return['nome'] == categoria for categoria_return in categorias):
        categoria = categoria_Obj.getCategoriaidDAO(categoria)
    else:
        return render_template('produtos.html', mensagem_erro="Categoria selecionada não existe")  # Caso categoria não exista
   
    if acao == "confirmar" and produtos_Obj.editar_produto_DAO(nome, status, categoria, preco, qnt_min, produtoid)[0]:
        # tradamento de dados
        if "," in preco:
            preco = preco.replace(",", ".")
        return render_template('produtos.html', mensagem_sucesso=mensagem_sucesso)  # Caso de sucesso no processo
    else:
        return render_template('produtos.html', mensagem_erro=mensagem_erro)  # Caso de erro no processo# tradamento de dados
   
# Função para mover produtos
@produtos_blueprint.route('/mover_produto', methods=['POST'])
def mover_produto():
    produtoid = request.form.get('mover-produtoid')
    tipo_movimentacao = request.form.get('tipo-mover')
    quantidade = request.form.get('quantidade-mover')
    acao = request.form.get('DecisaoMover')
    
    mensagem_alerta = "Informe um valor de entrada ou saída"
    mensagem_erro_quantia = "A quantidade solicitada excede o estoque disponível! selecione outra quantia"
    mensagem_erro_input = "Informe uma quantidade positiva"
    mensagem_erro = "Erro ao alterar a quantidade de estoque"
    mensagem_sucesso = "Quantidade alterada com sucesso"
   
    # Caso operação seja cancelada recarrega a página
    if acao == "cancelar":
            return redirect(url_for('produtos.produtos'))
    if (quantidade == ""):
        return render_template('produtos.html', mensagem_alerta=mensagem_alerta)
    else:
        quantidade = int(quantidade)
    if (quantidade < 0):
        return render_template('produtos.html', mensagem_alerta=mensagem_erro_input)
    elif (quantidade == 0):
        return render_template('produtos.html', mensagem_alerta=mensagem_alerta)
    else:
        if acao == "confirmar":
            quantidade_atual = produtos_Obj.getQuantidadeDAO(produtoid)
            diferenca = quantidade_atual - quantidade

            # Caso subtração seja negativa (ERRO)
            if tipo_movimentacao == "Saida" and (diferenca < 0):
                return render_template('produtos.html', mensagem_erro_quantia=mensagem_erro_quantia)  
            # Caso subtração seja positiva (OK)
            elif tipo_movimentacao == "Saida" and (diferenca >= 0):
                if produtos_Obj.setQuantidadeDAO(produtoid, diferenca):
                    saida_Obj.add_saida_DAO(produtoid, produtos_Obj.getCategoriaDAO(produtoid), quantidade, datetime.now().strftime('%Y-%m-%d'))
                    return render_template('produtos.html', mensagem_sucesso=mensagem_sucesso)  
            # Caso a operação seja de adição
            elif tipo_movimentacao == "Entrada" and produtos_Obj.setQuantidadeDAO(produtoid, (quantidade_atual+ quantidade)):
                entrada_Obj.add_entrada_DAO(produtoid, produtos_Obj.getCategoriaDAO(produtoid), quantidade, datetime.now().strftime('%Y-%m-%d'))
                return render_template('produtos.html', mensagem_sucesso=mensagem_sucesso)  
        else:
            return render_template('produtos.html', mensagem_erro=mensagem_erro)

# Função para alterar o status
@produtos_blueprint.route('/alterar_StatusProduto', methods=['POST'])
def alterar_StatusProduto():
    acao = request.form.get('DecisaoAlterar')
    produtoid = request.form.get('alterar_Status_selecionado')
    mensagem_erro = "Erro ao alterar o status do produto"
    mensagem_sucesso = "Status do produto alterado com sucesso"

    # Caso operação seja cancelada recarrega a página
    if acao == "cancelar":
        return redirect(url_for('produtos.produtos'))
    elif acao == "confirmar":
        opcoesStatus = ["ATIVO", "INATIVO"]
        if produtos_Obj.getStatusDAO(produtoid) == opcoesStatus[0]:
            if produtos_Obj.setStatusDAO(produtoid, opcoesStatus[1]):
                return render_template('produtos.html', mensagem_sucesso=mensagem_sucesso)  
        else:
            if produtos_Obj.setStatusDAO(produtoid, opcoesStatus[0]):
                return render_template('produtos.html', mensagem_sucesso=mensagem_sucesso)  
    else:
        return render_template('produtos.html', mensagem_erro=mensagem_erro)

from flask import Flask, render_template, request, redirect, url_for
from Model.categorias import Categoria
from Model.entradas import Entradas
from Model.saidas import Saidas
from Model.produtos import Produtos
from Controller.conexaoDAO import ConexaoDAO


# Muda o diretório de templates para 'View' e o static para 'Estilo'
app = Flask(__name__, template_folder='View', static_folder='View/Estilo')

# Criação de objetos que serão posteriormente utilizados
categoria_Obj = Categoria()
entrada_Obj = Entradas()
saidas_Obj = Saidas()
produtos_Obj = Produtos()
conexao = ConexaoDAO()

@app.route('/', methods=['GET', 'POST'])
def index():
    show_error = False
    if request.method == 'GET':
        if conexao.banco_conectado():  
            return redirect(url_for('produtos'))    # Tela que será carregada ao inicializar o programa.
        else:
            show_error = True
            return render_template('produtos.html', show_error=show_error)

''' Produtos '''
# Função responsável por carregar o template de produtos:        
@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
    results = None
    if conexao.banco_conectado():
        results = fetch_produtos_data()
        return render_template('produtos.html', produtos=results)
    else:
        return "Erro na conexão com o banco de dados"
# Função para adicionar produtos    
@app.route('/add_produto', methods=['POST'])
def add_produto():
    nome = request.form.get('nome')
    status = request.form.get('status').upper()
    categoria = request.form.get('categoria')
    preco = request.form.get('preco')
    qnt_min = request.form.get('qnt_min')
    acao = request.form.get('DecisaoAdicionar')
    mensagem_alerta = "Todos os campos são obrigatórios"
    mensagem_erro = "Erro ao cadastrar produto"
    mensagem_sucesso = "Produto cadastrado com sucesso"

    if acao == "cancelar":
        return redirect(url_for('produtos'))
   
    # tradamento de dados
    if "," in preco:
        preco = preco.replace(",", ".")

    if not (nome and status and categoria and preco and qnt_min) and acao == "confirmar":
        return render_template('produtos.html', mensagem_alerta=mensagem_alerta)  # Caso não sejam passados dados
   
    categorias = categoria_Obj.visualizarCategoria()    
    if any(categoria_return['nome'] == categoria for categoria_return in categorias):
        categoria = categoria_Obj.getCategoriaid(categoria)
    else:
        return render_template('produtos.html', mensagem_erro="Categoria selecionada não existe")  # Caso categoria não exista
   
    if acao == "confirmar" and produtos_Obj.add_produto(nome, status, categoria, preco, qnt_min, acao)[0]:
        return render_template('produtos.html', mensagem_sucesso=mensagem_sucesso)  # Caso de sucesso no processo
    else:
        return render_template('produtos.html', mensagem_erro=mensagem_erro)  # Caso de erro no processo
   
# Função para editar produtos
@app.route('/editar_produto', methods=['POST'])
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
        return redirect(url_for('produtos'))

    if not (nome and status and categoria and preco and qnt_min) and acao == "confirmar":
        return render_template('produtos.html', mensagem_alerta=mensagem_alerta)  # Caso não sejam passados dados
   
    categorias = categoria_Obj.visualizarCategoria()    
    if any(categoria_return['nome'] == categoria for categoria_return in categorias):
        categoria = categoria_Obj.getCategoriaid(categoria)
    else:
        return render_template('produtos.html', mensagem_erro="Categoria selecionada não existe")  # Caso categoria não exista
   
    if acao == "confirmar" and produtos_Obj.editar_produto(nome, status, categoria, preco, qnt_min, produtoid)[0]:
        # tradamento de dados
        if "," in preco:
            preco = preco.replace(",", ".")
        return render_template('produtos.html', mensagem_sucesso=mensagem_sucesso)  # Caso de sucesso no processo
    else:
        return render_template('produtos.html', mensagem_erro=mensagem_erro)  # Caso de erro no processo# tradamento de dados
   
# Função para mover produtos
@app.route('/mover_produto', methods=['POST'])
def mover_produto():
    produtoid = request.form.get('mover-produtoid')
    tipo_movimentacao = request.form.get('tipo-mover')
    quantidade = int(request.form.get('quantidade-mover'))
    acao = request.form.get('DecisaoMover')
    mensagem_alerta = "Todos os campos são obrigatórios"
    mensagem_erro_quantia = "Quantidade selecionada tornará o estoque negativo! selecione outra quantia"
    mensagem_erro = "Erro ao alterar a quantidade de estoque"
    mensagem_sucesso = "Quantidade alterada com sucesso"
   
    # Caso nem todos os campos estejam preenchidos retorna mensagem de erro ao usuário
    if not (tipo_movimentacao and quantidade ) and acao == "confirmar":
        return render_template('produtos.html', mensagem_alerta=mensagem_alerta)
    # Caso operação seja cancelada recarrega a página
    elif acao == "cancelar":
        return redirect(url_for('produtos'))
   
    elif acao == "confirmar":
        quantidade_atual = produtos_Obj.getQuantidade(produtoid)
        diferenca = quantidade_atual - quantidade

        # Caso subtração seja negativa (ERRO)
        if tipo_movimentacao == "Retirada" and (diferenca < 0):
            return render_template('produtos.html', mensagem_erro_quantia=mensagem_erro_quantia)  
        # Caso subtração seja positiva (OK)
        elif tipo_movimentacao == "Retirada" and (diferenca >= 0):
            if produtos_Obj.setQuantidade(produtoid, diferenca):
                return render_template('produtos.html', mensagem_sucesso=mensagem_sucesso)  
        # Caso a operação seja de adição
        elif tipo_movimentacao == "Adicao" and produtos_Obj.setQuantidade(produtoid, (quantidade_atual+ quantidade)):
                return render_template('produtos.html', mensagem_sucesso=mensagem_sucesso)  
    else:
        return render_template('produtos.html', mensagem_erro=mensagem_erro)

# Função para alterar o status
@app.route('/alterar_StatusProduto', methods=['POST'])
def alterar_StatusProduto():
    acao = request.form.get('DecisaoAlterar')
    produtoid = request.form.get('alterar_StatusProduto_selecionado')
    mensagem_erro = "Erro ao alterar o status do produto"
    mensagem_sucesso = "Status do produto alterado com sucesso"

    # Caso operação seja cancelada recarrega a página
    if acao == "cancelar":
        return redirect(url_for('produtos'))
    elif acao == "confirmar":
        opcoesStatus = ["ATIVO", "INATIVO"]
        if produtos_Obj.getStatus(produtoid) == opcoesStatus[0]:
            if produtos_Obj.setStatus(produtoid, opcoesStatus[1]):
                return render_template('produtos.html', mensagem_sucesso=mensagem_sucesso)  
        else:
            if produtos_Obj.setStatus(produtoid, opcoesStatus[0]):
                return render_template('produtos.html', mensagem_sucesso=mensagem_sucesso)  
    else:
        return render_template('produtos.html', mensagem_erro=mensagem_erro)

''' Categorias '''
# Função responsável por carregar o template de categorias:      
@app.route('/categorias', methods=['GET', 'POST'])
def categorias():
    results = categoria_Obj.visualizarCategoria()
    if conexao.banco_conectado():
        return render_template('categorias.html', categorias=results)
    else:
        return "Erro na conexão com o banco de dados"

@app.route('/add_categoria', methods=['POST'])
def add_categoria():
    nome = request.form.get('nome')
    status = request.form.get('status').upper()
    acao = request.form.get('DecisaoAdicionar')
    mensagem_alerta = "Todos os campos são obrigatórios"
    mensagem_erro = "Erro ao cadastrar categoria"
    mensagem_sucesso = "Categoria cadastrada com sucesso"

    if acao == "cancelar":
        return redirect(url_for('categorias'))
   
    # tradamento de dados
    if not (nome and status) and acao == "confirmar":
        return render_template('categorias.html', mensagem_alerta=mensagem_alerta)  # Caso não sejam passados dados

    elif acao == "confirmar" and categoria_Obj.add_Categoria(nome, status)[0]:
        return render_template('categorias.html', mensagem_sucesso=mensagem_sucesso)  # Caso de sucesso no processo
    else:
        return render_template('categorias.html', mensagem_erro=mensagem_erro)  # Caso de erro no processo

# Função para editar categoria
@app.route('/editar_categoria', methods=['POST'])
def editar_categoria():
    nome = request.form.get('editar-nome')
    status = request.form.get('editar-status').upper()
    categoriaid = request.form.get('editar-categoriaid')
    acao = request.form.get('DecisaoEditar')
    mensagem_alerta = "Todos os campos são obrigatórios"
    mensagem_erro = "Erro ao alterar dados da categoria"
    mensagem_sucesso = "Categoria alterada com sucesso"

    if acao == "cancelar":
        return redirect(url_for('categorias'))

    if not (nome and status) and acao == "confirmar":
        return render_template('categorias.html', mensagem_alerta=mensagem_alerta)  # Caso não sejam passados dados
    elif acao == "confirmar" and categoria_Obj.editar_categoria(nome, status, categoriaid)[0]:
        return render_template('categorias.html', mensagem_sucesso=mensagem_sucesso)  # Caso de sucesso no processo
    else:
        return render_template('categorias.html', mensagem_erro=mensagem_erro)  # Caso de erro no processo# tradamento de dados
   
# Função para alterar o status categoria
@app.route('/alterar_StatusCategoria', methods=['POST'])
def alterar_StatusCategoria():
    acao = request.form.get('DecisaoAlterar')
    Categoriaid = request.form.get('alterar_StatusCategoria_selecionada')
    mensagem_erro = "Erro ao alterar o status da categoria"
    mensagem_sucesso = "Status da categoria alterado com sucesso"

    # Caso operação seja cancelada recarrega a página
    if acao == "cancelar":
        return redirect(url_for('categorias'))
    elif acao == "confirmar":
        opcoesStatus = ["ATIVO", "INATIVO"]
        if categoria_Obj.getStatus(Categoriaid) == opcoesStatus[0]:
            if categoria_Obj.setStatus(Categoriaid, opcoesStatus[1]):
                return render_template('categorias.html', mensagem_sucesso=mensagem_sucesso)  
        else:
            if categoria_Obj.setStatus(Categoriaid, opcoesStatus[0]):
                return render_template('categorias.html', mensagem_sucesso=mensagem_sucesso)  
    else:
        return render_template('categorias.html', mensagem_erro=mensagem_erro)

# Função responsável por carregar o template de relatórios:      
@app.route('/relatorios', methods=['GET', 'POST'])
def relatorios():
    results = None
    if conexao.banco_conectado():
        results = ""
        return render_template('relatorios.html', envios=results)
    else:
        return "Erro na conexão com o banco de dados"

def fetch_produtos_data():
    results = produtos_Obj.visualizar_produtos()
    # Atualizando o dicionário com o nome correspondente ao ID do cliente
    for obj in results:
        if 'categoria_id' in obj:
            obj['categoria_id'] = categoria_Obj.getNome(obj['categoria_id'])
    return results

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

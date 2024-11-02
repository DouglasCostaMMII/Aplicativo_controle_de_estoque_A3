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
        results = produtos_Obj.visualizar_produtos()
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
    acao = request.form.get('acao')
    mensagem_alerta = "Todos os campos são obrigatórios"
    mensagem_erro = "Erro ao cadastrar produto"
    mensagem_sucesso = "Produto cadastrado com sucesso"

    if acao == "cancelar":
        return redirect(url_for('produtos'))

    if not (nome and status and categoria and preco and qnt_min) and acao == "confirmar":
        return render_template('produtos.html', mensagem_alerta=mensagem_alerta)  # Caso não sejam passados dados
    
    categorias = categoria_Obj.visualizar_Categoria()  
    if any(categoria_return['nome'] == categoria for categoria_return in categorias):
        categoria = categoria_Obj.getCategoriaid(categoria)
    else:
        return render_template('produtos.html', error_message="Categoria selecionada não existe")  # Caso categoria não exista
    
    if acao == "confirmar" and produtos_Obj.add_produto(nome, status, categoria, preco, qnt_min, acao)[0]:
        # tradamento de dados
        if "," in preco:
            preco = preco.replace(",", ".")
        return render_template('produtos.html', mensagem_sucesso=mensagem_sucesso)  # Caso de sucesso no processo
    else:
        return render_template('produtos.html', error_message=mensagem_erro)  # Caso de erro no processo
    
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
        return render_template('produtos.html', error_message="Categoria selecionada não existe")  # Caso categoria não exista
    
    if acao == "confirmar" and produtos_Obj.editar_produto(nome, status, categoria, preco, qnt_min, produtoid)[0]:
        # tradamento de dados
        if "," in preco:
            preco = preco.replace(",", ".")
        return render_template('produtos.html', mensagem_sucesso=mensagem_sucesso)  # Caso de sucesso no processo
    else:
        return render_template('produtos.html', error_message=mensagem_erro)  # Caso de erro no processo# tradamento de dados
    
# Função para mover produtos
@app.route('/mover_produto', methods=['POST'])
def mover_produto():
    produtoid = request.form.get('mover-produtoid')
    tipo_movimentacao = request.form.get('tipo-mover').upper()
    quantidade = int(request.form.get('quantidade-mover'))
    acao = request.form.get('DecisaoMover')
    
    # Caso nem todos os campos estejam preenchidos retorna mensagem de erro ao usuário
    if not (tipo_movimentacao and quantidade ) and acao == "confirmar":
        return "Todos os campos são obrigatórios", 400
    # Caso operação seja cancelada recarrega a página
    elif acao == "cancelar":
        return redirect(url_for('produtos'))
    
    elif acao == "confirmar":
        quantidade_atual = produtos_Obj.getQuantidade(produtoid)
        diferenca = quantidade_atual - quantidade

        # Caso subtração seja negativa (ERRO)
        if tipo_movimentacao == "RETIRADA" and (diferenca < 0): 
            return "Quantidade negativa", 500  
        # Caso subtração seja positiva (OK)
        elif tipo_movimentacao == "RETIRADA" and (diferenca >= 0):
            if produtos_Obj.setQuantidade(produtoid, diferenca):
                return redirect(url_for('produtos'))  
        # Caso a operação seja de adição
        elif tipo_movimentacao == "ADIÇÂO" and produtos_Obj.setQuantidade(produtoid, (quantidade_atual+ quantidade)):
                return redirect(url_for('produtos'))  
        
    else:
        return "Erro ao editar o produto", 500  # Caso de erro no processo

''' Categorias '''
# Função responsável por carregar o template de categorias:      
@app.route('/categorias', methods=['GET', 'POST'])
def categorias():
    results = None
    if conexao.banco_conectado():
        results = ""
        return render_template('categorias.html', envios=results)
    else:
        return "Erro na conexão com o banco de dados"

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
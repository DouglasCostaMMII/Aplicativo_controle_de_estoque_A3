from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
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

# Função responsável por carregar o template de produtos:        
@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
    results = None
    if conexao.banco_conectado():
        results = fetch_produtos_data()
        return render_template('produtos.html', produtos=results)
    else:
        return "Erro na conexão com o banco de dados"
    
@app.route('/add_produto', methods=['POST'])
def add_produto():
    nome = request.form.get('nome')
    status = request.form.get('status').upper()
    categoria = request.form.get('categoria')
    preco = request.form.get('preco')
    qnt_min = request.form.get('qnt_min')
    acao = request.form.get('acao')

    if "," in preco:
        preco = preco.replace(",", ".")

    if not (nome and status and categoria and preco and qnt_min) and acao == "confirmar":
        return "Todos os campos são obrigatórios", 400
    elif acao == "cancelar":
        return redirect(url_for('produtos'))
    elif acao == "confirmar" and produtos_Obj.add_produto(nome, status, categoria, preco, qnt_min, acao)[0]:
        return redirect(url_for('produtos'))  # Adiciona return aqui
    else:
        return "Erro ao adicionar o produto", 500  # Caso de erro no processo

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

    if "," in preco:
        preco = preco.replace(",", ".")  
    
    if not (nome and status and categoria and preco and qnt_min) and acao == "confirmar":
        return "Todos os campos são obrigatórios", 400
    elif acao == "cancelar":
        return redirect(url_for('produtos'))
    elif acao == "confirmar" and produtos_Obj.editar_produto(nome, status, categoria, preco, qnt_min, produtoid)[0]:
        return redirect(url_for('produtos'))  # Adiciona return aqui
    else:
        return "Erro ao editar o produto", 500  # Caso de erro no processo


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
    db_config = {
        'user': 'root',
        'password': "",
        'host': "192.168.0.125", 
        'database': "estoque"
    }
    try: 
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        query = "SELECT produtoid, nome, descricao, preco, quantidade, categoria_id, status FROM produtos"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        # Atualizando o dicionário com o nome correspondente ao ID do cliente
        for obj in results:
            if 'categoria_id' in obj:
                obj['categoria_id'] = categoria_Obj.getNome(obj['categoria_id'])
        return results
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        return []

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
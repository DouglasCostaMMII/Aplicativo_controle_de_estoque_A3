from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from Model.categoriasDAO import CategoriaDAO 
from Model.entradasDAO import EntradasDAO 
from Model.saidasDAO import SaidasDAO 
from Model.produtosDAO import ProdutosDAO 

# Muda o diretório de templates para 'View' e o static para 'Estilo'
app = Flask(__name__, template_folder='View', static_folder='View/Estilo')

# Criação de objetos que serão posteriormente utilizados 
categoria_Obj = CategoriaDAO()
entrada_Obj = EntradasDAO()
saidas_Obj = SaidasDAO()
srodutos_Obj = ProdutosDAO()

@app.route('/', methods=['GET', 'POST'])
def index():
    show_error = False
    if request.method == 'GET':
        if banco_conectado():  
            return redirect(url_for('produtos'))    # Tela que será carregada ao inicializar o programa.
        else:
            show_error = True
            return render_template('produtos.html', show_error=show_error)

# Função responsável por carregar o template de produtos:        
@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
    results = None
    if banco_conectado():
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
    acao = request.form.get('acao')

    if "," in preco:
        preco = preco.replace(",", ".")

    if not (nome and status and categoria and preco and qnt_min) and acao == "confirmar":
        return "Todos os campos são obrigatórios", 400
    elif acao == "cancelar":
        return redirect(url_for('produtos'))
    else:
        if banco_conectado():
            try:
                db_config = {
                    'user': 'root',
                    'password': "",
                    'host': "192.168.1.112", 
                    'database': "estoque"
                }
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                query = "INSERT INTO produtos (nome, status, categoria_id, preco, quantidade, quantidade_minima) VALUES (%s, %s, %s, %s, 0, %s)"
                cursor.execute(query, (nome, status, categoria, preco, qnt_min))
                conn.commit()
            except mysql.connector.Error as err:
                print(f"Erro ao adicionar produto: {err}")
                return "Erro ao adicionar produto", 500
            finally:
                cursor.close()
                conn.close()
            
            return redirect(url_for('produtos'))
        else:
            return "Erro na conexão com o banco de dados", 500

# Função para editar produtos
@app.route('/editar_produto', methods=['POST'])
def editar_produto():
    nome = request.form.get('editar-nome')
    status = request.form.get('editar-status').upper()
    categoria = request.form.get('editar-categoria')
    preco = request.form.get('editar-preco')
    qnt_min = request.form.get('editar-qnt_min')
    produtoid = request.form.get('editar-editar_produtoid')

    if banco_conectado():
        try:
            db_config = {
                'user': 'root',
                'password': "",
                'host': "192.168.1.112", 
                'database': "estoque"
            }
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            query = """
                UPDATE produtos
                SET nome = %s, status = %s, categoria_id = %s, preco = %s, quantidade_minima = %s
                WHERE produtoid = %s
            """
            cursor.execute(query, (nome, status, categoria, preco, qnt_min, produtoid))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('produtos'))
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            return "Erro ao editar produto", 500
    else:
        return "Erro na conexão com o banco de dados", 500


# Função responsável por carregar o template de categorias:      
@app.route('/categorias', methods=['GET', 'POST'])
def categorias():
    results = None
    if banco_conectado():
        results = ""
        return render_template('categorias.html', envios=results)
    else:
        return "Erro na conexão com o banco de dados"

# Função responsável por carregar o template de relatórios:      
@app.route('/relatorios', methods=['GET', 'POST'])
def relatorios():
    results = None
    if banco_conectado():
        results = ""
        return render_template('relatorios.html', envios=results)
    else:
        return "Erro na conexão com o banco de dados"

# Função responsável por verificar se há conexão com o banco de dados:         
def banco_conectado():
    # Parâmetros para se conectar ao banco de dados. Atenção ao IP do host e a senha do banco utilizados. 
    db_config = {
        'user': 'root',
        'password': "",
        'host': "192.168.1.112", 
        'database': "estoque"
    }
    try: 
        conn = mysql.connector.connect(**db_config)
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(err)
        return False
    
def fetch_produtos_data():
    db_config = {
        'user': 'root',
        'password': "",
        'host': "192.168.1.112", 
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
        return results
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
        return []

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
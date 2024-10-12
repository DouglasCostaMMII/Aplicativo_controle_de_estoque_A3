from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from Model.categoriasDAO import CategoriaDAO 
from Model.entradasDAO import EntradasDAO 
from Model.saidasDAO import SaidasDAO 
from Model.produtosDAO import ProdutosDAO 

# Muda o diretório de templates para 'view'
app = Flask(__name__, template_folder='View')

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
            return redirect(url_for('main'))
        else:
            show_error = True
            return render_template('categorias.html', show_error=show_error)

# Função responsável por carregar o template de produtos:        
@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
    results = None
    if banco_conectado():
        results = ""
        return render_template('produtos.html', envios=results)
    else:
        return "Erro na conexão com o banco de dados"

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
        'password': "admin123",
        'host': "192.168.1.114", 
        'database': "estoque"
    }
    try: 
        conn = mysql.connector.connect(**db_config)
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(err)
        return False
    
@app.route('/main', methods=['GET', 'POST'])
def main():
    if banco_conectado():
        return render_template('categorias.html')
    else:
        return "Erro na conexão com o banco de dados"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
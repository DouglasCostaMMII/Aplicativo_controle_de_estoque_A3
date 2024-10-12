from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from Model.categoriasDAO import CategoriaDAO 
from Model.entradasDAO import EntradasDAO 
from Model.saidasDAO import SaidasDAO 
from Model.produtosDAO import ProdutosDAO 

# Muda o diretório de templates para 'view'
app = Flask(__name__, template_folder='view')

# Criação de objetos que serão posteriormente utilizados 
categoria = CategoriaDAO()
entrada = EntradasDAO()
saidas = SaidasDAO()
produtos = ProdutosDAO()

@app.route('/', methods=['GET', 'POST'])
def index():
    show_error = False
    if request.method == 'GET':
        if banco_conectado():  
            return redirect(url_for('main'))
        else:
            show_error = True
            return render_template('index.html', show_error=show_error)
    
def banco_conectado():
    # Parâmetros para se conectar ao banco de dados. Atenção ao IP do host e a senha do banco utilizados. 
    db_config = {
        'user': 'root',
        'password': "admin123",
        'host': "192.168.1.114", 
        'database': "estoque"
    }
    try: 
        print("Tentando")
        conn = mysql.connector.connect(**db_config)
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(err)
        return False
    
@app.route('/main', methods=['GET', 'POST'])
def main():
    if banco_conectado():
        return render_template('index.html')
    else:
        return "Erro na conexão com o banco de dados"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
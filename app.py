from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from Model.categoriasDAO import CategoriaDAO 
from Model.entradasDAO import EntradasDAO 
from Model.saidasDAO import SaidasDAO 
from Model.produtosDAO import ProdutosDAO 

# Mude o diretório de templates para 'view'
app = Flask(__name__, template_folder='view')

categoria = CategoriaDAO()
entrada = EntradasDAO()
saidas = SaidasDAO()
produtos = ProdutosDAO()

@app.route('/', methods=['GET', 'POST'])
def index():
    show_error = False
    if request.method == 'POST':
        # Aqui você deve colocar a lógica que você deseja verificar
        if True:  # Substitua isso pela sua condição real
            return redirect(url_for('main'))
        else:
            show_error = True
            
    # Sempre retorne a renderização do template, mesmo se for um GET
    return render_template('index.html', show_error=show_error)
    
def banco_conectado(banco, ip, senha):
    db_config = {
        'user': 'root',
        'password': senha,
        'host': ip,
        'database': banco
    }
    if banco == "estoque" and ip == "192.168.1.114" and senha == "admin123":
        try: 
            conn = mysql.connector.connect(**db_config)
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(err)
            return False
    else:
        return False
    
@app.route('/main', methods=['GET', 'POST'])
def main():
    banco = "estoque"
    ip = "192.168.1.114"
    senha = "admin123"
    results = None
    if banco_conectado(banco, ip, senha):
        return render_template('index.html', envios=results)
    else:
        return "Erro na conexão com o banco de dados"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
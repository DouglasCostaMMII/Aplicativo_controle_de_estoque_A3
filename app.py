from flask import Flask, redirect, url_for
from Controller.produtosAPP import produtos_blueprint  
from Controller.categoriasAPP import categorias_blueprint
from Controller.relatoriosAPP import relatorio_blueprint

# Inicializa o app Flask
app = Flask(__name__, template_folder='View/Corpo', static_folder='View/Estilo')

# Registra os blueprints
app.register_blueprint(produtos_blueprint)
app.register_blueprint(categorias_blueprint)
app.register_blueprint(relatorio_blueprint)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Redireciona para a rota de produtos do Blueprint
    return redirect(url_for('produtos.produtos'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

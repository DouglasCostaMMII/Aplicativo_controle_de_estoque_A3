from flask import Blueprint, render_template, request, redirect, url_for
from Model.conexaoDAO import ConexaoDAO

# Criação do blueprint
relatorios_blueprint = Blueprint('relatorios', __name__, template_folder='View')

# Criação de objetos que serão utilizados
conexao = ConexaoDAO()

# Função responsável por carregar o template de relatórios:      
@relatorios_blueprint.route('/relatorios', methods=['GET', 'POST'])
def relatorios():
    results = None
    if conexao.banco_conectado():
        results = ""
        return render_template('relatorios.html', envios=results)
    else:
        return "Erro na conexão com o banco de dados"

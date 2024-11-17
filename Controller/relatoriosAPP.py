from flask import Blueprint, render_template, request, redirect, url_for
from Model.conexaoDAO import ConexaoDAO
from Model.entradaDAO import EntradaDAO
from Model.saidaDAO import SaidaDAO


# Criação do blueprint
relatorio_blueprint = Blueprint('relatorio', __name__, template_folder='View')

# Criação de objetos que serão posteriormente utilizados
entradas_Obj = EntradaDAO()
saidas_Obj = SaidaDAO()
conexao = ConexaoDAO()

# Criação de objetos que serão utilizados
conexao = ConexaoDAO()

# Função responsável por carregar o template de relatórios:      
@relatorio_blueprint.route('/relatorios', methods=['GET', 'POST'])
def relatorios():
    if conexao.banco_conectado():
        results = entradas_Obj.visualizar_entradas_DAO() + saidas_Obj.visualizar_saidas_DAO()
        return render_template('relatorios.html', relatorio=results)
    else:
        return "Erro na conexão com o banco de dados"

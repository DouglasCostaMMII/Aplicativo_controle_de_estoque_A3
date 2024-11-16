from flask import Blueprint, render_template, request, redirect, url_for
from Controller.categorias import Categoria
from Model.conexaoDAO import ConexaoDAO


# Criação do blueprint
categorias_blueprint = Blueprint('categorias', __name__, template_folder='View')

# Criação de objetos que serão posteriormente utilizados
categoria_Obj = Categoria()
conexao = ConexaoDAO()

# Função responsável por carregar o template de categorias:      
@categorias_blueprint.route('/categorias', methods=['GET', 'POST'])
def categorias():
    results = categoria_Obj.visualizarCategoria()
    if conexao.banco_conectado():
        return render_template('categorias.html', categorias=results)
    else:
        return "Erro na conexão com o banco de dados"

@categorias_blueprint.route('/add_categoria', methods=['POST'])
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
@categorias_blueprint.route('/editar_categoria', methods=['POST'])
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
@categorias_blueprint.route('/alterar_StatusCategoria', methods=['POST'])
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
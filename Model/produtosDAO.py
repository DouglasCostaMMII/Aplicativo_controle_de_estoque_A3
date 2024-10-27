import mysql.connector
import bancoConectadoBase
from mysql.connector import Error
from flask import Flask, render_template, request, redirect, url_for


class ProdutosDAO:
    def __init__(self, nome="", descricao="", preco=0.0, quantidade=0, categoriaID=0):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.quantidade = quantidade
        self.categoriaID = categoriaID

    # GETS
    def getNome(self):  
        return self.nome
    def getDescricao(self):
        return self.descricao
    def getPreco(self):  
        return self.preco
    def getQuantidade(self):
        return self.quantidade
    def getCategoriaID(self):
        return self.categoriaID
    
    #SETS
    def setNome(self, novoNome):  
        self.nome = novoNome
    def setDescricao(self, novaDescricao):
        self.descricao = novaDescricao
    def setPreco(self, novoPreco):  
        self.preco = novoPreco
    def setQuantidade(self, novaQuantidade):
        self.quantidade = novaQuantidade
    def setCategoriaID(self, novaCategoriaID):
        self.categoriaID = novaCategoriaID
    
    #Add pradoto
    def add_produto():
        nome = request.form.get('nome')
        status = request.form.get('status').upper()
        categoria = request.form.get('categoria')
        preco = request.form.get('preco')
        qnt_min = request.form.get('qnt_min')

        if not (nome and status and categoria and preco and qnt_min):
            return "Todos os campos são obrigatórios", 400

        if bancoConectadoBase.banco_conectado(True):
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
    
    # def fetch_produtos_data():
    #     db_config = {
    #         'user': 'root',
    #         'password': "",
    #         'host': "192.168.1.112", 
    #         'database': "estoque"
    #     }
    #     try: 
    #         conn = mysql.connector.connect(**db_config)
    #         cursor = conn.cursor(dictionary=True)
    #         query = "SELECT produtoid, nome, descricao, preco, quantidade, categoria_id, status FROM produtos"
    #         cursor.execute(query)
    #         results = cursor.fetchall()
    #         cursor.close()
    #         conn.close()
    #         return results
    #     except mysql.connector.Error as err:
    #         print(f"Erro: {err}")
    #         return []

    '''
    Desenvolver métodos de interação com o banco de dados

    def adicionar_produto()
    ...

    def editar_produto()
    ...

    def visualizar_produto()
    ...

    def deletar_produto()
    ...    
    '''
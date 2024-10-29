from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error
from Controller.conexaoDAO import ConexaoDAO


conexao = ConexaoDAO()

class ProdutoDAO:

    def add_produto_DAO(self, nome, status, categoria, preco, qnt_min, acao):
        if conexao.banco_conectado():
            db_config = conexao.dados_db()
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                query = "INSERT INTO produtos (nome, status, categoria_id, preco, quantidade, quantidade_minima) VALUES (%s, %s, %s, %s, 0, %s)"
                cursor.execute(query, (nome, status, categoria, preco, qnt_min))
                conn.commit()
                cursor.close()
                conn.close()
                return [True]
            except mysql.connector.Error as err:
                print(f"Erro: {err}")
                return [False, "Erro ao adicionar produto", 500]
        else:
            return [False, "Erro na conexão com o banco de dados", 500]
        
    def editar_produto_DAO(self, nome, status, categoria, preco, qnt_min, produtoid):
        if conexao.banco_conectado():
            db_config = conexao.dados_db()
            try:
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
                return [True]
            except mysql.connector.Error as err:
                print(f"Erro: {err}")
                return [False, "Erro ao editar produto", 500]
        else:
            return [False, "Erro na conexão com o banco de dados", 500]

    #Add produto
    def add_produtoDAO(self, nome, status, categoria, qnt_min):
        nome = request.form.get('nome')
        status = request.form.get('status').upper()
        categoria = request.form.get('categoria')
        preco = request.form.get('preco')
        qnt_min = request.form.get('qnt_min')

        if not (nome and status and categoria and preco and qnt_min):
            return "Todos os campos são obrigatórios", 400

        if conexao.banco_conectado():
            try:
                db_config = {
                    'user': 'root',
                    'password': "",
                    'host': "192.168.0.125", 
                    'database': "estoque"
                }
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                query = "INSERT INTO produtos (nome, status, categoria_id, preco, quantidade, quantidade_minima) VALUES (%s, %s, %s, %s, 0, %s)"
                cursor.execute(query, (nome, status, categoria, preco, qnt_min))
                conn.commit()
                cursor.close()
                conn.close()
                return[True]
            except mysql.connector.Error as err:
                print(f"Erro ao adicionar produto: {err}")
                return "Erro ao adicionar produto", 500
            finally:
                cursor.close()
                conn.close()
            
                return redirect(url_for('produtos'))
        else:
            return [False, "Erro na conexão com o banco de dados", 500]
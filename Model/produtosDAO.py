from flask import redirect, url_for
import mysql.connector 
import sqlite3
from Model.conexaoDAO import ConexaoDAO
from Model.categoriasDAO import CategoriaDAO


# Criação de objetos que serão posteriormente utilizados
conexao = ConexaoDAO()
categoria_Obj = CategoriaDAO()

class ProdutoDAO:

    ''' Gets '''
    # Obtém o nome do produto pelo ID.
    def getNomeDAO(self, produtoid):
        if conexao.banco_conectado()[0]:
            db_config = conexao.dados_db()
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor(dictionary=True)
                sql = "SELECT nome FROM produtos WHERE produtoid = %s"
                cursor.execute(sql, (produtoid,))
                nome = cursor.fetchone()
                cursor.close()
                conn.close()
                
                if nome:
                    return nome['nome']
                else:
                    print(f"Nenhum nome encontrado com o id: {produtoid}")
                    return ""
            except mysql.connector.Error as e:
                print(f"Erro ao buscar a quantidade do produto: {e}")
            return ""
    
    # Obtém a quantidade do produto através do ID.    
    def getQuantidadeDAO(self, produtoid):
        if conexao.banco_conectado()[0]:
            db_config = conexao.dados_db()
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor(dictionary=True)
                sql = "SELECT quantidade FROM produtos WHERE produtoid = %s"
                cursor.execute(sql, (produtoid,))
                quantidade = cursor.fetchone()
                cursor.close()
                conn.close()
                
                if quantidade:
                    return int(quantidade['quantidade'])
                else:
                    print(f"Nenhuma quantidade encontrada com o id: {produtoid}")
                    return ""
            except mysql.connector.Error as e:
                print(f"Erro ao buscar a quantidade do produto: {e}")
            return ""

    # Obtém o status do produto através do ID.            
    def getStatusDAO(self, produtoid):
        if conexao.banco_conectado()[0]:
            db_config = conexao.dados_db()
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor(dictionary=True)
                sql = "SELECT status FROM produtos WHERE produtoid = %s"
                cursor.execute(sql, (produtoid,))
                status = cursor.fetchone()
                cursor.close()
                conn.close()
                
                if status:
                    return str(status['status'])
                else:
                    print(f"Nenhum status encontrada com o id: {produtoid}")
                    return ""
            except mysql.connector.Error as e:
                print(f"Erro ao buscar o status do produto: {e}")
            return ""

    # Obtém a categoria do produto através do ID.            
    def getCategoriaDAO(self, produtoid):
        if conexao.banco_conectado()[0]:
            db_config = conexao.dados_db()
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor(dictionary=True)
                sql = "SELECT categoria_id FROM produtos WHERE produtoid = %s"
                cursor.execute(sql, (produtoid,))
                categoria = cursor.fetchone()
                cursor.close()
                conn.close()
                
                if categoria:
                    return str(categoria['categoria_id'])
                else:
                    print(f"Nenhum status encontrada com o id: {produtoid}")
                    return ""
            except mysql.connector.Error as e:
                print(f"Erro ao buscar o status do produto: {e}")
            return ""

    ''' Sets '''
    # Atualiza a quantidade do produto.
    def setQuantidadeDAO(self, produtoid, quantidade):
        sql = "UPDATE produtos SET quantidade = %s WHERE produtoid = %s"
        try:
            conectado = conexao.banco_conectado()[1]
            cursor = conectado.cursor()
            cursor.execute(sql, (quantidade, produtoid))
            conectado.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            print(f"Erro: {e}")

    # Atualiza o status do produto.    
    def setStatusDAO(self, produtoid, status):
        sql = "UPDATE produtos SET status = %s WHERE produtoid = %s"
        try:
            conectado = conexao.banco_conectado()[1]
            cursor = conectado.cursor()
            cursor.execute(sql, (status, produtoid))
            conectado.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            print(f"Erro: {e}")

    ''' CRUD '''
    # Adiciona um produto novo.
    def add_produto_DAO(self, nome, status, categoria, preco, qnt_min, acao):
        if conexao.banco_conectado()[0]:
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
    
    # Edita o produto selecionado.     
    def editar_produto_DAO(self, nome, status, categoria, preco, qnt_min, produtoid):
        if conexao.banco_conectado()[0]:
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
        
    # Retorna todos os produtos encontrados no banco de dados e suas informações.
    def visualizar_produtos_DAO(self):
        if conexao.banco_conectado()[0]:
            db_config = conexao.dados_db()
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor(dictionary=True)
                query = "SELECT * FROM produtos"
                cursor.execute(query)
                results = cursor.fetchall()
                cursor.close()
                conn.close()
                for obj in results:
                    if 'categoria_id' in obj:
                        obj['categoria_id'] = categoria_Obj.getNomeDAO(obj['categoria_id'])
                return results
            except mysql.connector.Error as err:
                print(f"Erro: {err}")
                return []
            
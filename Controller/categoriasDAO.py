import mysql.connector
import sqlite3
from mysql.connector import Error
from Controller.conexaoDAO import ConexaoDAO


conexao = ConexaoDAO()

class CategoriaDAO:

    ''' GETS '''
    # Obtém o nome da categoria pelo ID.
    def getCategoriaidDAO(self, nome):
        if conexao.banco_conectado():
            db_config = conexao.dados_db()
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor(dictionary=True)
                sql = "SELECT categoriaid FROM categorias WHERE nome = %s"
                cursor.execute(sql, (nome,))
                categoriaid = cursor.fetchone()
                cursor.close()
                conn.close()
                return categoriaid['categoriaid']
            except mysql.connector.Error as e:
                print(f"Erro ao buscar o nome da categoria: {e}")
            return ""
    # Obtém o nome da categoria pelo ID.
    def getNomeDAO(self, categoriaid):
        if conexao.banco_conectado():
            db_config = conexao.dados_db()
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor(dictionary=True)
                sql = "SELECT nome FROM categorias WHERE categoriaid = %s"
                cursor.execute(sql, (categoriaid,))
                nome = cursor.fetchone()
                cursor.close()
                conn.close()
                
                if nome:
                    return nome['nome']
                else:
                    print(f"Nenhum nome encontrado com o id: {categoriaid}")
                    return ""
            except mysql.connector.Error as e:
                print(f"Erro ao buscar o nome da categoria: {e}")
            return ""
    # Obtém a descricao da categoria pelo ID.
    def getDescricaoDAO(self, categoriaid):
        if conexao.banco_conectado():
            db_config = conexao.dados_db()
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor(dictionary=True)
                sql = "SELECT descricao FROM categorias WHERE categoriaid = %s"
                cursor.execute(sql, (categoriaid,))
                descricao = cursor.fetchone()
                cursor.close()
                conn.close()
                
                if descricao:
                    return descricao['descricao']
                else:
                    print(f"Nenhuma descricao encontrada com o id: {categoriaid}")
                    return ""
            except mysql.connector.Error as e:
                print(f"Erro ao buscar a descricao da categoria: {e}")
            return ""
        
    # Obtém o status da categoria pelo ID.
    def getStatusDAO(self, categoriaid):
        if conexao.banco_conectado():
            db_config = conexao.dados_db()
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor(dictionary=True)
                sql = "SELECT status FROM categorias WHERE categoriaid = %s"
                cursor.execute(sql, (categoriaid,))
                status = cursor.fetchone()
                cursor.close()
                conn.close()
                
                if status:
                    return status['descrstatusicao']
                else:
                    print(f"Nenhum status encontrada com o id: {categoriaid}")
                    return ""
            except mysql.connector.Error as e:
                print(f"Erro ao buscar o status da categoria: {e}")
            return ""

    ''' SETS ''' 
    # Atualiza o nome da categoria.
    def setNomeDAO(self, categoriaid, novo_nome):
        sql = "UPDATE categorias SET nome = ? WHERE categoriaid = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (novo_nome, categoriaid))
            self.connection.commit()
            cursor.close()
        except sqlite3.Error as e:
            print(f"Erro: {e}")

    # Atualiza a descricao da categoria.
    def setNomeDAO(self, categoriaid, nova_descricao):
        sql = "UPDATE categorias SET descricao = ? WHERE categoriaid = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (nova_descricao, categoriaid))
            self.connection.commit()
            cursor.close()
        except sqlite3.Error as e:
            print(f"Erro: {e}")

    # Atualiza o status da categoria.
    def setStatusDAO(self, categoriaid, novo_status):
        sql = "UPDATE categorias SET status = ? WHERE categoriaid = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (novo_status, categoriaid))
            self.connection.commit()
            cursor.close()
        except sqlite3.Error as e:
            print(f"Erro: {e}")

    ''' CRUD '''
    # Adiciona uma categoria nova.
    def adicionarCategoriaDAO(self, nome, descricao):
        sql = "INSERT INTO categorias (nome, descricao) VALUES (?, ?)"
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, (nome, descricao))
            self.connection.commit()
            cursor.close()
        except sqlite3.Error as e:
            print(f"Erro: {e}")

    # Retorna todas as categorias encontradas no banco de dados e suas informações.
    def visualizarCategoriaDAO():
        if conexao.banco_conectado():
            db_config = conexao.dados_db()
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor(dictionary=True)
                query = "SELECT * FROM categorias"
                cursor.execute(query)
                results = cursor.fetchall()
                cursor.close()
                conn.close()
                return results
            except mysql.connector.Error as err:
                print(f"Erro: {err}")
                return []
            
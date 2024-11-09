import mysql.connector
import sqlite3
import mysql.connector 
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
        
    # Obtém o status da categoria pelo ID.
    def getStatusDAO(self, categoriaid):
        if conexao.banco_conectado()[0]:
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
                     return str(status['status'])
                else:
                    print(f"Nenhum status encontrada com o id: {categoriaid}")
                    return ""
            except mysql.connector.Error as e:
                print(f"Erro ao buscar o status da categoria: {e}")
            return ""

    ''' SETS ''' 
    # Atualiza o nome da categoria.
    def setNomeDAO(self, categoriaid, nome):
            if conexao.banco_conectado()[0]:
                db_config = conexao.dados_db()
                try:
                    conn = mysql.connector.connect(**db_config)
                    cursor = conn.cursor()
                    sql = "UPDATE categorias SET nome = %s WHERE categoriaid = %s"
                    cursor.execute(sql, (nome, categoriaid))
                    conn.commit()
                    cursor.close()
                    return [True]
                except sqlite3.Error as e:
                    print(f"Erro: {e}")

    # Atualiza o status da categoria.
    def setStatusDAO(self, categoriaid, status):
            if conexao.banco_conectado()[0]:
                db_config = conexao.dados_db()
                try:
                    conn = mysql.connector.connect(**db_config)
                    cursor = conn.cursor()
                    sql = "UPDATE categorias SET status = %s WHERE categoriaid = %s"
                    cursor.execute(sql, (status, categoriaid))
                    conn.commit()
                    cursor.close()
                    return [True]
                except sqlite3.Error as e:
                    print(f"Erro: {e}")

    ''' CRUD '''
    # Adiciona uma categoria nova.
    def adicionarCategoriaDAO(self, nome, status):
        if conexao.banco_conectado()[0]:
            db_config = conexao.dados_db()
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                sql = "INSERT INTO categorias (nome, status) VALUES (%s, %s)"
                cursor.execute(sql, (nome, status,))
                conn.commit()
                cursor.close()
                conn.close()
                return [True]
            except mysql.connector.Error as err:
                print(f"Erro: {err}")
                return [False, "Erro ao adicionar categoria", 500]
        else:
            return [False, "Erro na conexão com o banco de dados", 500]

    # Retorna todas as categorias encontradas no banco de dados e suas informações.
    def visualizarCategoriaDAO(self):
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
            
import mysql.connector 
from Model.conexaoDAO import ConexaoDAO
from Model.categoriasDAO import CategoriaDAO
from Model.produtosDAO import ProdutoDAO


# Criação de objetos que serão posteriormente utilizados
conexao = ConexaoDAO()
categoria_Obj = CategoriaDAO()
produto_Obj = ProdutoDAO()

class EntradaDAO:

    ''' CRUD '''
    # Função para adicionar uma nova entrada ao banco de dados
    def add_entrada_DAO(self, produtoid, categoriaid, quantidade, data):
        if conexao.banco_conectado()[0]:
            db_config = conexao.dados_db()
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                query = "INSERT INTO entradas (produto_id, categoria_idE, quantidade, data_entrada) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (produtoid.strip(), categoriaid, quantidade, data))
                conn.commit()
                cursor.close()
                conn.close()
                return [True]
            except mysql.connector.Error as err:
                print(f"Erro: {err}")
                return [False, "Erro ao adicionar entrada", 500]
        else:
            return [False, "Erro na conexão com o banco de dados", 500]
    
    # Retorna todas as entradas encontradas no banco de dados e suas informações.    
    def visualizar_entradas_DAO(self):
        if conexao.banco_conectado()[0]:
            db_config = conexao.dados_db()
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor(dictionary=True)
                query = "SELECT * FROM entradas"
                cursor.execute(query)
                results = cursor.fetchall()
                cursor.close()
                conn.close()
                for obj in results:
                    if 'categoria_idE' in obj:
                        obj['categoria_idE'] = categoria_Obj.getNomeDAO(obj['categoria_idE'])
                    if 'produto_id' in obj:
                        obj['produto_id'] = produto_Obj.getNomeDAO(obj['produto_id'])
                return results
            except mysql.connector.Error as err:
                print(f"Erro: {err}")
                return []
            
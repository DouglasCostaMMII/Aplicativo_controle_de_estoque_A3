import mysql.connector

class ConexaoDAO:

    def dados_db(self):
        return {
            'user': 'usuario',
            'password': "",
            'host': "10.149.129.3", 
            'database': "estoque"
        }

    def banco_conectado(self):
        db_config = {
            'user': 'usuario',
            'password': "",
            'host': "10.149.129.3", 
            'database': "estoque"
        }
        
        try: 
            conn = mysql.connector.connect(**db_config)
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(err)
            return False
    
import mysql.connector

class ConexaoDAO:

    def dados_db(self):
        return {
            'user': 'root',
            'password': "",
            'host': "192.168.0.125", 
            'database': "estoque"
        }

    def banco_conectado(self):
        db_config = {
            'user': 'root',
            'password': "",
            'host': "192.168.0.125", 
            'database': "estoque"
        }
        
        try: 
            conn = mysql.connector.connect(**db_config)
            conn.close()
            return True
        except mysql.connector.Error as err:
            print(err)
            return False
    
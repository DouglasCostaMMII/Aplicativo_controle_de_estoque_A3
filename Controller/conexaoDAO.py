import mysql.connector
import sqlite3
import socket


class ConexaoDAO:

    def get_ip(self):
        hostname = socket.gethostname()  # Obtém o nome do host
        ip_address = socket.gethostbyname(hostname)  # Obtém o IP do host
        return ip_address
    
    def dados_db(self):
        return {
            'user': 'root',
            'password': "",
            'host': self.get_ip(),
            'database': "estoque"
        }

    def banco_conectado(self):
        db_config = self.dados_db()
        
        try: 
            conn = mysql.connector.connect(**db_config)
            return [True, conn]
        except mysql.connector.Error as err:
            print(f"Falha na conexão: {err}")
            return [False, None]
        
    
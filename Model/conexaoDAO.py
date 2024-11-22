import mysql.connector
import socket


class ConexaoDAO:
    
    # Função para obter o IP do Host da máquina
    def get_ip(self):
        hostname = socket.gethostname()  # Obtém o nome do host
        ip_address = socket.gethostbyname(hostname)  # Obtém o IP do host
        return ip_address
    
    # Dados para conectar ao banco de dados
    def dados_db(self):
        return {'user': 'root',
                'password': "",
                'host': self.get_ip(),
                'database': "estoque"}

    # Função para se conectar ao banco de dados
    def banco_conectado(self):
        db_config = self.dados_db()
        try: 
            conn = mysql.connector.connect(**db_config)
            return [True, conn]
        except mysql.connector.Error as err:
            print(f"Falha na conexão: {err}")
            return [False, None]

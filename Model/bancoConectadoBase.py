import mysql.connector


def banco_conectado():
    # Parâmetros para se conectar ao banco de dados. Atenção ao IP do host e a senha do banco utilizados. 
    db_config = {
        'user': 'root',
        'password': "",
        'host': "192.168.1.112", 
        'database': "estoque"
    }
    try: 
        conn = mysql.connector.connect(**db_config)
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(err)
        return False
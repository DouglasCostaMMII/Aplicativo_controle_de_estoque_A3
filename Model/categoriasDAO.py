import mysql.connector
from mysql.connector import Error


class CategoriaDAO:
    def __init__(self, nome="", descricao=""):
        self.nome = nome
        self.descricao = descricao

    # GETS
    def getNome(self):  
        return self.nome
    def getDescricao(self):
        return self.descricao
    
    #SETS
    def setNome(self, novoNome):  
        self.nome = novoNome
    def setDescricao(self, novaDescricao):
        self.descricao = novaDescricao

    '''
    Desenvolver métodos de interação com o banco de dados

    def adicionar_categoria()
    ...

    def editar_categoria()
    ...

    def visualizar_categoria()
    ...

    def deletar_categoria()
    ...    
    '''
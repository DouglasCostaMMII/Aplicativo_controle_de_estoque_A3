import mysql.connector
from mysql.connector import Error


class SaidasDAO:
    def __init__(self, produtoID=0, quantidade=0, data=""):
        self.produtoID = produtoID
        self.quantidade = quantidade
        self.data = data

    # GETS
    def getProdutoID(self):  
        return self.produtoID
    def getQuantidade(self):
        return self.quantidade
    def getData(self):
        return self.data
    
    #SETS
    def setProdutoID(self, novoProdutoID):  
        self.produtoID = novoProdutoID
    def setQuantidade(self, novaQuantidade):
        self.quantidade = novaQuantidade
    def setData(self, novaData):
        self.data = novaData
    

    '''
    Desenvolver métodos de interação com o banco de dados

    def adicionar_saida()
    ...

    def editar_saida()
    ...

    def visualizar_saida()
    ...

    def deletar_saida()
    ...    
    '''
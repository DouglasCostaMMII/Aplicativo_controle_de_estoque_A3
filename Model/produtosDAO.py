import mysql.connector
from mysql.connector import Error


class ProdutosDAO:
    def __init__(self, nome="", descricao="", preco=0.0, quantidade=0, categoriaID=0):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.quantidade = quantidade
        self.categoriaID = categoriaID

    # GETS
    def getNome(self):  
        return self.nome
    def getDescricao(self):
        return self.descricao
    def getPreco(self):  
        return self.preco
    def getQuantidade(self):
        return self.quantidade
    def getCategoriaID(self):
        return self.categoriaID
    
    #SETS
    def setNome(self, novoNome):  
        self.nome = novoNome
    def setDescricao(self, novaDescricao):
        self.descricao = novaDescricao
    def setPreco(self, novoPreco):  
        self.preco = novoPreco
    def setQuantidade(self, novaQuantidade):
        self.quantidade = novaQuantidade
    def setCategoriaID(self, novaCategoriaID):
        self.categoriaID = novaCategoriaID
    

    '''
    Desenvolver métodos de interação com o banco de dados

    def adicionar_produto()
    ...

    def editar_produto()
    ...

    def visualizar_produto()
    ...

    def deletar_produto()
    ...    
    '''
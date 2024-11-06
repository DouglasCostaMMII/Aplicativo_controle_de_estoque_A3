import mysql.connector
from mysql.connector import Error
from Controller.produtosDAO import ProdutoDAO


produtoDAO = ProdutoDAO()

class Produtos:
    def __init__(self, nome="", status="", preco=0.0, quantidade=0, categoriaID=0):
        self.nome = nome
        self.status = status
        self.preco = preco
        self.quantidade = quantidade
        self.categoriaID = categoriaID

    # GETS
    def getNome(self, produtoid): 
        return self.nome
    def getStatus(self, produtoid):
        return produtoDAO.getStatusDAO(produtoid)
    def getPreco(self, produtoid):
        return self.preco
    def getQuantidade(self, produtoid):
        return produtoDAO.getQuantidadeDAO(produtoid)
    def getCategoriaID(self, produtoid):
        return self.categoriaID
    
    #SETS
    def setNome(self, novoNome):  
        self.nome = novoNome
    def setStatus(self, produtoid, novoStatus):
        return produtoDAO.setStatusDAO(produtoid, novoStatus)
    def setPreco(self, novoPreco):  
        self.preco = novoPreco
    def setQuantidade(self, produtoid, novaQuantidade):
        self.quantidade = novaQuantidade
        return produtoDAO.setQuantidadeDAO(produtoid, novaQuantidade)
    def setCategoriaID(self, novaCategoriaID):
        self.categoriaID = novaCategoriaID
    
    def add_produto(self, nome, status, categoria, preco, qnt_min, acao):
        return produtoDAO.add_produto_DAO(nome, status, categoria, preco, qnt_min, acao)

    def editar_produto(self, nome, status, categoria, preco, qnt_min, produtoid):
        return produtoDAO.editar_produto_DAO(nome, status, categoria, preco, qnt_min, produtoid)

    def visualizar_produtos(self):
        return produtoDAO.visualizar_produtos_DAO()
    
    '''
    Desenvolver métodos de interação com o banco de dados

    def deletar_produto()
    ...    
    '''
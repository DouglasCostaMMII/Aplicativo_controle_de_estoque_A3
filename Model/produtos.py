import mysql.connector
from mysql.connector import Error
from Controller.produtosDAO import ProdutoDAO


produtoDAO = ProdutoDAO()

class Produtos:
# def fetch_produtos_data():

    def __init__(self, nome="", preco=0.0, quantidade=0, categoriaID=0):
        self.nome = nome
        # self.descricao = descricao
        self.preco = preco
        self.quantidade = quantidade
        self.categoriaID = categoriaID

    # GETS
    def getNome(self):  
        return self.nome
    # def getDescricao(self):
    #     return self.descricao
    def getPreco(self):  
        return self.preco
    def getQuantidade(self, produtoid):
        return produtoDAO.getQuantidadeDAO(produtoid)
    def getCategoriaID(self):
        return self.categoriaID
    
    #SETS
    def setNome(self, novoNome):  
        self.nome = novoNome
    # def setDescricao(self, novaDescricao):
    #     self.descricao = novaDescricao
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
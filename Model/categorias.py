from Controller.categoriasDAO import CategoriaDAO


categoriaDAO_obj = CategoriaDAO()

class Categoria:
    def __init__(self, nome="", descricao="", status=""):
        self.nome = nome
        self.descricao = descricao
        self.status = status

    # GETS
    def getCategoriaid(self, nome):
        return categoriaDAO_obj.getCategoriaidDAO(nome)
    def getNome(self, id):  
        return categoriaDAO_obj.getNomeDAO(id)
    def getDescricao(self):
        return categoriaDAO_obj.getDescricaoDAO(id)
    def getStatus(self):
        return categoriaDAO_obj.getStatusDAO(id)
    
    # SETS
    def setNome(self, id, novoNome):  
        self.nome = novoNome
        categoriaDAO_obj.setNomeDAO(id, novoNome)
    def setDescricao(self, novaDescricao):
        self.descricao = novaDescricao
        categoriaDAO_obj.setNomeDAO(id, novaDescricao)
    def setStatus(self, novoStatus):
        self.status = novoStatus
        categoriaDAO_obj.setStatusDAO(id, novoStatus)

    # CRUD
    def adicionarCategoria(nome, descricao):
        categoriaDAO_obj.adicionarCategoriaDAO(nome, descricao)

    def editar_categoria(self, id, nome, descricao):
        self.setNome(id, nome)
        self.setDescricao(id, descricao)

    def visualizarCategoria(self):
        return categoriaDAO_obj.visualizarCategoriaDAO() 

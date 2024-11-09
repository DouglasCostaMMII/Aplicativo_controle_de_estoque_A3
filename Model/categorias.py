from Controller.categoriasDAO import CategoriaDAO


categoriaDAO_obj = CategoriaDAO()

class Categoria:
    def __init__(self, nome="", status=""):
        self.nome = nome
        self.status = status

    # GETS
    def getCategoriaid(self, nome):
        return categoriaDAO_obj.getCategoriaidDAO(nome)
    def getNome(self, id):  
        return categoriaDAO_obj.getNomeDAO(id)
    def getStatus(self, categoriaid):
        return categoriaDAO_obj.getStatusDAO(categoriaid)
    
    # SETS
    def setNome(self, id, novoNome):  
        self.nome = novoNome
        categoriaDAO_obj.setNomeDAO(id, novoNome)
    def setStatus(self, categoriaid, novoStatus):
        self.status = novoStatus
        categoriaDAO_obj.setStatusDAO(categoriaid, novoStatus)
        return True

    # CRUD
    def add_Categoria(self, nome, status):
        return categoriaDAO_obj.adicionarCategoriaDAO(nome, status)

    def editar_categoria(self, nome, status, categoriaid):
        categoriaDAO_obj.setNomeDAO(categoriaid, nome)
        categoriaDAO_obj.setStatusDAO(categoriaid, status)
        return [True]

    def visualizar_Categoria(self):
        return categoriaDAO_obj.visualizarCategoriaDAO()
    
    def inativarCategoria(self):
        categoriaDAO_obj.setStatusDAO()

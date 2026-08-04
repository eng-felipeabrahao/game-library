from modelos import Jogo


class GerenciadorJogos:

    def __init__(self):
        self.jogos = []

    def adicionar(self, nome, status):
        jogo = Jogo(nome, status)
        self.jogos.append(jogo)

    def obter(self, indice):
        return self.jogos[indice]

    def atualizar(self, indice, nome, status):
        jogo = self.jogos[indice]
        jogo.atualizar(nome, status)

    def excluir(self, indice):
        self.jogos.pop(indice)

    def listar(self):
        return self.jogos
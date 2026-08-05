from banco import BancoDeDados


class GerenciadorJogos:
    """Coordena as operações relacionadas aos jogos."""

    def __init__(self):
        self.banco = BancoDeDados()

    def adicionar(self, nome: str, status: str):
        """Adiciona um jogo."""

        self.banco.adicionar_jogo(
            nome,
            status
        )

    def listar(self):
        """Retorna todos os jogos."""

        return self.banco.listar_jogos()

    def obter(self, jogo_id: int):
        """Retorna um jogo pelo ID."""

        return self.banco.obter_jogo(
            jogo_id
        )

    def atualizar(
        self,
        jogo_id: int,
        nome: str,
        status: str
    ):
        """Atualiza um jogo."""

        self.banco.atualizar_jogo(
            jogo_id,
            nome,
            status
        )

    def excluir(self, jogo_id: int):
        """Exclui um jogo."""

        self.banco.excluir_jogo(
            jogo_id
        )
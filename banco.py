from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from modelos import Base, Jogo


class BancoDeDados:
    """Responsável pela persistência dos jogos no banco de dados."""

    def __init__(self):
        # SQLite utiliza um arquivo local, não sendo necessário configurar
        # servidor, usuário ou senha para este projeto.
        self.engine = create_engine(
            "sqlite:///biblioteca.db"
        )

        # Cria as tabelas definidas nos modelos caso ainda não existam.
        Base.metadata.create_all(self.engine)

    def adicionar_jogo(self, nome: str, status: str):
        """Adiciona um novo jogo ao banco."""

        with Session(self.engine) as sessao:
            jogo = Jogo(
                nome=nome,
                status=status
            )

            sessao.add(jogo)
            sessao.commit()

    def listar_jogos(self):
        """Retorna todos os jogos cadastrados."""

        with Session(self.engine) as sessao:
            comando = select(Jogo).order_by(Jogo.id)

            resultado = sessao.scalars(comando)

            return resultado.all()

    def obter_jogo(self, jogo_id: int):
        """Retorna um jogo pelo seu identificador."""

        with Session(self.engine) as sessao:
            return sessao.get(Jogo, jogo_id)

    def atualizar_jogo(
        self,
        jogo_id: int,
        nome: str,
        status: str
    ):
        """Atualiza um jogo existente."""

        with Session(self.engine) as sessao:
            jogo = sessao.get(Jogo, jogo_id)

            if jogo is None:
                return

            jogo.atualizar(nome, status)

            sessao.commit()

    def excluir_jogo(self, jogo_id: int):
        """Remove um jogo pelo seu identificador."""

        with Session(self.engine) as sessao:
            jogo = sessao.get(Jogo, jogo_id)

            if jogo is None:
                return

            sessao.delete(jogo)
            sessao.commit()
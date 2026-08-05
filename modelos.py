from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String


class Base(DeclarativeBase):
    """Classe base para os modelos persistidos pelo SQLAlchemy."""
    pass


class Jogo(Base):
    """Representa um jogo e seu registro correspondente no banco."""

    __tablename__ = "jogos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    nome: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    def atualizar(self, nome: str, status: str):
        """Atualiza os dados do jogo em memória."""
        self.nome = nome
        self.status = status
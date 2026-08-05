from PySide6.QtCore import QAbstractTableModel, Qt


class ModeloJogos(QAbstractTableModel):

    def __init__(self, jogos=None):
        # Inicializa a classe base QAbstractTableModel.
        super().__init__()

        # Armazena a lista de jogos que será apresentada pela tabela.
        # Caso nenhuma lista seja fornecida, utiliza uma lista vazia.
        self.jogos = jogos or []

    def rowCount(self, parent=None):
        # Informa ao QTableView a quantidade de linhas do modelo.
        return len(self.jogos)

    def columnCount(self, parent=None):
        # A tabela possui duas colunas: Nome e Status.
        return 2

    def data(
        self,
        index,
        role=Qt.ItemDataRole.DisplayRole
    ):
        # Ignora índices inválidos solicitados pelo Qt.
        if not index.isValid():
            return None

        # DisplayRole representa o valor exibido visualmente na célula.
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        # Obtém o jogo correspondente à linha solicitada.
        jogo = self.jogos[index.row()]

        # A primeira coluna apresenta o nome do jogo.
        if index.column() == 0:
            return jogo.nome

        # A segunda coluna apresenta o status do jogo.
        if index.column() == 1:
            return jogo.status

        # Retorna None para colunas não definidas pelo modelo.
        return None
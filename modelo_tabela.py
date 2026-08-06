from PySide6.QtCore import QAbstractTableModel, Qt


class ModeloJogos(QAbstractTableModel):

    CABECALHOS = [
        "Nome",
        "Status"
    ]

    def __init__(self, jogos=None):
        # Inicializa a classe base QAbstractTableModel.
        super().__init__()

        # Armazena a lista de jogos que será apresentada pela tabela.
        self.jogos = jogos or []

    def rowCount(self, parent=None):
        # Informa ao QTableView a quantidade de linhas do modelo.
        return len(self.jogos)

    def columnCount(self, parent=None):
        # Retorna a quantidade de colunas definida pelo modelo.
        return len(self.CABECALHOS)

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

        if index.column() == 0:
            return jogo.nome

        if index.column() == 1:
            return jogo.status

        return None

    def headerData(
        self,
        section,
        orientation,
        role=Qt.ItemDataRole.DisplayRole
    ):
        # Define os textos exibidos nos cabeçalhos da tabela.
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            return self.CABECALHOS[section]

        return None
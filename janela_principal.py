from gerenciador_jogos import GerenciadorJogos

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QAbstractItemView
)


class JanelaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        # Mantém o estado da edição atual.
        self.linha_editando = None

        # Centraliza o acesso aos dados da aplicação.
        self.gerenciador = GerenciadorJogos()

        self.configurar_janela()
        self.criar_widgets()
        self.configurar_layout()
        self.conectar_sinais()

        # Carrega os jogos persistidos assim que a aplicação inicia.
        self.atualizar_tabela()

    def configurar_janela(self):
        self.resize(800, 600)
        self.setWindowTitle("Biblioteca de Games")

    def criar_widgets(self):

        # Widget central exigido pela QMainWindow para receber o conteúdo.
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)

        # Campo utilizado para inserir ou editar o nome do jogo.
        self.campo_texto = QLineEdit()
        self.campo_texto.setPlaceholderText(
            "Digite o nome do game"
        )

        # O mesmo botão alterna entre adicionar e salvar uma edição.
        self.botao_adicionar = QPushButton("Adicionar")

        self.botao_editar = QPushButton("Editar")
        self.botao_excluir = QPushButton("Excluir")
        self.botao_cancelar = QPushButton("Cancelar")

        # Cancelar só faz sentido durante uma edição.
        self.botao_cancelar.setEnabled(False)

        # Status disponíveis para os jogos.
        self.combo_status = QComboBox()

        self.combo_status.addItems([
            "Backlog",
            "Jogando",
            "Zerado"
        ])

        # Tabela utilizada para apresentar os jogos cadastrados.
        self.tabela = QTableWidget()

        self.tabela.setColumnCount(2)

        self.tabela.setHorizontalHeaderLabels([
            "Nome",
            "Status"
        ])

        # Faz as colunas ocuparem proporcionalmente todo o espaço disponível.
        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        # A edição dos registros será feita pelos controles da interface,
        # evitando alterações diretas que poderiam ignorar nossas regras.
        self.tabela.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

    def configurar_layout(self):

        self.layout = QVBoxLayout()

        self.widget_central.setLayout(
            self.layout
        )

        self.layout.addWidget(
            self.campo_texto
        )

        self.layout.addWidget(
            self.combo_status
        )

        self.layout.addWidget(
            self.tabela
        )

        self.layout.addWidget(
            self.botao_adicionar
        )

        self.layout.addWidget(
            self.botao_editar
        )

        self.layout.addWidget(
            self.botao_excluir
        )

        self.layout.addWidget(
            self.botao_cancelar
        )

    def conectar_sinais(self):

        self.botao_adicionar.clicked.connect(
            self.adicionar_jogo
        )

        self.botao_editar.clicked.connect(
            self.editar_jogo
        )

        self.botao_excluir.clicked.connect(
            self.excluir_jogo
        )

        self.botao_cancelar.clicked.connect(
            self.cancelar_edicao
        )

    def adicionar_jogo(self):

        nome = self.campo_texto.text().strip()
        status = self.combo_status.currentText()

        # Impede o cadastro de jogos sem nome.
        if not nome:
            return

        if self.linha_editando is None:

            self.gerenciador.adicionar(
                nome,
                status
            )

        else:

            jogo = self.obter_jogo_selecionado()

            if jogo is not None:
                self.gerenciador.atualizar(
                    jogo.id,
                    nome,
                    status
                )

            self.finalizar_edicao()

        self.atualizar_tabela()

        self.campo_texto.clear()
        self.campo_texto.setFocus()

    def atualizar_tabela(self):

        # A tabela representa o estado atual do banco, portanto é reconstruída
        # após cada operação de alteração.
        self.tabela.setRowCount(0)

        jogos = self.gerenciador.listar()

        for jogo in jogos:

            linha = self.tabela.rowCount()

            self.tabela.insertRow(linha)

            item_nome = QTableWidgetItem(
                jogo.nome
            )

            # Armazena o ID do banco no item sem exibi-lo ao usuário.
            # Isso permite identificar o registro independentemente da linha.
            item_nome.setData(
                Qt.ItemDataRole.UserRole,
                jogo.id
            )

            self.tabela.setItem(
                linha,
                0,
                item_nome
            )

            self.tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    jogo.status
                )
            )

    def obter_jogo_selecionado(self):

        linha = self.tabela.currentRow()

        if linha < 0:
            return None

        item = self.tabela.item(
            linha,
            0
        )

        jogo_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        return self.gerenciador.obter(
            jogo_id
        )

    def editar_jogo(self):

        jogo = self.obter_jogo_selecionado()

        if jogo is None:
            return

        self.linha_editando = self.tabela.currentRow()

        self.campo_texto.setText(
            jogo.nome
        )

        self.combo_status.setCurrentText(
            jogo.status
        )

        self.botao_adicionar.setText(
            "Salvar"
        )

        self.botao_cancelar.setEnabled(
            True
        )

    def cancelar_edicao(self):
        self.finalizar_edicao()

    def finalizar_edicao(self):

        self.linha_editando = None

        self.botao_adicionar.setText(
            "Adicionar"
        )

        self.botao_cancelar.setEnabled(
            False
        )

        self.campo_texto.clear()
        self.campo_texto.setFocus()

    def excluir_jogo(self):

        jogo = self.obter_jogo_selecionado()

        if jogo is None:
            return

        resposta = QMessageBox.question(
            self,
            "Confirmar exclusão",
            "Deseja realmente excluir este jogo?"
        )

        if resposta == QMessageBox.StandardButton.Yes:

            self.gerenciador.excluir(
                jogo.id
            )

            self.atualizar_tabela()
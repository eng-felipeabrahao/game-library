from gerenciador_jogos import GerenciadorJogos

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

        # Estado da aplicação
        self.linha_editando = None
        self.gerenciador = GerenciadorJogos()

        self.configurar_janela()
        self.criar_widgets()
        self.configurar_layout()
        self.conectar_sinais()

    def configurar_janela(self):
        self.resize(800, 600)
        self.setWindowTitle("Biblioteca de Games")

    def criar_widgets(self):

        # Widget central
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)

        # Campo de texto
        self.campo_texto = QLineEdit()
        self.campo_texto.setPlaceholderText(
            "Digite o nome do game"
        )

        # Botões
        self.botao_adicionar = QPushButton("Adicionar")
        self.botao_editar = QPushButton("Editar")
        self.botao_excluir = QPushButton("Excluir")
        self.botao_cancelar = QPushButton("Cancelar")

        self.botao_cancelar.setEnabled(False)

        # ComboBox
        self.combo_status = QComboBox()

        self.combo_status.addItems([
            "Backlog",
            "Jogando",
            "Zerado"
        ])

        # Tabela
        self.tabela = QTableWidget()

        self.tabela.setColumnCount(2)

        self.tabela.setHorizontalHeaderLabels([
            "Nome",
            "Status"
        ])

        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.tabela.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

    def configurar_layout(self):

        self.layout = QVBoxLayout()

        self.widget_central.setLayout(self.layout)

        self.layout.addWidget(self.campo_texto)
        self.layout.addWidget(self.combo_status)
        self.layout.addWidget(self.tabela)
        self.layout.addWidget(self.botao_adicionar)
        self.layout.addWidget(self.botao_editar)
        self.layout.addWidget(self.botao_excluir)
        self.layout.addWidget(self.botao_cancelar)

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

        if not nome:
            return

        if self.linha_editando is None:

            self.gerenciador.adicionar(
                nome,
                status
            )

        else:

            self.gerenciador.atualizar(
                self.linha_editando,
                nome,
                status
            )

            self.finalizar_edicao()

        self.atualizar_tabela()

        self.campo_texto.clear()
        self.campo_texto.setFocus()

    def atualizar_tabela(self):

        self.tabela.setRowCount(0)

        for jogo in self.gerenciador.listar():

            linha = self.tabela.rowCount()

            self.tabela.insertRow(linha)

            self.tabela.setItem(
                linha,
                0,
                QTableWidgetItem(jogo.nome)
            )

            self.tabela.setItem(
                linha,
                1,
                QTableWidgetItem(jogo.status)
            )

    def editar_jogo(self):

        linha = self.tabela.currentRow()

        if linha < 0:
            return

        self.linha_editando = linha

        jogo = self.gerenciador.obter(linha)

        self.campo_texto.setText(jogo.nome)

        self.combo_status.setCurrentText(
            jogo.status
        )

        self.botao_adicionar.setText("Salvar")
        self.botao_cancelar.setEnabled(True)

    def cancelar_edicao(self):

        self.finalizar_edicao()

    def finalizar_edicao(self):

        self.linha_editando = None

        self.botao_adicionar.setText("Adicionar")

        self.botao_cancelar.setEnabled(False)

        self.campo_texto.clear()

        self.campo_texto.setFocus()

    def excluir_jogo(self):

        linha = self.tabela.currentRow()

        if linha < 0:
            return

        resposta = QMessageBox.question(
            self,
            "Confirmar exclusão",
            "Deseja realmente excluir este jogo?"
        )

        if resposta == QMessageBox.StandardButton.Yes:

            self.gerenciador.excluir(linha)

            self.atualizar_tabela()
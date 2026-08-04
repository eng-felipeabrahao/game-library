from modelos import Jogo

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

        # Lista de jogos da aplicação
        self.jogos = []

        # Configurações da janela
        self.resize(800, 600)
        self.setWindowTitle("Biblioteca de Games")

        # Widget central
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)

        # Layout
        self.layout = QVBoxLayout()
        self.widget_central.setLayout(self.layout)

        # Campo de texto
        self.campo_texto = QLineEdit()
        self.campo_texto.setPlaceholderText("Digite o nome do game")

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

        # Faz as colunas ocuparem o espaço disponível
        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        # Impede edição direta das células
        self.tabela.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        # Layout
        self.layout.addWidget(self.campo_texto)
        self.layout.addWidget(self.combo_status)
        self.layout.addWidget(self.tabela)
        self.layout.addWidget(self.botao_adicionar)
        self.layout.addWidget(self.botao_editar)
        self.layout.addWidget(self.botao_excluir)
        self.layout.addWidget(self.botao_cancelar)

        # Sinais
        self.botao_adicionar.clicked.connect(self.adicionar_jogo)
        self.botao_editar.clicked.connect(self.editar_jogo)
        self.botao_excluir.clicked.connect(self.excluir_jogo)
        self.botao_cancelar.clicked.connect(self.cancelar_edicao)

    def adicionar_jogo(self):
        nome = self.campo_texto.text().strip()
        status = self.combo_status.currentText()

        if not nome:
            return

        # Cria um objeto Jogo
        jogo = Jogo(nome, status)

        if self.linha_editando is None:

            # Adiciona o jogo à lista
            self.jogos.append(jogo)

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

        else:
            self.tabela.setItem(
                self.linha_editando,
                0,
                QTableWidgetItem(jogo.nome)
            )

            self.tabela.setItem(
                self.linha_editando,
                1,
                QTableWidgetItem(jogo.status)
            )

            self.finalizar_edicao()

        self.campo_texto.clear()
        self.campo_texto.setFocus()

    def editar_jogo(self):
        linha = self.tabela.currentRow()

        if linha < 0:
            return

        self.linha_editando = linha

        nome = self.tabela.item(linha, 0).text()
        status = self.tabela.item(linha, 1).text()

        self.campo_texto.setText(nome)
        self.combo_status.setCurrentText(status)

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
            self.tabela.removeRow(linha)
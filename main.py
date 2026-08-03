from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTableWidget
)


class JanelaPrincipal(QMainWindow):

    def __init__(self):
        # Inicializa a classe pai, nesse caso, QMainWindow
        super().__init__()

        # Configurações da janela
        self.resize(800, 600)
        self.setWindowTitle("Biblioteca de Games")

        # Widget central
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)

        # Layout principal
        self.layout = QVBoxLayout()
        self.widget_central.setLayout(self.layout)

        # Campo de texto
        self.campo_texto = QLineEdit()
        self.campo_texto.setPlaceholderText("Digite o nome do game")

        # Botões
        self.botao_adicionar = QPushButton("Adicionar")
        self.botao_editar = QPushButton("Editar")
        self.botao_excluir = QPushButton("Excluir")
        
        # Cria o ComboBox para definição de status dos Games
        self.combo_status = QComboBox()

        # Adiciona Itens ao ComboBox
        self.combo_status.addItems([
            "Backlog",
            "Jogando",
            "Zerado"
        ])

        # Criando uma tabela para melhorar a visualização dos Games e Status
        self.tabela = QTableWidget()

        # Define o numero de colunas da tabela
        self.tabela.setColumnCount(2)

        # A tabela armazenará o nome e o status de cada jogo
        self.tabela.setHorizontalHeaderLabels([
            "Nome",
            "Status"
        ])

        # Adiciona os widgets ao layout
        self.layout.addWidget(self.campo_texto)
        self.layout.addWidget(self.combo_status)
        self.layout.addWidget(self.tabela)
        self.layout.addWidget(self.botao_adicionar)
        self.layout.addWidget(self.botao_editar)
        self.layout.addWidget(self.botao_excluir)

        # Conecta o botão ao método
        self.botao_adicionar.clicked.connect(self.adicionar_jogo)


    def adicionar_jogo(self):
        nome = self.campo_texto.text()
        status = self.combo_status.currentText()
        print(f"{nome}  =>  {status}")
        self.campo_texto.clear()
        self.campo_texto.setFocus()


# Cria a aplicação
app = QApplication([])

# Cria a janela
janela = JanelaPrincipal()

# Mostra a janela
janela.show()

# Executa a aplicação
app.exec()
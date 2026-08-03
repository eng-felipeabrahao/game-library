from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem
)


class JanelaPrincipal(QMainWindow):

    def __init__(self):
        # Inicializa a classe pai, nesse caso, QMainWindow
        super().__init__()

        # Variável para armazenar a linha que está sendo editada
        self.linha_editando = None

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
        self.botao_cancelar = QPushButton("Cancelar")
        
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
        self.layout.addWidget(self.botao_cancelar)

        # Desabilita o botão de cancelar a edição inicialmente
        self.botao_cancelar.setEnabled(False)
        

        # Conecta o botão ao método
        self.botao_adicionar.clicked.connect(self.adicionar_jogo)
        self.botao_editar.clicked.connect(self.editar_jogo)
        self.botao_cancelar.clicked.connect(self.cancelar_edicao)


    def adicionar_jogo(self):
        nome = self.campo_texto.text().strip()
        status = self.combo_status.currentText()

        # Cria validação dos dados, impedindo a inserção de células vazias
        if not nome:
            return

        # Verifica se estamos editando uma linha existente ou adicionando uma nova
        if self.linha_editando is None:
            linha = self.tabela.rowCount()
            self.tabela.insertRow(linha)
            self.tabela.setItem(
                linha,
                0,
                QTableWidgetItem(nome)
            )
            self.tabela.setItem(
                linha,
                1,
                QTableWidgetItem(status)
            )
        # Se estivermos editando, atualiza os valores da linha existente
        else:
            self.tabela.setItem(
                self.linha_editando,
                0,
                QTableWidgetItem(nome)
            )
            self.tabela.setItem(
                self.linha_editando,
                1,
                QTableWidgetItem(status)
            )

            # Altera o texto do botão de volta para "Adicionar"
            self.botao_adicionar.setText("Adicionar")

            # Limpa a variável de edição após atualizar a linha
            self.linha_editando = None

            # Desabilita o botão de cancelar a edição após salvar as alterações
            self.botao_cancelar.setEnabled(False)

        self.campo_texto.clear()
        self.campo_texto.setFocus()

    def editar_jogo(self):
        # Obtém a linha selecionada na tabela
        linha = self.tabela.currentRow()

        # Valida se a linha selecionada é válida
        if linha < 0:
            return

        # Armazena a linha que está sendo editada
        self.linha_editando = linha

        # Obtém os valores da linha selecionada
        nome = self.tabela.item(linha, 0).text()
        status = self.tabela.item(linha, 1).text()

        # Atualiza os campos de texto e combo box com os valores da linha selecionada
        self.campo_texto.setText(nome)
        self.combo_status.setCurrentText(status)

        # Altera o texto do botão para indicar que estamos salvando uma edição
        self.botao_adicionar.setText("Salvar")

        # Habilita o botão de cancelar a edição
        self.botao_cancelar.setEnabled(True)

    def cancelar_edicao(self):
        # Limpa a variável de edição, indicando que não estamos mais editando nenhuma linha
        self.linha_editando = None

        # Altera o texto do botão de volta para "Adicionar"
        self.botao_adicionar.setText("Adicionar")

        # Desabilita o botão de cancelar a edição
        self.botao_cancelar.setEnabled(False)

        # Limpa o campo de texto e retorna o foco para ele
        self.campo_texto.clear()

        # Retorna o foco para o campo de texto
        self.campo_texto.setFocus()


# Cria a aplicação
app = QApplication([])

# Cria a janela
janela = JanelaPrincipal()

# Mostra a janela
janela.show()

# Executa a aplicação
app.exec()


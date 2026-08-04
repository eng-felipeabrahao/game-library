from PySide6.QtWidgets import QApplication

from janela_principal import JanelaPrincipal


app = QApplication([])

janela = JanelaPrincipal()

janela.show()

app.exec()
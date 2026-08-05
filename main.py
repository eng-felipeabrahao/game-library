from PySide6.QtWidgets import QApplication

from janela_principal import JanelaPrincipal


def main():
    """Inicializa e executa a aplicação."""

    app = QApplication([])

    janela = JanelaPrincipal()
    janela.show()

    app.exec()


if __name__ == "__main__":
    main()
import os
from PyQt5 import QtWidgets, QtCore, QtGui

class JanelaMinimizada(QtWidgets.QWidget):
    restaurar_sinal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Configurações da janela minimizada
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.Tool)

        # Torna o fundo transparente
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Ícone redondo
        tamanho_icone = 50
        self.setFixedSize(tamanho_icone, tamanho_icone)

        # Cria uma label para o ícone
        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet('''
            QLabel {
                background-color: rgba(0, 122, 204, 0.6);
                border-radius: %dpx;
            }
        ''' % (tamanho_icone // 2))
        self.label.setFixedSize(tamanho_icone, tamanho_icone)

        # Adiciona um ícone à label (opcional)
        script_dir = os.path.dirname(os.path.realpath(__file__))
        icon_path = os.path.join(script_dir, 'icon1.png')
        if os.path.exists(icon_path):
            pixmap = QtGui.QPixmap(icon_path).scaled(30, 30, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.label.setPixmap(pixmap)
        else:
            self.label.setText("Icon")

        # Variáveis para arrastar a janela
        self.offset = None

    def mousePressEvent(self, event):
        """Evento de pressionar o mouse para iniciar o arraste."""
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        """Evento de movimento do mouse para arrastar a janela."""
        if event.buttons() == QtCore.Qt.LeftButton and self.offset is not None:
            self.move(event.globalPos() - self.offset)

    def mouseDoubleClickEvent(self, event):
        """Evento de duplo clique para restaurar a janela principal."""
        if event.button() == QtCore.Qt.LeftButton:
            self.restaurar_sinal.emit()
            self.close()

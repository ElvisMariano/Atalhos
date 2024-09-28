import os
import webbrowser
import functools
import subprocess
from PyQt5 import QtWidgets, QtCore, QtGui
from janela_minimizada import JanelaMinimizada
from configuracao_dialog import ConfiguracaoDialog

class JanelaSobreposta(QtWidgets.QWidget):
    """Janela principal que exibe os atalhos de forma sobreposta."""
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint |
                            QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.Tool)

        # Torna o fundo transparente
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Variável para armazenar o deslocamento do mouse
        self.offset = None

        # Limita o tamanho máximo da janela
        self.setFixedSize(150, 250)  # Ajuste o tamanho conforme necessário

        # Cria um layout principal
        layout_principal = QtWidgets.QVBoxLayout(self)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # Cria um widget central
        self.widget_central = QtWidgets.QWidget(self)
        self.widget_central.setStyleSheet('''
            QWidget {
                background-color: rgba(30, 30, 30, 0.9);
                border-radius: 10px;
            }
        ''')

        # Adiciona o widget central ao layout principal
        layout_principal.addWidget(self.widget_central)

        # Cria um layout para o widget central
        layout_central = QtWidgets.QVBoxLayout(self.widget_central)
        layout_central.setContentsMargins(5, 5, 5, 5)
        layout_central.setSpacing(5)

        # Cria um layout horizontal para os botões e ícone da empresa
        layout_botoes = QtWidgets.QHBoxLayout()
        layout_botoes.setContentsMargins(0, 0, 0, 0)  # Ajuste das margens
        layout_botoes.setSpacing(5)

        # Ícone da empresa
        label_logo = QtWidgets.QLabel(self)
        # Caminho para o ícone da empresa
        script_dir = os.path.dirname(os.path.realpath(__file__))
        icon_path = os.path.join(script_dir, 'company_icon.png')
        if os.path.exists(icon_path):
            pixmap_logo = QtGui.QPixmap(icon_path).scaled(30, 30, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            label_logo.setPixmap(pixmap_logo)
        else:
            label_logo.setText("Logo")
        label_logo.setFixedSize(30, 30)

        # Botão de configuração
        botao_configuracao = QtWidgets.QPushButton('', self)
        botao_configuracao.setFixedSize(15, 15)
        botao_configuracao.setStyleSheet('''
            QPushButton {
                background-color: #28a745;
                border: none;
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        ''')
        botao_configuracao.clicked.connect(self.abrir_configuracao)

        # Botão de minimizar
        botao_minimizar = QtWidgets.QPushButton('', self)
        botao_minimizar.setFixedSize(15, 15)
        botao_minimizar.setStyleSheet('''
            QPushButton {
                background-color: #ffbd2e;
                border: none;
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: #ff9500;
            }
        ''')
        botao_minimizar.clicked.connect(self.minimizar)

        # Botão de fechar
        botao_fechar = QtWidgets.QPushButton('', self)
        botao_fechar.setFixedSize(15, 15)
        botao_fechar.setStyleSheet('''
            QPushButton {
                background-color: #ff5f56;
                border: none;
                border-radius: 7px;
            }
            QPushButton:hover {
                background-color: #ff1b0a;
            }
        ''')
        botao_fechar.clicked.connect(self.close)

        # Adiciona o ícone da empresa ao layout
        layout_botoes.addWidget(label_logo, alignment=QtCore.Qt.AlignLeft)

        # Preenche o espaço restante
        layout_botoes.addStretch()

        # Adicionando os botões (configuração, minimizar, fechar)
        layout_botoes.addWidget(botao_configuracao, alignment=QtCore.Qt.AlignRight)
        layout_botoes.addWidget(botao_minimizar, alignment=QtCore.Qt.AlignRight)
        layout_botoes.addWidget(botao_fechar, alignment=QtCore.Qt.AlignRight)

        # Adiciona o layout dos botões ao layout central
        layout_central.addLayout(layout_botoes)

        # Cria um layout para os botões de atalhos
        self.layout_botoes_atalho = QtWidgets.QVBoxLayout()
        self.layout_botoes_atalho.setSpacing(5)
        self.layout_botoes_atalho.setContentsMargins(0, 0, 0, 0)

        # Inicializa os sites
        self.sites = {}
        self.carregar_configuracao()
        self.criar_botoes_atalho()

        # Adiciona o layout dos botões de atalho ao layout central
        layout_central.addLayout(self.layout_botoes_atalho)

        # Centraliza os elementos
        layout_central.addStretch()

        # Ícone da bandeja do sistema
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        tray_icon_path = os.path.join(script_dir, 'icon_tray.png')
        if os.path.exists(tray_icon_path):
            self.tray_icon.setIcon(QtGui.QIcon(tray_icon_path))
        else:
            self.tray_icon.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_ComputerIcon))

        tray_menu = QtWidgets.QMenu()
        restaurar_acao = tray_menu.addAction("Restaurar")
        restaurar_acao.triggered.connect(self.show)
        sair_acao = tray_menu.addAction("Sair")
        sair_acao.triggered.connect(QtWidgets.QApplication.quit)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()

        # Conecta ao sinal screenChanged após a janela ser totalmente inicializada
        QtCore.QTimer.singleShot(0, self.conectar_sinal_tela)

        # Suporte a arrastar e soltar
        self.setAcceptDrops(True)

        # Variável para armazenar o ícone minimizado
        self.icone_minimizado = None

    def conectar_sinal_tela(self):
        """Conecta o sinal de mudança de tela."""
        window_handle = self.windowHandle()
        if window_handle is not None:
            window_handle.screenChanged.connect(self.atualizar_tela)

    def atualizar_tela(self):
        """Atualiza a tela quando há mudança."""
        self.adjustSize()

    def abrir_site(self, url):
        """Abre o site ou executa o aplicativo dado o URL ou caminho."""
        if url.startswith('http://') or url.startswith('https://'):
            webbrowser.open(url)
        elif os.path.exists(url):
            subprocess.Popen([url], shell=True)
        else:
            QtWidgets.QMessageBox.warning(self, 'Erro', f'Não foi possível abrir o atalho.\n{url}')

    def criar_botoes_atalho(self):
        """Cria os botões de atalho com base nos sites carregados."""
        for nome, url in self.sites.items():
            botao = QtWidgets.QPushButton(nome, self)
            botao.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            botao.setFixedHeight(30)
            botao.setStyleSheet('''
                QPushButton {
                    background-color: #007ACC;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #005F8C;
                }
            ''')
            botao.clicked.connect(functools.partial(self.abrir_site, url))
            self.layout_botoes_atalho.addWidget(botao)
        # Adiciona um espaçamento esticável no final para empurrar os botões para cima
        self.layout_botoes_atalho.addStretch()

    def atualizar_botoes_atalho(self):
        """Atualiza os botões de atalho após mudanças na configuração."""
        # Remove os botões existentes
        while self.layout_botoes_atalho.count():
            item = self.layout_botoes_atalho.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        # Recria os botões
        self.criar_botoes_atalho()

    def carregar_configuracao(self):
        """Carrega a configuração usando QSettings."""
        settings = QtCore.QSettings('SuaEmpresa', 'Atalhos')
        self.sites = settings.value('sites', self.obter_sites_padrao())

    def salvar_configuracao(self):
        """Salva a configuração usando QSettings."""
        settings = QtCore.QSettings('SuaEmpresa', 'Atalhos')
        settings.setValue('sites', self.sites)

    def obter_sites_padrao(self):
        """Retorna um dicionário com os sites padrão."""
        return {
            'PLM': 'PLM//',
            'CRYSTAL': 'CR//',
            'POPULIS': 'https://autoliv.populisservicos.com.br/',
            'PARTS': 'Parts//',
            'CHATGPT': 'https://chat.openai.com/',
            'GCWIN': r'\\brgo-gcwinmon01\programs_brgo\GCWin\GCWin.exe'
        }

    def mousePressEvent(self, event):
        """Evento de pressionar o mouse para iniciar o arraste da janela."""
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        """Evento de movimento do mouse para arrastar a janela."""
        if event.buttons() == QtCore.Qt.LeftButton and self.offset is not None:
            # Movimento suavizado
            delta = event.pos() - self.offset
            self.move(self.pos() + delta)

    def minimizar(self):
        """Minimiza a janela para um ícone redondo."""
        self.hide()
        self.icone_minimizado = JanelaMinimizada()
        self.icone_minimizado.restaurar_sinal.connect(self.restaurar)
        # Posiciona o ícone minimizado próximo à posição da janela principal
        self.icone_minimizado.move(self.x(), self.y())
        self.icone_minimizado.show()

    def restaurar(self):
        """Restaura a janela a partir do ícone minimizado."""
        self.show()
        if self.icone_minimizado:
            self.icone_minimizado.close()
            self.icone_minimizado = None

    def abrir_configuracao(self):
        """Abre a janela de configuração dos atalhos."""
        dialog = ConfiguracaoDialog(self.sites, self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.sites = dialog.get_sites()
            self.salvar_configuracao()
            self.atualizar_botoes_atalho()

    def on_tray_icon_activated(self, reason):
        """Evento quando o ícone da bandeja é ativado."""
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.show()

    def dragEnterEvent(self, event):
        """Evento ao arrastar algo para a janela."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Evento ao soltar algo na janela."""
        for url in event.mimeData().urls():
            caminho = url.toLocalFile()
            nome = os.path.basename(caminho)
            if os.path.exists(caminho):
                self.sites[nome] = caminho
                self.salvar_configuracao()
                self.atualizar_botoes_atalho()

    def verificar_atualizacoes(self):
        """Verifica se há atualizações disponíveis."""
        # Implementação simples de verificação de atualizações
        # Aqui você pode implementar a lógica para verificar atualizações em um servidor
        pass

    def closeEvent(self, event):
        """Evento chamado quando a janela é fechada."""
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Aplicativo em execução",
            "O aplicativo continua em execução na bandeja do sistema.",
            QtWidgets.QSystemTrayIcon.Information,
            1000
        )

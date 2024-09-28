import sys
import locale
from PyQt5 import QtWidgets, QtCore
from janela_sobreposta import JanelaSobreposta

def main():
    # Habilitar suporte a High DPI
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    # Configuração de internacionalização (i18n)
    locale_lang, _ = locale.getdefaultlocale()
    app = QtWidgets.QApplication(sys.argv)
    translator = QtCore.QTranslator()
    # Supondo que exista um arquivo de tradução 'app_pt_BR.qm'
    if translator.load(f'app_{locale_lang}.qm'):
        app.installTranslator(translator)

    janela = JanelaSobreposta()
    janela.show()

    # Verifica atualizações ao iniciar
    janela.verificar_atualizacoes()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

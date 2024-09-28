import os
from PyQt5 import QtWidgets, QtCore

class ConfiguracaoDialog(QtWidgets.QDialog):
    """Janela de diálogo para configuração dos atalhos."""
    def __init__(self, sites, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Configuração de Atalhos')

        self.resize(400, 300)
        self.sites = sites.copy()

        layout = QtWidgets.QVBoxLayout(self)

        # Tabela para mostrar os atalhos
        self.table = QtWidgets.QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Nome', 'URL'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setAlternatingRowColors(True)

        layout.addWidget(self.table)

        # Botões para Adicionar, Editar, Remover
        btn_layout = QtWidgets.QHBoxLayout()

        btn_add = QtWidgets.QPushButton('Adicionar')
        btn_edit = QtWidgets.QPushButton('Editar')
        btn_remove = QtWidgets.QPushButton('Remover')

        btn_add.clicked.connect(self.adicionar_atalho)
        btn_edit.clicked.connect(self.editar_atalho)
        btn_remove.clicked.connect(self.remover_atalho)

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_remove)

        layout.addLayout(btn_layout)

        # Botões OK e Cancelar
        btn_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

        self.carregar_sites()

    def carregar_sites(self):
        """Carrega os sites na tabela."""
        self.table.setRowCount(0)
        for nome, url in self.sites.items():
            row = self.table.rowCount()
            self.table.insertRow(row)
            nome_item = QtWidgets.QTableWidgetItem(nome)
            url_item = QtWidgets.QTableWidgetItem(url)
            self.table.setItem(row, 0, nome_item)
            self.table.setItem(row, 1, url_item)

    def adicionar_atalho(self):
        """Adiciona um novo atalho."""
        dialog = AtalhoDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            nome, url = dialog.get_data()
            if nome in self.sites:
                QtWidgets.QMessageBox.warning(self, 'Erro', 'Um atalho com este nome já existe.')
                return
            self.sites[nome] = url
            self.carregar_sites()

    def editar_atalho(self):
        """Edita o atalho selecionado."""
        selected = self.table.currentRow()
        if selected >= 0:
            nome_item = self.table.item(selected, 0)
            url_item = self.table.item(selected, 1)
            nome = nome_item.text()
            url = url_item.text()

            dialog = AtalhoDialog(self, nome, url)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                novo_nome, novo_url = dialog.get_data()
                # Remove a entrada antiga se o nome mudou
                if nome != novo_nome:
                    del self.sites[nome]
                self.sites[novo_nome] = novo_url
                self.carregar_sites()
        else:
            QtWidgets.QMessageBox.warning(self, 'Editar Atalho', 'Selecione um atalho para editar.')

    def remover_atalho(self):
        """Remove o atalho selecionado."""
        selected = self.table.currentRow()
        if selected >= 0:
            nome_item = self.table.item(selected, 0)
            nome = nome_item.text()
            confirm = QtWidgets.QMessageBox.question(self, 'Remover Atalho', f'Deseja remover o atalho "{nome}"?')
            if confirm == QtWidgets.QMessageBox.Yes:
                del self.sites[nome]
                self.carregar_sites()
        else:
            QtWidgets.QMessageBox.warning(self, 'Remover Atalho', 'Selecione um atalho para remover.')

    def get_sites(self):
        """Retorna os sites atualizados."""
        return self.sites

class AtalhoDialog(QtWidgets.QDialog):
    """Janela de diálogo para adicionar ou editar um atalho."""
    def __init__(self, parent=None, nome='', url=''):
        super().__init__(parent)
        self.setWindowTitle('Adicionar/Editar Atalho')

        layout = QtWidgets.QFormLayout(self)

        self.nome_edit = QtWidgets.QLineEdit(self)
        self.nome_edit.setText(nome)
        self.url_edit = QtWidgets.QLineEdit(self)
        self.url_edit.setText(url)

        layout.addRow('Nome:', self.nome_edit)
        layout.addRow('URL:', self.url_edit)

        btn_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.validar)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def validar(self):
        """Valida os dados inseridos."""
        nome = self.nome_edit.text().strip()
        url = self.url_edit.text().strip()
        if nome and url:
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, 'Erro', 'Por favor, preencha ambos os campos.')

    def get_data(self):
        """Retorna o nome e URL inseridos."""
        return self.nome_edit.text().strip(), self.url_edit.text().strip()

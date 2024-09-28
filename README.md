
# Aplicativo de Atalhos Personalizados

Um aplicativo em Python que fornece uma interface sobreposta para acessar rapidamente sites e aplicativos favoritos. A interface é minimalista e sempre fica no topo das outras janelas, permitindo acesso fácil e rápido aos seus atalhos personalizados.

---

## 📋 Sumário

- [Funcionalidades](#funcionalidades)
- [Capturas de Tela](#capturas-de-tela)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Personalização](#personalização)
- [Contribuindo](#contribuindo)
- [Licença](#licença)
- [Contato](#contato)

---

## 🛠 Funcionalidades

- **Interface Sobreposta**: Janela sempre no topo, com design minimalista.
- **Atalhos Personalizáveis**: Adicione, edite ou remova atalhos para sites ou aplicativos.
- **Minimização para Ícone**: Ao minimizar, transforma-se em um ícone redondo na tela.
- **Bandeja do Sistema**: Permanece ativo na bandeja do sistema quando fechado.
- **Arrastar e Soltar**: Suporte para drag and drop para adicionar novos atalhos.
- **Internacionalização (i18n)**: Suporte para múltiplos idiomas usando `QTranslator`.
- **Atualização Automática (Esboço)**: Estrutura pronta para implementar verificação de atualizações.

---

## 📸 Capturas de Tela

*Nota: Inclua aqui imagens ou GIFs mostrando o aplicativo em funcionamento.*

---

## ⚙️ Pré-requisitos

- **Python 3.6 ou superior**
- **PyQt5**: Biblioteca para criar interfaces gráficas.

---

## 🚀 Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/ElvisMariano/atalhos.git
   ```

2. **Navegue até o diretório do projeto:**

   ```bash
   cd app-de-atalhos
   ```

3. **Crie um ambiente virtual (opcional, mas recomendado):**

   ```bash
   python -m venv venv
   ```

4. **Ative o ambiente virtual:**

   - **Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **Linux/MacOS:**

     ```bash
     source venv/bin/activate
     ```

5. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

   *Nota: Certifique-se de que o arquivo `requirements.txt` contenha `PyQt5`.*

---

## 🎮 Uso

1. **Execute o aplicativo:**

   ```bash
   python main.py
   ```

2. **Interface Principal:**

   - A janela principal aparecerá sobreposta às outras janelas.
   - Use os botões de atalho para abrir sites ou aplicativos.

3. **Minimizar:**

   - Clique no botão amarelo para minimizar.
   - A janela se transformará em um ícone redondo que pode ser movido pela tela.
   - Dê um duplo clique no ícone para restaurar a janela principal.

4. **Fechar:**

   - Clique no botão vermelho para fechar.
   - O aplicativo permanecerá em execução na bandeja do sistema.
   - Clique no ícone da bandeja para restaurar.

---

## 🎨 Personalização

### Adicionar, Editar ou Remover Atalhos

1. **Acessar as Configurações:**

   - Clique no botão verde (configurações) na janela principal.

2. **Adicionar Atalho:**

   - Clique em *Adicionar*.
   - Insira o Nome e a URL ou caminho do aplicativo.
   - Clique em *OK*.

3. **Editar Atalho:**

   - Selecione um atalho na lista.
   - Clique em *Editar*.
   - Modifique o Nome e/ou a URL.
   - Clique em *OK*.

4. **Remover Atalho:**

   - Selecione um atalho na lista.
   - Clique em *Remover*.
   - Confirme a remoção.

### Arrastar e Soltar

1. **Adicionar Atalho Rápido:**

   - Arraste um arquivo executável ou atalho da área de trabalho diretamente para a janela principal.
   - O atalho será automaticamente adicionado com o nome do arquivo.

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir *issues* para reportar bugs ou sugerir melhorias. Para contribuir com código:

1. Faça um *fork* do projeto.
2. Crie uma *branch* para sua feature:

   ```bash
   git checkout -b minha-feature
   ```

3. *Commit* suas alterações:

   ```bash
   git commit -m 'Adiciona nova funcionalidade'
   ```

4. Faça o *push* para a branch:

   ```bash
   git push origin minha-feature
   ```

5. Abra um *Pull Request*.

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 📧 Contato

- **Nome:** Elvis Mariano
- **Email:** [admelvismariano@gmail.com](mailto:admelvismariano@gmail.com)
- **GitHub:** [ElvisMariano](https://github.com/ElvisMariano)

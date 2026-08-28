# Leitor de Projetos -- English

**What it does**
Transforms a source‑code project into plain‑text files that can be read by AI tools, documentation generators, or shared with teammates.

## Quick start (source version)
1. **Clone or download the repository**
   ```bash
   git clone https://github.com/SEU_USUARIO/Leitor-de-projetos.git
   cd Leitor-de-projetos
   ```
2. **Install the required package** (only `pyinstaller` is needed for building the executable; the app itself uses only the Python standard library)
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # on Windows
   pip install -r requirements.txt   # if you have a requirements file, otherwise just `pip install pyinstaller`
   ```
3. **Run the GUI**
   ```bash
   python LeitorDeProjetos/main.py
   ```
   The window lets you select a project folder, choose the processing mode (single file or separate files), and optionally pick which files to include via the *Pré‑visualizar* step.

## Running the compiled executable
If you prefer not to install Python, you can use the pre‑built **LeitorDeProjetos.exe**:
1. Download the `.exe` from the latest GitHub **Release** (see the *Releases* tab of the repository).
2. Double‑click the file – no installation or configuration is required. The first time it runs Windows may show a warning about an unknown publisher; click *Run anyway*.

## Building the .exe yourself (optional)
```bash
pyinstaller --onefile --windowed --name LeitorDeProjetos LeitorDeProjetos/main.py
```
The resulting `dist/LeitorDeProjetos.exe` can be uploaded as a release asset.

## Publishing the executable on GitHub
1. **Create a release** on GitHub (Releases → *Draft a new release*).
2. Give it a tag, e.g. `v1.0.0`, and a title.
3. Drag the `LeitorDeProjetos.exe` file into the *Attach binaries* area and publish the release.
   Users can then download the single executable without needing any other files.

## Configuration (optional)
The application stores its settings (last used folder, selected mode, window size, etc.) in a JSON file located next to the script/executable. You can edit it manually if you need to change defaults, but the GUI already provides a *Configurações* dialog for adding/removing file extensions and ignored folders/files.

---
*Feel free to open an issue or submit a pull request if you find bugs or want new features.*


# Leitor de Projetos -- Português

## O que ele faz

Transforma um projeto de código-fonte em arquivos de texto simples que podem ser lidos por ferramentas de IA, geradores de documentação ou compartilhados com outros desenvolvedores.

## Início rápido (versão do código-fonte)

1. **Clone ou baixe o repositório**

   ```bash
   git clone https://github.com/SEU_USUARIO/Leitor-de-projetos.git
   cd Leitor-de-projetos
   ```

2. **Instale o pacote necessário**

   Apenas o `pyinstaller` é necessário para criar o executável. O aplicativo em si utiliza apenas a biblioteca padrão do Python.

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # no Windows
   pip install -r requirements.txt   # se você tiver um arquivo requirements.txt; caso contrário, use `pip install pyinstaller`
   ```

3. **Execute a interface gráfica**

   ```bash
   python LeitorDeProjetos/main.py
   ```

   A janela permite selecionar uma pasta de projeto, escolher o modo de processamento (arquivo único ou arquivos separados) e, opcionalmente, selecionar quais arquivos incluir através da etapa **Pré-visualizar**.

## Executando o executável compilado

Se você preferir não instalar o Python, pode utilizar o **LeitorDeProjetos.exe** pré-compilado:

1. Baixe o `.exe` na **Release** mais recente do GitHub (na aba **Releases** do repositório).
2. Dê dois cliques no arquivo — nenhuma instalação ou configuração é necessária.
3. Na primeira execução, o Windows pode exibir um aviso sobre um editor desconhecido. Clique em **Executar assim mesmo**.

## Criando o `.exe` por conta própria (opcional)

```bash
pyinstaller --onefile --windowed --name LeitorDeProjetos LeitorDeProjetos/main.py
```

O arquivo resultante, `dist/LeitorDeProjetos.exe`, pode ser enviado como um arquivo da release.

## Publicando o executável no GitHub

1. **Crie uma release** no GitHub: Releases → **Draft a new release**.
2. Defina uma tag, por exemplo `v1.0.0`, e um título.
3. Arraste o arquivo `LeitorDeProjetos.exe` para a área **Attach binaries** e publique a release.

Os usuários poderão então baixar apenas o executável, sem precisar instalar nenhum outro arquivo.

## Configuração (opcional)

O aplicativo armazena suas configurações (última pasta utilizada, modo selecionado, tamanho da janela etc.) em um arquivo JSON localizado ao lado do script ou executável.

Você pode editá-lo manualmente caso precise alterar os valores padrão, mas a interface gráfica já oferece uma janela de **Configurações** para adicionar ou remover extensões de arquivos e pastas/arquivos ignorados.

---

Sinta-se à vontade para abrir uma issue ou enviar um pull request caso encontre algum problema ou queira sugerir novas funcionalidades.

# Project Reading Tools -- English

Two simple Python scripts for reading projects and transforming their files into formats that are easier to view, share, or send to AI tools.

## `ler_projeto_separado.py`

Scans a project folder and generates a single `.txt` file containing the folder structure and the contents of the selected files.

Useful for:

* Sending an entire project to an AI.
* Viewing the structure and contents of a project in a single file.
* Quickly creating a text-based copy of a project.
* Analyzing projects without having to open files one by one.

Supports configuring which file extensions should be read and which folders should be ignored.

## `ler_projeto_junto.py`

Scans a project folder and copies the selected files into a new folder, converting each file into a separate `.txt` file.

Useful for:

* Converting source code into text files.
* Preparing projects for sharing or analysis.
* Automatically separating different source-code files.
* Making it easier to convert files to other formats.

The file extensions and ignored folders can be configured directly in the code.

## Requirements

* Python 3.x
* Windows

No external libraries are required.

## Usage

Open the desired script, configure the project folder path in `pasta_principal`, and run the script.

The generated files are automatically saved to the Desktop.

## Note

The scripts only process text and source-code files with the configured extensions. Images and other binary files are not processed.


# Ferramentas de Leitura de Projetos -- Português

Dois scripts Python simples para ler projetos e transformar seus arquivos em formatos mais fáceis de visualizar, compartilhar ou enviar para IAs.

## ler_projeto_separado.py

Percorre uma pasta de projeto e gera um único arquivo `.txt` contendo a estrutura das pastas e o conteúdo dos arquivos selecionados.

É útil para:

- Enviar um projeto inteiro para uma IA.
- Visualizar a estrutura e o conteúdo de um projeto em um único arquivo.
- Criar rapidamente uma cópia textual do projeto.
- Analisar projetos sem precisar abrir arquivo por arquivo.

Possui suporte para definir quais extensões serão lidas e quais pastas serão ignoradas.

## ler_projeto_junto.py

Percorre uma pasta de projeto e copia os arquivos selecionados para uma nova pasta, convertendo cada arquivo em um `.txt` separado.

É útil para:

- Transformar códigos em arquivos de texto.
- Preparar projetos para envio ou análise.
- Separar automaticamente diferentes arquivos de código.
- Facilitar a conversão dos arquivos para outros formatos.

As extensões e pastas ignoradas podem ser configuradas diretamente no código.

## Requisitos

- Python 3.x
- Windows

Nenhuma biblioteca externa é necessária.

## Uso

Abra o arquivo desejado, configure o caminho da pasta do projeto em `pasta_principal` e execute o script.

Os arquivos gerados são salvos automaticamente na Área de Trabalho.

## Observação

Os scripts trabalham apenas com arquivos de texto e código definidos nas extensões configuradas. Imagens e outros arquivos binários não são processados.
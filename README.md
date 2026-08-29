# Project Reader -- English

A tool for transforming code projects into organized text files, making it easier to read, analyze, document, and send projects to Artificial Intelligence tools.

The project was created to simplify the process of gathering the contents of multiple project files into a format that can be easily viewed and shared.

## What is it for?

When working with programming projects, you may need to analyze or send multiple files at once.

Project Reader makes this process easier by gathering project information into text files.

Some possible uses include:

* Analyzing an entire project at once;
* Sending project contents to an AI;
* Sharing the structure and source code of a project;
* Making code reviews easier;
* Creating a textual representation of a project;
* Organizing project contents for documentation.

## How does it work?

The tool scans the selected project and processes its files according to the configured settings.

The result is one or more text files containing the information needed to view and analyze the project without having to open every file individually.

This can be particularly useful when working with AI tools, where providing the complete context of a project can make analysis much easier.

## How to use

There are two main ways to use the project.

### Executable

For users who do not have Python installed, or simply want to use the tool directly, the compiled **LeitorDeProjetos-1.0.3.exe** is available.

Open the repository's [**Releases** page](https://github.com/ink-creator/Leitor-de-projetos/releases), select the latest release and download the `.exe` under **Assets**.

This is the recommended option for users who only want to use the program without modifying its source code.

### Source code

You can also use the project directly from its source code.

This option is better suited for users who want to study, modify, or adapt the tool to their own needs.

The main source code is located in:

```text
LeitorDeProjetos/
```

## Manual method

The project also contains a folder called `manual`.

This folder is not part of an automatic process performed by the program. Its purpose is to provide a way to perform the process manually, without depending on the tool.

```text
manual/
```

This can be useful when you want more control over which files are gathered or simply want to understand the process behind the tool.

## Project structure

```text
Leitor-de-projetos/
│
├── .github/
│   └── workflows/
│
├── LeitorDeProjetos/
│
├── manual/
│
├── .gitignore
│
└── README.md
```

### `LeitorDeProjetos`

Contains the program's source code.

### `manual`

Contains materials related to the manual process of reading and organizing project files.

### `.github/workflows`

Contains the files used by GitHub workflows.

## Using it with Artificial Intelligence

One of the main purposes of the project is to make working with code projects and Artificial Intelligence tools easier.

Instead of having to select and send many files individually, the project allows the contents to be prepared in a more organized way.

For example:

```text
Project
    |
    v
Project Reader
    |
    v
Text file
    |
    v
AI tool
    |
    v
Project analysis
```

This can be useful for tasks such as:

* Code analysis;
* Finding problems;
* Improvement suggestions;
* Project explanations;
* Documentation;
* Refactoring;
* Understanding project structure.

## Be careful when sharing projects

Before sending generated files to an AI or another person, review the project contents.

Text files generated from a project may contain information that should not be shared, such as:

```text
Passwords
API Keys
Tokens
Credentials
Personal information
Private keys
Sensitive configuration
```

Always review the generated content before sharing it.

## Technologies

The project was developed in Python.

A compiled `.exe` version is also available to make the tool easier to use for people who do not have a Python environment configured.

## Status

Project in development.

The goal is to keep Project Reader as a small, practical, and easy-to-use tool that can receive new features as new needs arise.

License

This project is available under the MIT License.

See the LICENSE file for more information.

------

# Leitor de Projetos -- Português

Uma ferramenta para transformar projetos de código em arquivos de texto organizados, facilitando a leitura, análise, documentação e o envio de projetos para ferramentas de Inteligência Artificial.

O projeto foi desenvolvido para tornar mais simples a tarefa de reunir o conteúdo de vários arquivos de um projeto em um formato que possa ser visualizado e compartilhado facilmente.

## Para que serve?

Ao trabalhar com projetos de programação, pode ser necessário analisar ou enviar vários arquivos de uma só vez.

O Leitor de Projetos facilita esse processo ao reunir as informações do projeto em arquivos de texto.

Alguns exemplos de uso:

* Analisar um projeto inteiro de uma vez;
* Enviar o conteúdo de um projeto para uma IA;
* Compartilhar a estrutura e o código de um projeto;
* Facilitar revisões de código;
* Criar uma representação textual de um projeto;
* Organizar o conteúdo de projetos para documentação.

## Como funciona?

A ferramenta percorre o projeto selecionado e trabalha com seus arquivos de acordo com as configurações definidas.

O resultado é um ou mais arquivos de texto contendo as informações necessárias para visualizar e analisar o projeto sem precisar abrir cada arquivo individualmente.

Isso pode ser especialmente útil ao trabalhar com ferramentas de IA, nas quais fornecer o contexto completo de um projeto pode facilitar bastante a análise.

## Como utilizar

Existem duas formas principais de utilizar o projeto.

### Executável

Para quem não possui Python ou simplesmente quer utilizar a ferramenta diretamente, está disponível o **LeitorDeProjetos-1.0.3.exe**.

Abra a página [**Releases** do repositório](https://github.com/ink-creator/Leitor-de-projetos/releases), entre na versão mais recente e baixe o `.exe` na seção **Assets**.

Essa é a forma recomendada para quem quer apenas utilizar o programa sem modificar seu código.

### Código-fonte

Também é possível utilizar o projeto diretamente pelo código-fonte.

Essa opção é mais adequada para quem deseja estudar, modificar ou adaptar a ferramenta às próprias necessidades.

O código principal está localizado na pasta:

```text
LeitorDeProjetos/
```

## Modo manual

O projeto também possui uma pasta chamada `manual`.

Ela não representa uma parte automática do programa. Seu objetivo é disponibilizar uma forma de realizar o processo manualmente, sem depender da ferramenta.

```text
manual/
```

Essa opção pode ser útil quando você quer ter mais controle sobre quais arquivos serão reunidos ou simplesmente entender o processo por trás da ferramenta.

## Estrutura

```text
Leitor-de-projetos/
│
├── .github/
│   └── workflows/
│
├── LeitorDeProjetos/
│
├── manual/
│
├── .gitignore
│
└── README.md
```

### `LeitorDeProjetos`

Contém o código do programa.

### `manual`

Contém os materiais relacionados ao processo manual de leitura e organização dos arquivos.

### `.github/workflows`

Contém os arquivos utilizados pelos workflows do GitHub.

## Uso com Inteligência Artificial

Um dos principais objetivos do projeto é facilitar o uso de projetos de código com ferramentas de Inteligência Artificial.

Em vez de precisar selecionar e enviar diversos arquivos individualmente, o projeto permite preparar o conteúdo de uma forma mais organizada.

Por exemplo:

```text
Projeto
    |
    v
Leitor de Projetos
    |
    v
Arquivo de texto
    |
    v
Ferramenta de IA
    |
    v
Análise do projeto
```

Isso pode ser útil para tarefas como:

* Análise de código;
* Identificação de problemas;
* Sugestões de melhorias;
* Explicação de projetos;
* Documentação;
* Refatoração;
* Entendimento da estrutura de um projeto.

## Atenção ao compartilhar projetos

Antes de enviar os arquivos gerados para uma IA ou outra pessoa, verifique o conteúdo do projeto.

Arquivos de texto gerados a partir de um projeto podem conter informações que não deveriam ser compartilhadas, como:

```text
Senhas
API Keys
Tokens
Credenciais
Dados pessoais
Chaves privadas
Configurações sensíveis
```

Sempre revise o conteúdo antes de compartilhá-lo.

## Tecnologias

O projeto foi desenvolvido em Python.

Também existe uma versão compilada em `.exe` para facilitar o uso por pessoas que não possuem o ambiente Python configurado.

## Status

Projeto em desenvolvimento.

A proposta é manter o Leitor de Projetos como uma ferramenta pequena, prática e fácil de utilizar, podendo receber novas funcionalidades conforme surgirem novas necessidades.

## Licença

Este projeto está licenciado sob a MIT License.

Consulte o arquivo [LICENSE](LICENSE) para mais informações.

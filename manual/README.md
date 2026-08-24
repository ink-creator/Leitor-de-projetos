# Ferramentas de Leitura de Projetos

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
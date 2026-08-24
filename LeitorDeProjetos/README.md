# Leitor de Projetos

Transforma projetos de código em arquivos de texto para análise,
documentação, compartilhamento e uso com IAs.

## Executar

```
python main.py
```

Sem dependências externas — apenas biblioteca padrão (Tkinter).

## Empacotar como .exe

```
pip install pyinstaller
pyinstaller --onefile --windowed --name LeitorDeProjetos main.py
```

## Deploy no GitHub (para currículo)

### 1. Commit e push das alterações
```bash
git add .
git commit -m "Melhorias de UI e seleção de arquivos"
git push origin main
```

### 2. Criar um repositório no GitHub
1. Acesse https://github.com e crie um novo repositório (ex.: `Leitor-de-projetos`).
2. Siga as instruções para conectar o repositório local ao remoto, caso ainda não tenha feito:
```bash
git remote add origin https://github.com/SEU_USUARIO/Leitor-de-projetos.git
git branch -M main
git push -u origin main
```

### 3. Configurar GitHub Actions (CI/CD) – opcional
O projeto já inclui um workflow em `.github/workflows/release.yml` que gera um artefato `.exe` a cada *release*.
Para utilizá‑lo:
1. Crie uma *release* na página do repositório (botão **Releases → Draft a new release**).
2. Defina uma tag (ex.: `v1.0.0`) e publique.
3. O workflow será disparado, compilando o executável e disponibilizando‑o como artefato da release.

### 4. Atualizar o README do repositório
Inclua no seu perfil ou currículo o link do repositório e, se desejar, o link direto para a última release, por exemplo:
```
https://github.com/SEU_USUARIO/Leitor-de-projetos/releases/latest
```

Esses passos permitem que recrutadores acessem rapidamente o código‑fonte e o executável pronto para demonstração.

## Estrutura

```
LeitorDeProjetos/
├── main.py                      # entrypoint
├── interface/
│   ├── janela_principal.py      # orquestração da UI
│   ├── configuracoes.py         # painel de extensões e ignorados
│   └── dialogos.py              # pré-visualização, confirmação, ajuda, histórico
├── processadores/
│   ├── separado.py              # modo "Arquivo único"
│   └── junto.py                 # modo "Arquivos separados"
├── configuracao/
│   ├── config.py                # persistência de preferências
│   └── historico.py             # persistência de histórico
└── utils/
    └── arquivos.py              # paths dinâmicos, detecção de arquivo sensível
```

## Decisões tomadas em relação aos scripts originais

Os nomes dos arquivos fonte originais (`ler_projeto_separado.py`,
`ler_projeto_junto.py`) descreviam o oposto do que a lógica de cada
um faz. A lógica foi 100% preservada; os nomes exibidos na interface
foram corrigidos:

| Arquivo original            | Comportamento real                  | Nome na interface   |
|------------------------------|--------------------------------------|----------------------|
| `ler_projeto_separado.py`   | gera **um único** arquivo TXT        | **Arquivo único**    |
| `ler_projeto_junto.py`      | gera **um TXT por arquivo**          | **Arquivos separados** |

Outras mudanças de comportamento, autorizadas explicitamente durante
o desenvolvimento (não são "reescrita da lógica de processamento"):

- **Bloqueio real de `.env`**: nos scripts originais, `.env` só era
  ignorado se aparecesse como nome de *pasta*. Como arquivo, na raiz
  do projeto, ele passava despercebido. Isso contradizia a exigência
  de segurança da especificação e foi corrigido em
  `utils/arquivos.py::eh_arquivo_sensivel`, que verifica pelo nome do
  arquivo antes de qualquer outra regra, em ambos os modos.
- **Remoção de `print()`**: os scripts imprimiam cada linha no
  console. Substituído por callbacks de progresso (`on_progresso`,
  `on_erro`) consumidos pela thread da interface.
- **Extensões dos dois modos não foram unificadas** — por decisão
  explícita, cada modo mantém sua própria lista padrão:
  - Arquivo único: `.py .js .html .css .php .md .txt .bat`
  - Arquivos separados: `.php .css .js`
- **`.gitignore` e `pyvenv.cfg`** removidos de `IGNORAR_PASTAS` no
  script original — eram nomes de *arquivo* numa lista comparada
  apenas contra nomes de *pasta* (`os.path.isdir`), então nunca
  tinham efeito algum. Remoção não altera comportamento observável.
- **`src` removido do padrão de pastas ignoradas** do modo Arquivo
  único (só existia lá, não no outro modo). Ignorar todo código-fonte
  contradiz o propósito da ferramenta; continua disponível para
  adicionar manualmente em Configurações.

## O que foi validado neste ambiente

Testado ponta a ponta com display virtual (Xvfb) simulando o fluxo
real pela janela: seleção de projeto, pré-visualização, processamento
nos dois modos, thread não bloqueando a UI, `.env` bloqueado e
confirmado sem vazamento no conteúdo de saída em ambos os modos,
erro de leitura (arquivo com bytes inválidos) isolado sem interromper
o restante do processamento, histórico gravando corretamente,
configuração persistindo e recarregando.

**Não testado** (o ambiente de desenvolvimento é Linux, não Windows):
geração do `.exe` via PyInstaller, `os.startfile` (usado em "Abrir
pasta" — código Windows-only, caminho testado apenas nos ramos
`darwin`/outros), comportamento real de `PermissionError` do Windows
(neste ambiente os testes rodaram como root, que ignora permissões de
arquivo Unix; usei um arquivo com bytes inválidos para exercitar o
branch de tratamento de erro, mas é um caminho de código diferente do
`PermissionError` real do Windows, ainda que a estrutura do
`try/except` cubra ambos). Recomendo testar essas duas coisas
(build do `.exe` e "Abrir pasta"/"Abrir resultado") em uma máquina
Windows real antes de considerar finalizado.

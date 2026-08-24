"""
Janela principal do Leitor de Projetos.

Responsável apenas por orquestração de UI: delega toda a lógica de
processamento para processadores/separado.py e processadores/junto.py,
e toda a persistência para configuracao/config.py e
configuracao/historico.py.
"""

from __future__ import annotations

import datetime
import os
import queue
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from configuracao.config import carregar_config, salvar_config
from configuracao.historico import adicionar_entrada
from interface.configuracoes import JanelaConfiguracoes
from interface.dialogos import (
    JanelaAjuda,
    JanelaConfirmacaoSeguranca,
    JanelaHistorico,
    JanelaPreVisualizacao,
)
from processadores import junto, separado
from utils.arquivos import obter_pasta_saida_padrao

# Nova paleta de cores: tons de azul escuro e preto (mesma usada em dialogos)
COR_FUNDO = "#0d1b2a"          # fundo principal (azul muito escuro)
COR_FUNDO_CARD = "#1a2b3c"     # cartões e áreas de conteúdo
COR_FUNDO_CAMPO = "#16202a"    # campos de entrada
COR_TEXTO = "#e0e0e8"          # texto principal (claro)
COR_TEXTO_SECUNDARIO = "#9a9ab0"  # texto secundário
COR_SUCESSO = "#4ade80"        # verde sucesso
COR_ERRO = "#f87171"           # vermelho erro
COR_AVISO = "#fbbf24"
COR_DESTAQUE = "#3b5b9a"       # azul destaque
COR_DESTAQUE_HOVER = "#2e4a8a" # hover destaque

MODO_ARQUIVO_UNICO = "separado"
MODO_ARQUIVOS_SEPARADOS = "junto"

DESCRICAO_MODO = {
    MODO_ARQUIVO_UNICO: "Cria um único arquivo TXT contendo a estrutura e o conteúdo dos arquivos selecionados.",
    MODO_ARQUIVOS_SEPARADOS: "Cria arquivos TXT separados para cada arquivo de código encontrado.",
}

NOME_MODO_EXIBICAO = {
    MODO_ARQUIVO_UNICO: "Arquivo único",
    MODO_ARQUIVOS_SEPARADOS: "Arquivos separados",
}


class JanelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Leitor de Projetos")
        self.configure(bg=COR_FUNDO)

        self._config = carregar_config()

        largura = self._config.get("janela_largura", 900)
        altura = self._config.get("janela_altura", 640)
        self.geometry(f"{largura}x{altura}")
        self.minsize(760, 560)

        self._pasta_projeto: str = self._config.get("ultima_pasta_projeto", "")
        self._pasta_saida: str = self._config.get("ultima_pasta_saida", "")
        self._modo = tk.StringVar(value=self._config.get("ultimo_modo", MODO_ARQUIVO_UNICO))

        self._fila_eventos: queue.Queue = queue.Queue()
        self._thread_processamento: threading.Thread | None = None
        self._ultimo_resultado = None

        self._montar_layout()
        self.protocol("WM_DELETE_WINDOW", self._ao_fechar)

        # Variáveis para armazenar seleção de arquivos feita na pré‑visualização
        self._arquivos_selecionados: list[str] | None = None
        self._arquivos_ignorados: list[str] | None = None

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _montar_layout(self) -> None:
        topo = tk.Frame(self, bg=COR_FUNDO)
        topo.pack(fill="x", padx=24, pady=(20, 4))

        tk.Label(
            topo, text="Leitor de Projetos",
            font=("Segoe UI", 16, "bold"),
            bg=COR_FUNDO, fg=COR_TEXTO,
        ).pack(anchor="w")
        tk.Label(
            topo,
            text="Ferramenta para transformar projetos de código em arquivos de texto\n"
                 "para análise, compartilhamento e uso com IAs.",
            font=("Segoe UI", 9),
            bg=COR_FUNDO, fg=COR_TEXTO_SECUNDARIO,
            justify="left",
        ).pack(anchor="w", pady=(2, 0))

        barra_acoes = tk.Frame(self, bg=COR_FUNDO)
        barra_acoes.pack(fill="x", padx=24, pady=(12, 0))

        for texto, comando in [
            ("Configurações", self._abrir_configuracoes),
            ("Ajuda", self._abrir_ajuda),
            ("Histórico", self._abrir_historico),
        ]:
            tk.Button(
                barra_acoes, text=texto, command=comando,
                bg=COR_FUNDO_CARD, fg=COR_TEXTO_SECUNDARIO,
                relief="flat", padx=12, pady=4, cursor="hand2",
                font=("Segoe UI", 9),
            ).pack(side="left", padx=(0, 8))

        corpo = tk.Frame(self, bg=COR_FUNDO)
        corpo.pack(fill="both", expand=True, padx=24, pady=16)

        self._montar_secao_projeto(corpo)
        self._montar_secao_modo(corpo)
        self._montar_secao_saida(corpo)
        self._montar_secao_progresso(corpo)
        self._montar_barra_inferior(corpo)

    def _card(self, parent: tk.Widget) -> tk.Frame:
        card = tk.Frame(parent, bg=COR_FUNDO_CARD)
        card.pack(fill="x", pady=(0, 12))
        return card

    def _montar_secao_projeto(self, parent: tk.Widget) -> None:
        card = self._card(parent)
        interno = tk.Frame(card, bg=COR_FUNDO_CARD)
        interno.pack(fill="x", padx=16, pady=12)

        tk.Label(
            interno, text="Projeto selecionado",
            font=("Segoe UI", 10, "bold"),
            bg=COR_FUNDO_CARD, fg=COR_TEXTO,
        ).pack(anchor="w")

        linha = tk.Frame(interno, bg=COR_FUNDO_CARD)
        linha.pack(fill="x", pady=(8, 0))

        self._label_pasta_projeto = tk.Label(
            linha, text=self._texto_pasta_projeto(),
            font=("Segoe UI", 9),
            bg=COR_FUNDO_CAMPO, fg=COR_TEXTO,
            anchor="w", padx=10, pady=8,
        )
        self._label_pasta_projeto.pack(side="left", fill="x", expand=True)

        tk.Button(
            linha, text="Selecionar pasta", command=self._selecionar_pasta_projeto,
            bg=COR_DESTAQUE, fg="#1e1e2e", relief="flat",
            padx=12, pady=6, cursor="hand2", font=("Segoe UI", 9, "bold"),
        ).pack(side="left", padx=(8, 0))

        tk.Button(
            linha, text="Abrir pasta", command=lambda: self._abrir_no_explorador(self._pasta_projeto),
            bg=COR_FUNDO_CAMPO, fg=COR_TEXTO_SECUNDARIO, relief="flat",
            padx=12, pady=6, cursor="hand2", font=("Segoe UI", 9),
        ).pack(side="left", padx=(8, 0))

        pre_viz = tk.Frame(interno, bg=COR_FUNDO_CARD)
        pre_viz.pack(fill="x", pady=(10, 0))

        tk.Button(
            pre_viz, text="Pré-visualizar arquivos", command=self._pre_visualizar,
            bg=COR_FUNDO_CAMPO, fg=COR_TEXTO, relief="flat",
            padx=12, pady=6, cursor="hand2", font=("Segoe UI", 9),
        ).pack(side="left")

    def _texto_pasta_projeto(self) -> str:
        if self._pasta_projeto:
            return self._pasta_projeto
        return "Nenhuma pasta selecionada. Escolha um projeto para começar."

    def _montar_secao_modo(self, parent: tk.Widget) -> None:
        card = self._card(parent)
        interno = tk.Frame(card, bg=COR_FUNDO_CARD)
        interno.pack(fill="x", padx=16, pady=12)

        tk.Label(
            interno, text="Modo de processamento",
            font=("Segoe UI", 10, "bold"),
            bg=COR_FUNDO_CARD, fg=COR_TEXTO,
        ).pack(anchor="w")

        opcoes = tk.Frame(interno, bg=COR_FUNDO_CARD)
        opcoes.pack(fill="x", pady=(8, 0))

        for modo, nome in NOME_MODO_EXIBICAO.items():
            linha_opcao = tk.Frame(opcoes, bg=COR_FUNDO_CARD)
            linha_opcao.pack(fill="x", pady=2)

            tk.Radiobutton(
                linha_opcao, text=nome, variable=self._modo, value=modo,
                bg=COR_FUNDO_CARD, fg=COR_TEXTO, selectcolor=COR_FUNDO_CAMPO,
                activebackground=COR_FUNDO_CARD, activeforeground=COR_TEXTO,
                font=("Segoe UI", 10, "bold"), cursor="hand2",
            ).pack(anchor="w")

            tk.Label(
                linha_opcao, text=DESCRICAO_MODO[modo],
                font=("Segoe UI", 9),
                bg=COR_FUNDO_CARD, fg=COR_TEXTO_SECUNDARIO,
            ).pack(anchor="w", padx=(24, 0))

    def _montar_secao_saida(self, parent: tk.Widget) -> None:
        card = self._card(parent)
        interno = tk.Frame(card, bg=COR_FUNDO_CARD)
        interno.pack(fill="x", padx=16, pady=12)

        tk.Label(
            interno, text="Pasta de destino",
            font=("Segoe UI", 10, "bold"),
            bg=COR_FUNDO_CARD, fg=COR_TEXTO,
        ).pack(anchor="w")

        linha = tk.Frame(interno, bg=COR_FUNDO_CARD)
        linha.pack(fill="x", pady=(8, 0))

        self._label_pasta_saida = tk.Label(
            linha, text=self._texto_pasta_saida(),
            font=("Segoe UI", 9),
            bg=COR_FUNDO_CAMPO, fg=COR_TEXTO,
            anchor="w", padx=10, pady=8,
        )
        self._label_pasta_saida.pack(side="left", fill="x", expand=True)

        # Renomeado para evitar duplicação de texto de botão "Selecionar pasta"
        tk.Button(
            linha, text="Selecionar pasta de saída", command=self._selecionar_pasta_saida,
            bg=COR_FUNDO_CAMPO, fg=COR_TEXTO, relief="flat",
            padx=12, pady=6, cursor="hand2", font=("Segoe UI", 9),
        ).pack(side="left", padx=(8, 0))

        tk.Button(
            linha, text="Abrir pasta", command=lambda: self._abrir_no_explorador(self._pasta_saida_efetiva()),
            bg=COR_FUNDO_CAMPO, fg=COR_TEXTO_SECUNDARIO, relief="flat",
            padx=12, pady=6, cursor="hand2", font=("Segoe UI", 9),
        ).pack(side="left", padx=(8, 0))

    def _texto_pasta_saida(self) -> str:
        if self._pasta_saida:
            return self._pasta_saida
        return f"Padrão: {obter_pasta_saida_padrao()}"

    def _pasta_saida_efetiva(self) -> str:
        return self._pasta_saida or str(obter_pasta_saida_padrao())

    def _montar_secao_progresso(self, parent: tk.Widget) -> None:
        self._card_progresso = tk.Frame(parent, bg=COR_FUNDO_CARD)
        # Não empacotado inicialmente — só aparece durante o processamento.

        interno = tk.Frame(self._card_progresso, bg=COR_FUNDO_CARD)
        interno.pack(fill="x", padx=16, pady=12)

        self._label_status_progresso = tk.Label(
            interno, text="Processando projeto...",
            font=("Segoe UI", 10, "bold"),
            bg=COR_FUNDO_CARD, fg=COR_TEXTO,
        )
        self._label_status_progresso.pack(anchor="w")

        self._label_arquivo_atual = tk.Label(
            interno, text="", font=("Segoe UI", 9),
            bg=COR_FUNDO_CARD, fg=COR_TEXTO_SECUNDARIO,
        )
        self._label_arquivo_atual.pack(anchor="w", pady=(4, 8))

        self._barra_progresso = ttk.Progressbar(
            interno, orient="horizontal", mode="determinate",
        )
        self._barra_progresso.pack(fill="x")

        self._label_contador = tk.Label(
            interno, text="", font=("Segoe UI", 9),
            bg=COR_FUNDO_CARD, fg=COR_TEXTO_SECUNDARIO,
        )
        self._label_contador.pack(anchor="e", pady=(4, 0))

    def _montar_barra_inferior(self, parent: tk.Widget) -> None:
        self._barra_inferior = tk.Frame(parent, bg=COR_FUNDO)
        self._barra_inferior.pack(fill="x", pady=(8, 0))

        self._botao_gerar = tk.Button(
            self._barra_inferior, text="Gerar arquivos",
            command=self._iniciar_fluxo_processamento,
            bg=COR_DESTAQUE, fg="#1e1e2e", relief="flat",
            padx=24, pady=10, cursor="hand2",
            font=("Segoe UI", 11, "bold"),
        )
        self._botao_gerar.pack(side="left")

        self._label_mensagem = tk.Label(
            self._barra_inferior, text="",
            font=("Segoe UI", 9),
            bg=COR_FUNDO, fg=COR_TEXTO_SECUNDARIO,
        )
        self._label_mensagem.pack(side="left", padx=(16, 0))

    # ------------------------------------------------------------------
    # Seleção de pastas
    # ------------------------------------------------------------------

    def _selecionar_pasta_projeto(self) -> None:
        pasta = filedialog.askdirectory(title="Selecionar pasta do projeto")
        if not pasta:
            return
        self._pasta_projeto = pasta
        self._label_pasta_projeto.config(text=self._texto_pasta_projeto())
        self._persistir_config()

    def _selecionar_pasta_saida(self) -> None:
        pasta = filedialog.askdirectory(title="Selecionar pasta de destino")
        if not pasta:
            return
        self._pasta_saida = pasta
        self._label_pasta_saida.config(text=self._texto_pasta_saida())
        self._persistir_config()

    def _abrir_no_explorador(self, caminho: str) -> None:
        if not caminho or not os.path.isdir(caminho):
            messagebox.showinfo("Pasta não encontrada", "Selecione uma pasta válida primeiro.")
            return

        if sys.platform == "win32":
            os.startfile(caminho)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", caminho])
        else:
            subprocess.run(["xdg-open", caminho])

    # ------------------------------------------------------------------
    # Pré-visualização
    # ------------------------------------------------------------------

    def _pre_visualizar(self) -> None:
        """Abre a janela de pré‑visualização permitindo ao usuário escolher
        quais arquivos serão processados. A seleção é armazenada em
        ``self._arquivos_selecionados`` e ``self._arquivos_ignorados`` para ser
        utilizada posteriormente na fase de geração.
        """
        if not self._validar_projeto_selecionado():
            return

        processaveis, ignorados = self._listar_arquivos_modo_atual()
        JanelaPreVisualizacao(
            self,
            processaveis,
            ignorados,
            self._pasta_projeto,
            on_confirmar=self._atualizar_selecao,
        )

    def _atualizar_selecao(self, selecionados: list[str], ignorados: list[str]) -> None:
        """Callback usado pela janela de pré‑visualização para armazenar a
        escolha do usuário.
        """
        self._arquivos_selecionados = selecionados
        self._arquivos_ignorados = ignorados
        # Opcional: atualizar algum indicador visual – por enquanto apenas
        # mantemos a informação para o fluxo de processamento.

    def _listar_arquivos_modo_atual(self) -> tuple[list[str], list[str]]:
        """Retorna as listas de arquivos a processar e a ignorar.
        Se o usuário já fez uma seleção na pré‑visualização, utiliza essa
        seleção; caso contrário, calcula a partir da configuração.
        """
        if self._arquivos_selecionados is not None and self._arquivos_ignorados is not None:
            return self._arquivos_selecionados, self._arquivos_ignorados

        modo = self._modo.get()
        if modo == MODO_ARQUIVO_UNICO:
            extensoes = tuple(self._config["extensoes_separado"])
            processaveis, ignorados, _ = separado.listar_arquivos_projeto(
                self._pasta_projeto, extensoes,
                self._config["pastas_ignoradas"], self._config["arquivos_ignorados"],
            )
        else:
            extensoes = tuple(self._config["extensoes_junto"])
            processaveis, ignorados, _ = junto.listar_arquivos_projeto(
                self._pasta_projeto, extensoes,
                self._config["pastas_ignoradas"], self._config["arquivos_ignorados"],
            )
        return processaveis, ignorados

    def _validar_projeto_selecionado(self) -> bool:
        if not self._pasta_projeto:
            messagebox.showwarning("Nenhum projeto selecionado", "Selecione uma pasta de projeto primeiro.")
            return False
        if not os.path.isdir(self._pasta_projeto):
            messagebox.showerror("Pasta inválida", "A pasta do projeto selecionada não existe mais.")
            return False
        return True

    # ------------------------------------------------------------------
    # Fluxo de processamento
    # ------------------------------------------------------------------

    def _iniciar_fluxo_processamento(self) -> None:
        if not self._validar_projeto_selecionado():
            return

        if self._thread_processamento and self._thread_processamento.is_alive():
            messagebox.showinfo("Em andamento", "Já existe um processamento em execução.")
            return

        processaveis, ignorados = self._listar_arquivos_modo_atual()
        _, _, sensiveis = self._listar_com_contagem_sensiveis()

        JanelaConfirmacaoSeguranca(
            self,
            total_processar=len(processaveis),
            total_sensiveis_ignorados=sensiveis,
            on_confirmar=self._executar_processamento,
        )

    def _listar_com_contagem_sensiveis(self) -> tuple[list[str], list[str], int]:
        modo = self._modo.get()
        if modo == MODO_ARQUIVO_UNICO:
            extensoes = tuple(self._config["extensoes_separado"])
            return separado.listar_arquivos_projeto(
                self._pasta_projeto, extensoes,
                self._config["pastas_ignoradas"], self._config["arquivos_ignorados"],
            )
        extensoes = tuple(self._config["extensoes_junto"])
        return junto.listar_arquivos_projeto(
            self._pasta_projeto, extensoes,
            self._config["pastas_ignoradas"], self._config["arquivos_ignorados"],
        )

    def _executar_processamento(self) -> None:
        self._botao_gerar.config(state="disabled")
        self._card_progresso.pack(fill="x", pady=(0, 12), before=self._barra_inferior)
        self._barra_progresso["value"] = 0
        self._label_mensagem.config(text="")

        modo = self._modo.get()
        pasta_saida = self._pasta_saida_efetiva()

        def on_progresso(evento) -> None:
            self._fila_eventos.put(("progresso", evento))

        def on_erro(caminho: str, motivo: str) -> None:
            self._fila_eventos.put(("erro", (caminho, motivo)))

        def worker() -> None:
            try:
                if modo == MODO_ARQUIVO_UNICO:
                    nome_arquivo = f"arquivo_{datetime.datetime.now():%d_%H_%M}.txt"
                    resultado = separado.processar(
                        caminho_projeto=self._pasta_projeto,
                        caminho_saida_dir=pasta_saida,
                        nome_arquivo_saida=nome_arquivo,
                        extensoes=tuple(self._config["extensoes_separado"]),
                        pastas_ignoradas=self._config["pastas_ignoradas"],
                        arquivos_ignorados=self._config["arquivos_ignorados"],
                        on_progresso=on_progresso,
                        on_erro=on_erro,
                        arquivos_processaveis=self._arquivos_selecionados,
                    )
                else:
                    nome_subpasta = f"resumo_{datetime.datetime.now():%d-%m-%Y_%Hh}"
                    pasta_saida_final = os.path.join(pasta_saida, nome_subpasta)
                    resultado = junto.processar(
                        caminho_projeto=self._pasta_projeto,
                        caminho_saida_dir=pasta_saida_final,
                        extensoes=tuple(self._config["extensoes_junto"]),
                        pastas_ignoradas=self._config["pastas_ignoradas"],
                        arquivos_ignorados=self._config["arquivos_ignorados"],
                        on_progresso=on_progresso,
                        on_erro=on_erro,
                        arquivos_processaveis=self._arquivos_selecionados,
                    )
                self._fila_eventos.put(("concluido", resultado))
            except Exception as e:
                self._fila_eventos.put(("falha", str(e)))

        self._thread_processamento = threading.Thread(target=worker, daemon=True)
        self._thread_processamento.start()
        self.after(80, self._checar_fila_eventos)

    def _checar_fila_eventos(self) -> None:
        try:
            while True:
                tipo, dados = self._fila_eventos.get_nowait()

                if tipo == "progresso":
                    evento = dados
                    self._label_arquivo_atual.config(text=f"Arquivo atual:\n{evento.arquivo_atual}")
                    self._label_contador.config(text=f"{evento.atual} / {evento.total}")
                    if evento.total > 0:
                        self._barra_progresso["value"] = (evento.atual / evento.total) * 100

                elif tipo == "erro":
                    caminho, motivo = dados
                    self._label_status_progresso.config(
                        text=f"[AVISO] Não foi possível ler: {caminho} — {motivo}",
                        fg=COR_AVISO,
                    )
                    self.after(1800, lambda: self._label_status_progresso.config(
                        text="Processando projeto...", fg=COR_TEXTO,
                    ))

                elif tipo == "concluido":
                    self._finalizar_processamento(dados)
                    return

                elif tipo == "falha":
                    self._botao_gerar.config(state="normal")
                    self._card_progresso.pack_forget()
                    messagebox.showerror("Erro no processamento", f"Ocorreu um erro:\n{dados}")
                    return

        except queue.Empty:
            pass

        self.after(80, self._checar_fila_eventos)

    def _finalizar_processamento(self, resultado) -> None:
        self._botao_gerar.config(state="normal")
        self._card_progresso.pack_forget()

        nome_projeto = os.path.basename(self._pasta_projeto.rstrip(os.sep)) or self._pasta_projeto
        modo = self._modo.get()

        adicionar_entrada(
            nome_projeto=nome_projeto,
            quantidade_arquivos=resultado.processados,
            modo=modo,
            pasta_resultado=resultado.caminho_saida,
        )

        self._ultimo_resultado = resultado
        self._mostrar_resultado(resultado)
        self._persistir_config()

    def _mostrar_resultado(self, resultado) -> None:
        janela = tk.Toplevel(self)
        janela.title("Processamento concluído")
        janela.configure(bg=COR_FUNDO)
        janela.transient(self)
        janela.grab_set()
        janela.resizable(False, False)

        corpo = tk.Frame(janela, bg=COR_FUNDO)
        corpo.pack(padx=28, pady=24)

        tk.Label(
            corpo, text="Processamento concluído.",
            font=("Segoe UI", 13, "bold"),
            bg=COR_FUNDO, fg=COR_SUCESSO,
        ).pack(anchor="w", pady=(0, 12))

        linhas = [
            f"Arquivos encontrados: {resultado.encontrados}",
            f"Arquivos processados: {resultado.processados}",
            f"Arquivos ignorados: {resultado.ignorados}",
            f"Erros: {len(resultado.erros)}",
        ]
        for linha in linhas:
            tk.Label(
                corpo, text=linha, font=("Segoe UI", 10),
                bg=COR_FUNDO, fg=COR_TEXTO,
            ).pack(anchor="w")

        tk.Label(
            corpo, text="\nResultado:", font=("Segoe UI", 10, "bold"),
            bg=COR_FUNDO, fg=COR_TEXTO,
        ).pack(anchor="w")
        tk.Label(
            corpo, text=resultado.caminho_saida, font=("Consolas", 9),
            bg=COR_FUNDO, fg=COR_TEXTO_SECUNDARIO, wraplength=420, justify="left",
        ).pack(anchor="w")

        botoes = tk.Frame(corpo, bg=COR_FUNDO)
        botoes.pack(fill="x", pady=(20, 0))

        def abrir_resultado() -> None:
            caminho = resultado.caminho_saida
            alvo = caminho if os.path.isdir(caminho) else os.path.dirname(caminho)
            self._abrir_no_explorador(alvo)

        def novo_processamento() -> None:
            janela.destroy()

        tk.Button(
            botoes, text="Abrir resultado", command=abrir_resultado,
            bg=COR_DESTAQUE, fg="#1e1e2e", relief="flat",
            padx=14, pady=8, cursor="hand2", font=("Segoe UI", 9, "bold"),
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            botoes, text="Abrir pasta", command=abrir_resultado,
            bg=COR_FUNDO_CARD, fg=COR_TEXTO, relief="flat",
            padx=14, pady=8, cursor="hand2", font=("Segoe UI", 9),
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            botoes, text="Novo processamento", command=novo_processamento,
            bg=COR_FUNDO_CARD, fg=COR_TEXTO_SECUNDARIO, relief="flat",
            padx=14, pady=8, cursor="hand2", font=("Segoe UI", 9),
        ).pack(side="left")

    # ------------------------------------------------------------------
    # Diálogos auxiliares
    # ------------------------------------------------------------------

    def _abrir_configuracoes(self) -> None:
        JanelaConfiguracoes(self, self._config, self._ao_salvar_configuracoes)

    def _ao_salvar_configuracoes(self, nova_config: dict) -> None:
        self._config = nova_config
        self._persistir_config()

    def _abrir_ajuda(self) -> None:
        JanelaAjuda(self)

    def _abrir_historico(self) -> None:
        JanelaHistorico(self)

    # ------------------------------------------------------------------
    # Persistência
    # ------------------------------------------------------------------

    def _persistir_config(self) -> None:
        self._config["ultima_pasta_projeto"] = self._pasta_projeto
        self._config["ultima_pasta_saida"] = self._pasta_saida
        self._config["ultimo_modo"] = self._modo.get()
        self._config["janela_largura"] = self.winfo_width()
        self._config["janela_altura"] = self.winfo_height()
        salvar_config(self._config)

    def _ao_fechar(self) -> None:
        self._persistir_config()
        self.destroy()

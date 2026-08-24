"""
Diálogos modais reutilizáveis: pré-visualização de arquivos,
confirmação de segurança antes do processamento, ajuda/sobre, e
consulta ao histórico.
"""

from __future__ import annotations

import os
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from configuracao.historico import EntradaHistorico, carregar_historico, limpar_historico

COR_FUNDO = "#1e1e2e"
COR_FUNDO_CARD = "#2a2a3c"
COR_TEXTO = "#e0e0e8"
COR_TEXTO_SECUNDARIO = "#9a9ab0"
COR_SUCESSO = "#4ade80"
COR_ERRO = "#f87171"
COR_DESTAQUE = "#818cf8"


def _centralizar_janela(janela: tk.Toplevel, largura: int, altura: int) -> None:
    janela.update_idletasks()
    tela_largura = janela.winfo_screenwidth()
    tela_altura = janela.winfo_screenheight()
    x = (tela_largura // 2) - (largura // 2)
    y = (tela_altura // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{x}+{y}")


class JanelaPreVisualizacao(tk.Toplevel):
    """
    Mostra quais arquivos serão processados e quais serão ignorados,
    sem abrir o conteúdo dos arquivos — apenas a lista de nomes.
    """

    def __init__(
        self,
        parent: tk.Widget,
        processaveis: list[str],
        ignorados: list[str],
        raiz_projeto: str,
    ):
        super().__init__(parent)
        self.title("Pré-visualização")
        self.configure(bg=COR_FUNDO)
        self.transient(parent)
        self.grab_set()
        _centralizar_janela(self, 560, 520)

        total = len(processaveis) + len(ignorados)

        cabecalho = tk.Frame(self, bg=COR_FUNDO)
        cabecalho.pack(fill="x", padx=20, pady=(16, 8))

        tk.Label(
            cabecalho,
            text=f"Arquivos encontrados: {total}",
            font=("Segoe UI", 11, "bold"),
            bg=COR_FUNDO, fg=COR_TEXTO,
        ).pack(anchor="w")
        tk.Label(
            cabecalho,
            text=f"Serão processados: {len(processaveis)}      Serão ignorados: {len(ignorados)}",
            font=("Segoe UI", 10),
            bg=COR_FUNDO, fg=COR_TEXTO_SECUNDARIO,
        ).pack(anchor="w", pady=(2, 0))

        container_lista = tk.Frame(self, bg=COR_FUNDO)
        container_lista.pack(fill="both", expand=True, padx=20, pady=8)

        scrollbar = ttk.Scrollbar(container_lista)
        scrollbar.pack(side="right", fill="y")

        texto = tk.Text(
            container_lista,
            bg=COR_FUNDO_CARD, fg=COR_TEXTO,
            font=("Consolas", 9),
            wrap="none",
            yscrollcommand=scrollbar.set,
            borderwidth=0, highlightthickness=0,
        )
        texto.pack(fill="both", expand=True)
        scrollbar.config(command=texto.yview)

        texto.tag_config("ok", foreground=COR_SUCESSO)
        texto.tag_config("ignorado", foreground=COR_TEXTO_SECUNDARIO)

        for caminho in processaveis:
            rel = os.path.relpath(caminho, raiz_projeto)
            texto.insert("end", f"✓ {rel}\n", "ok")

        for caminho in ignorados:
            rel = os.path.relpath(caminho, raiz_projeto)
            texto.insert("end", f"✗ {rel}\n", "ignorado")

        texto.config(state="disabled")

        rodape = tk.Frame(self, bg=COR_FUNDO)
        rodape.pack(fill="x", padx=20, pady=(8, 16))

        tk.Button(
            rodape, text="Fechar", command=self.destroy,
            bg=COR_FUNDO_CARD, fg=COR_TEXTO, activebackground=COR_DESTAQUE,
            relief="flat", padx=16, pady=6, cursor="hand2",
        ).pack(side="right")


class JanelaConfirmacaoSeguranca(tk.Toplevel):
    """
    Confirmação obrigatória antes de iniciar o processamento,
    mostrando quantos arquivos serão processados e quantos arquivos
    sensíveis foram automaticamente excluídos.
    """

    def __init__(
        self,
        parent: tk.Widget,
        total_processar: int,
        total_sensiveis_ignorados: int,
        on_confirmar: Callable[[], None],
    ):
        super().__init__(parent)
        self.title("Confirmar processamento")
        self.configure(bg=COR_FUNDO)
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)
        _centralizar_janela(self, 400, 220)

        self._on_confirmar = on_confirmar

        corpo = tk.Frame(self, bg=COR_FUNDO)
        corpo.pack(fill="both", expand=True, padx=24, pady=24)

        tk.Label(
            corpo,
            text=f"Serão processados {total_processar} arquivos.",
            font=("Segoe UI", 11),
            bg=COR_FUNDO, fg=COR_TEXTO,
        ).pack(anchor="w", pady=(0, 6))

        if total_sensiveis_ignorados > 0:
            tk.Label(
                corpo,
                text=f"Arquivos sensíveis ignorados: {total_sensiveis_ignorados}.",
                font=("Segoe UI", 10),
                bg=COR_FUNDO, fg=COR_ERRO,
            ).pack(anchor="w", pady=(0, 16))
        else:
            tk.Label(
                corpo,
                text="Nenhum arquivo sensível encontrado.",
                font=("Segoe UI", 10),
                bg=COR_FUNDO, fg=COR_TEXTO_SECUNDARIO,
            ).pack(anchor="w", pady=(0, 16))

        tk.Label(
            corpo, text="Deseja continuar?",
            font=("Segoe UI", 11, "bold"),
            bg=COR_FUNDO, fg=COR_TEXTO,
        ).pack(anchor="w", pady=(0, 16))

        botoes = tk.Frame(corpo, bg=COR_FUNDO)
        botoes.pack(fill="x")

        tk.Button(
            botoes, text="Cancelar", command=self.destroy,
            bg=COR_FUNDO_CARD, fg=COR_TEXTO,
            relief="flat", padx=16, pady=6, cursor="hand2",
        ).pack(side="right", padx=(8, 0))

        tk.Button(
            botoes, text="Continuar", command=self._confirmar,
            bg=COR_DESTAQUE, fg="#1e1e2e",
            relief="flat", padx=16, pady=6, cursor="hand2",
            font=("Segoe UI", 10, "bold"),
        ).pack(side="right")

    def _confirmar(self) -> None:
        self.destroy()
        self._on_confirmar()


class JanelaAjuda(tk.Toplevel):
    def __init__(self, parent: tk.Widget):
        super().__init__(parent)
        self.title("Sobre / Ajuda")
        self.configure(bg=COR_FUNDO)
        self.transient(parent)
        self.grab_set()
        _centralizar_janela(self, 520, 480)

        container = tk.Frame(self, bg=COR_FUNDO)
        container.pack(fill="both", expand=True, padx=24, pady=20)

        texto = tk.Text(
            container, bg=COR_FUNDO, fg=COR_TEXTO,
            font=("Segoe UI", 10), wrap="word",
            borderwidth=0, highlightthickness=0,
        )
        texto.pack(fill="both", expand=True)

        texto.tag_config("titulo", font=("Segoe UI", 11, "bold"), foreground=COR_DESTAQUE)

        conteudo = [
            ("titulo", "Para que serve\n"),
            (None, "Transforma projetos de código em arquivos de texto, "
                    "para análise, documentação, compartilhamento e envio "
                    "para ferramentas de IA.\n\n"),
            ("titulo", "Arquivo único × Arquivos separados\n"),
            (None, "Arquivo único: gera um único .txt com a árvore de "
                    "pastas e o conteúdo de todos os arquivos.\n"
                    "Arquivos separados: gera um .txt para cada arquivo "
                    "de código, preservando a estrutura de pastas.\n\n"),
            ("titulo", "Como selecionar um projeto\n"),
            (None, "Clique em \"Selecionar pasta\" na seção Projeto e "
                    "escolha a pasta raiz do seu código.\n\n"),
            ("titulo", "Como configurar extensões\n"),
            (None, "Em Configurações, adicione ou remova extensões de "
                    "arquivo que devem ser lidas. Cada modo mantém sua "
                    "própria lista.\n\n"),
            ("titulo", "Como configurar itens ignorados\n"),
            (None, "Em Configurações, adicione nomes de pastas ou "
                    "arquivos que nunca devem ser processados.\n\n"),
            ("titulo", "Por que .env é ignorado\n"),
            (None, "Arquivos .env costumam conter senhas, chaves de API "
                    "e tokens. Por segurança, são sempre bloqueados, "
                    "mesmo que sua extensão esteja na lista permitida.\n\n"),
            ("titulo", "Onde os resultados são salvos\n"),
            (None, "Na pasta de destino escolhida, ou em uma pasta "
                    "padrão na Área de Trabalho caso nenhuma seja "
                    "informada.\n"),
        ]

        for tag, trecho in conteudo:
            if tag:
                texto.insert("end", trecho, tag)
            else:
                texto.insert("end", trecho)

        texto.config(state="disabled")

        tk.Button(
            self, text="Fechar", command=self.destroy,
            bg=COR_FUNDO_CARD, fg=COR_TEXTO,
            relief="flat", padx=16, pady=6, cursor="hand2",
        ).pack(pady=(0, 16))


class JanelaHistorico(tk.Toplevel):
    def __init__(self, parent: tk.Widget, on_limpar: Optional[Callable[[], None]] = None):
        super().__init__(parent)
        self.title("Histórico")
        self.configure(bg=COR_FUNDO)
        self.transient(parent)
        self.grab_set()
        _centralizar_janela(self, 520, 440)

        self._on_limpar = on_limpar

        container = tk.Frame(self, bg=COR_FUNDO)
        container.pack(fill="both", expand=True, padx=20, pady=(16, 8))

        entradas = carregar_historico()

        if not entradas:
            tk.Label(
                container, text="Nenhum processamento realizado ainda.",
                font=("Segoe UI", 10), bg=COR_FUNDO, fg=COR_TEXTO_SECUNDARIO,
            ).pack(pady=40)
        else:
            scrollbar = ttk.Scrollbar(container)
            scrollbar.pack(side="right", fill="y")

            lista = tk.Text(
                container, bg=COR_FUNDO_CARD, fg=COR_TEXTO,
                font=("Consolas", 9), wrap="none",
                yscrollcommand=scrollbar.set,
                borderwidth=0, highlightthickness=0,
            )
            lista.pack(fill="both", expand=True)
            scrollbar.config(command=lista.yview)

            for entrada in entradas:
                modo_label = "Arquivo único" if entrada.modo == "separado" else "Arquivos separados"
                linha = (
                    f"{entrada.data} — {entrada.nome_projeto} — "
                    f"{entrada.quantidade_arquivos} arquivos — {modo_label}\n"
                )
                lista.insert("end", linha)

            lista.config(state="disabled")

        rodape = tk.Frame(self, bg=COR_FUNDO)
        rodape.pack(fill="x", padx=20, pady=(8, 16))

        if entradas:
            tk.Button(
                rodape, text="Limpar histórico", command=self._limpar,
                bg=COR_FUNDO_CARD, fg=COR_ERRO,
                relief="flat", padx=16, pady=6, cursor="hand2",
            ).pack(side="left")

        tk.Button(
            rodape, text="Fechar", command=self.destroy,
            bg=COR_FUNDO_CARD, fg=COR_TEXTO,
            relief="flat", padx=16, pady=6, cursor="hand2",
        ).pack(side="right")

    def _limpar(self) -> None:
        limpar_historico()
        if self._on_limpar:
            self._on_limpar()
        self.destroy()

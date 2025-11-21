# ----------------------------------------------
# Importações necessárias
# ----------------------------------------------
import tkinter as tk
from tkinter import ttk, messagebox
import random

# =====================================================================
# =============================  IA DO JOGO  ===========================
# =====================================================================

def ia_facil(tabuleiro):
    jogadas = [i for i, x in enumerate(tabuleiro) if x == ""]
    return random.choice(jogadas) if jogadas else None

def ia_media(tabuleiro, jogador, ia):
    # tenta vencer
    for i in range(9):
        if tabuleiro[i] == "":
            copia = tabuleiro[:]
            copia[i] = ia
            if verifica_vitoria(copia, ia):
                return i
    # tenta bloquear
    for i in range(9):
        if tabuleiro[i] == "":
            copia = tabuleiro[:]
            copia[i] = jogador
            if verifica_vitoria(copia, jogador):
                return i
    # aleatório
    return ia_facil(tabuleiro)

def minimax(tabuleiro, atual, ia, jogador):
    if verifica_vitoria(tabuleiro, ia):
        return 1
    if verifica_vitoria(tabuleiro, jogador):
        return -1
    if "" not in tabuleiro:
        return 0

    if atual == ia:
        melhor = -999
        for i in range(9):
            if tabuleiro[i] == "":
                copia = tabuleiro[:]
                copia[i] = atual
                valor = minimax(copia, jogador, ia, jogador)
                melhor = max(melhor, valor)
        return melhor
    else:
        melhor = 999
        for i in range(9):
            if tabuleiro[i] == "":
                copia = tabuleiro[:]
                copia[i] = atual
                valor = minimax(copia, ia, ia, jogador)
                melhor = min(melhor, valor)
        return melhor

def ia_dificil(tabuleiro, jogador, ia):
    melhor_valor = -999
    melhor_jogada = None

    for i in range(9):
        if tabuleiro[i] == "":
            copia = tabuleiro[:]
            copia[i] = ia
            valor = minimax(copia, jogador, ia, jogador)
            if valor > melhor_valor:
                melhor_valor = valor
                melhor_jogada = i

    return melhor_jogada if melhor_jogada is not None else ia_facil(tabuleiro)

# =====================================================================
# =======================  FUNÇÃO DE VITÓRIA  ==========================
# =====================================================================

def verifica_vitoria(tab, simb):
    combinacoes = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    return any(tab[c[0]] == simb and tab[c[1]] == simb and tab[c[2]] == simb for c in combinacoes)

# =====================================================================
# =========================  CLASSE PRINCIPAL  =========================
# =====================================================================

class JogoDaVelha:

    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Velha – desenvolvido por Hildebrando Marques")
        self.root.geometry("420x560")
        self.root.resizable(False, False)

        self.tabuleiro = [""] * 9
        self.nome_jogador = ""
        self.jog_simbolo = "X"
        self.ia_simbolo = "O"
        self.dificuldade = "Fácil"
        self.rodadas_meta = 3
        self.rodada_atual = 1
        self.pontos_jog = 0
        self.pontos_ia = 0

        self.tela_inicial()

    # ----------------------------------------------
    # TELA INICIAL
    # ----------------------------------------------
    def tela_inicial(self):
        for w in self.root.winfo_children():
            w.destroy()

        self.root.configure(bg="white")

        tk.Label(self.root, text="Jogo da Velha", font=("Arial", 26, "bold"), bg="white").pack(pady=(18, 4))
        tk.Label(self.root, text="Desenvolvido por Hildebrando Marques", font=("Arial", 10), bg="white").pack()

        frame = tk.Frame(self.root, bg="white")
        frame.pack(pady=10)

        tk.Label(frame, text="Seu nome:", bg="white", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
        self.campo_nome = tk.Entry(frame, font=("Arial", 12))
        self.campo_nome.grid(row=1, column=0, pady=6, sticky="we")

        tk.Label(frame, text="Escolha seu símbolo:", bg="white", font=("Arial", 12)).grid(row=2, column=0, sticky="w")
        self.simbolo_var = tk.StringVar(value="X")
        r = tk.Frame(frame, bg="white")
        r.grid(row=3, column=0, sticky="w")
        ttk.Radiobutton(r, text="X", variable=self.simbolo_var, value="X").pack(side="left", padx=5)
        ttk.Radiobutton(r, text="O", variable=self.simbolo_var, value="O").pack(side="left")

        tk.Label(frame, text="Dificuldade:", bg="white", font=("Arial", 12)).grid(row=4, column=0, sticky="w")
        self.dif_var = tk.StringVar(value="Fácil")
        ttk.Combobox(frame, textvariable=self.dif_var, values=["Fácil", "Médio", "Difícil"], state="readonly").grid(row=5, column=0, pady=5, sticky="we")

        tk.Label(frame, text="Rodadas para vencer:", bg="white", font=("Arial", 12)).grid(row=6, column=0, sticky="w")
        self.rodada_var = tk.IntVar(value=3)
        ttk.Combobox(frame, textvariable=self.rodada_var, values=[3, 5, 7], state="readonly").grid(row=7, column=0, pady=5, sticky="we")

        tk.Button(self.root, text="Iniciar Jogo", font=("Arial", 14), bg="#1976D2", fg="white",
                  command=self.iniciar_jogo).pack(pady=14)

    def iniciar_jogo(self):
        self.nome_jogador = self.campo_nome.get().strip()
        if not self.nome_jogador:
            messagebox.showerror("Erro", "Digite seu nome!")
            return

        self.jog_simbolo = self.simbolo_var.get()
        self.ia_simbolo = "O" if self.jog_simbolo == "X" else "X"

        self.dificuldade = self.dif_var.get()
        self.rodadas_meta = int(self.rodada_var.get())

        self.pontos_jog = 0
        self.pontos_ia = 0
        self.rodada_atual = 1

        self.tela_jogo()

    # ----------------------------------------------
    # TELA DO JOGO
    # ----------------------------------------------
    def tela_jogo(self):
        for w in self.root.winfo_children():
            w.destroy()

        self.root.configure(bg="white")
        self.tabuleiro = [""] * 9

        tk.Label(self.root, text=f"Rodada {self.rodada_atual}/{self.rodadas_meta}",
                 font=("Arial", 16, "bold"), bg="white").pack(pady=(10, 0))

        tk.Label(self.root, text=f"{self.nome_jogador} ({self.jog_simbolo})  x  IA ({self.ia_simbolo})",
                 font=("Arial", 13), bg="white").pack()

        self.lbl_placar = tk.Label(self.root, text=f"Placar: {self.pontos_jog} - {self.pontos_ia}",
                                   font=("Arial", 14), bg="white")
        self.lbl_placar.pack(pady=8)

        canvas_size = 330
        margin = 15
        cell = (canvas_size - 2 * margin) // 3
        line_width = 8

        self.canvas = tk.Canvas(self.root, width=canvas_size, height=canvas_size,
                                bg="white", highlightthickness=0)
        self.canvas.pack(pady=10)

        self.canvas.create_line(margin, margin + cell, canvas_size - margin, margin + cell, width=line_width)
        self.canvas.create_line(margin, margin + 2 * cell, canvas_size - margin, margin + 2 * cell, width=line_width)
        self.canvas.create_line(margin + cell, margin, margin + cell, canvas_size - margin, width=line_width)
        self.canvas.create_line(margin + 2 * cell, margin, margin + 2 * cell, canvas_size - margin, width=line_width)

        self.btns = []
        for i in range(9):
            row = i // 3
            col = i % 3
            cx = margin + col * cell + cell // 2
            cy = margin + row * cell + cell // 2

            b = tk.Button(self.canvas, text="", font=("Arial", 32, "bold"),
                          bg="#fafafa", command=lambda i=i: self.jogada(i))
            self.canvas.create_window(cx, cy, window=b, width=cell - 12, height=cell - 12)
            self.btns.append(b)

        rodape = tk.Frame(self.root, bg="white")
        rodape.pack(pady=10)

        tk.Button(rodape, text="Voltar", bg="#f0f0f0",
                  command=self.tela_inicial).pack(side="left", padx=5)
        tk.Button(rodape, text="Reiniciar Rodada", bg="#f0f0f0",
                  command=self.reiniciar_rodada).pack(side="left", padx=5)
        tk.Button(rodape, text="Sair", bg="#f0f0f0",
                  command=self.root.quit).pack(side="left", padx=5)

    # ----------------------------------------------
    # Jogada do Jogador
    # ----------------------------------------------
    def jogada(self, pos):
        if self.tabuleiro[pos] != "":
            return

        self.tabuleiro[pos] = self.jog_simbolo
        self.btns[pos].config(text=self.jog_simbolo)

        if verifica_vitoria(self.tabuleiro, self.jog_simbolo):
            self.pontos_jog += 1
            self.lbl_placar.config(text=f"Placar: {self.pontos_jog} - {self.pontos_ia}")
            self.desativar_botoes()
            self.finalizar_rodada(f"{self.nome_jogador} venceu!")
            return

        if "" not in self.tabuleiro:
            self.finalizar_rodada("Empate!")
            return

        self.root.after(300, self.jogada_ia)

    # ----------------------------------------------
    # IA joga
    # ----------------------------------------------
    def jogada_ia(self):
        if "" not in self.tabuleiro:
            return

        if self.dificuldade == "Fácil":
            pos = ia_facil(self.tabuleiro)
        elif self.dificuldade == "Médio":
            pos = ia_media(self.tabuleiro, self.jog_simbolo, self.ia_simbolo)
        else:
            pos = ia_dificil(self.tabuleiro, self.jog_simbolo, self.ia_simbolo)

        if pos is None:
            return

        self.tabuleiro[pos] = self.ia_simbolo
        self.btns[pos].config(text=self.ia_simbolo)

        if verifica_vitoria(self.tabuleiro, self.ia_simbolo):
            self.pontos_ia += 1
            self.lbl_placar.config(text=f"Placar: {self.pontos_jog} - {self.pontos_ia}")
            self.desativar_botoes()
            self.finalizar_rodada("A IA venceu!")
            return

        if "" not in self.tabuleiro:
            self.finalizar_rodada("Empate!")

    # ----------------------------------------------
    # Auxiliar – desativa botões
    # ----------------------------------------------
    def desativar_botoes(self):
        for b in self.btns:
            b.config(state="disabled")

    def ativar_botoes(self):
        for b in self.btns:
            b.config(state="normal")

    # ----------------------------------------------
    # Reiniciar Rodada
    # ----------------------------------------------
    def reiniciar_rodada(self):
        self.tabuleiro = [""] * 9
        for b in self.btns:
            b.config(text="", state="normal")

    # ----------------------------------------------
    # Finaliza Rodada
    # ----------------------------------------------
    def finalizar_rodada(self, mensagem):
        self.root.after(250, lambda: messagebox.showinfo("Fim da Rodada", mensagem))

        self.rodada_atual += 1

        if self.pontos_jog > self.rodadas_meta // 2:
            self.fim_jogo(f"{self.nome_jogador} é o CAMPEÃO!")
            return

        if self.pontos_ia > self.rodadas_meta // 2:
            self.fim_jogo("A IA é a campeã!")
            return

        if self.rodada_atual > self.rodadas_meta:
            if self.pontos_jog > self.pontos_ia:
                self.fim_jogo(f"{self.nome_jogador} venceu o jogo!")
            elif self.pontos_ia > self.pontos_jog:
                self.fim_jogo("A IA venceu o jogo!")
            else:
                self.fim_jogo("Empate geral!")
            return

        self.root.after(260, self.reiniciar_rodada)

    # ----------------------------------------------
    # Tela Final
    # ----------------------------------------------
    def fim_jogo(self, mensagem):
        for w in self.root.winfo_children():
            w.destroy()

        tk.Label(self.root, text=mensagem, font=("Arial", 22, "bold"), bg="white").pack(pady=40)
        tk.Label(self.root, text=f"Placar final: {self.pontos_jog} x {self.pontos_ia}",
                 font=("Arial", 16), bg="white").pack()

        frame = tk.Frame(self.root, bg="white")
        frame.pack(pady=20)

        tk.Button(frame, text="Novo Jogo", font=("Arial", 12), bg="#1976D2", fg="white",
                  command=self.tela_inicial).pack(side="left", padx=10)
        tk.Button(frame, text="Sair", font=("Arial", 12),
                  bg="#f0f0f0", command=self.root.quit).pack(side="left", padx=10)


# =====================================================================
# EXECUÇÃO
# =====================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = JogoDaVelha(root)
    root.mainloop()

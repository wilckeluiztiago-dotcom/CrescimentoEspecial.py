import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from ..model.estado import Estado

class Visualizacao(ttk.Frame):
    def __init__(self, parent, estado: Estado):
        super().__init__(parent)
        self.estado = estado
        
        # Configuração da Figura Matplotlib
        self.fig = plt.Figure(figsize=(12, 8), dpi=100, facecolor='black')
        self.axs = self.fig.subplots(2, 3) # 6 subplots
        self.fig.tight_layout(pad=3.0)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Inicializar plots
        self.im_K = None
        self.im_H = None
        self.im_A = None
        self.im_P = None
        self.im_L = None
        self.im_Y = None
        
        self.inicializar_plots()

    def inicializar_plots(self):
        # Estilo Dark para visual premium
        plt.style.use('dark_background')
        
        # K - Capital Físico
        ax = self.axs[0, 0]
        self.im_K = ax.imshow(self.estado.K, cmap='viridis', origin='lower', vmin=0, interpolation='bicubic')
        ax.set_title('Capital Físico (K)')
        ax.axis('off') # Remover eixos para visual mais limpo
        self.fig.colorbar(self.im_K, ax=ax)

        # H - Capital Humano
        ax = self.axs[0, 1]
        self.im_H = ax.imshow(self.estado.H, cmap='plasma', origin='lower', vmin=0, interpolation='bicubic')
        ax.set_title('Capital Humano (H)')
        ax.axis('off')
        self.fig.colorbar(self.im_H, ax=ax)

        # A - Tecnologia
        ax = self.axs[0, 2]
        self.im_A = ax.imshow(self.estado.A, cmap='magma', origin='lower', vmin=0, interpolation='bicubic')
        ax.set_title('Tecnologia (A)')
        ax.axis('off')
        self.fig.colorbar(self.im_A, ax=ax)

        # P - Poluição
        ax = self.axs[1, 0]
        self.im_P = ax.imshow(self.estado.P, cmap='Greys', origin='lower', vmin=0, interpolation='bicubic')
        ax.set_title('Poluição (P)')
        ax.axis('off')
        self.fig.colorbar(self.im_P, ax=ax)

        # L - População
        ax = self.axs[1, 1]
        self.im_L = ax.imshow(self.estado.L, cmap='cividis', origin='lower', vmin=0, interpolation='bicubic')
        ax.set_title('População (L)')
        ax.axis('off')
        self.fig.colorbar(self.im_L, ax=ax)
        
        # Y - Produto (Output)
        ax = self.axs[1, 2]
        self.im_Y = ax.imshow(self.estado.Y, cmap='inferno', origin='lower', vmin=0, interpolation='bicubic')
        ax.set_title('Produto (Y)')
        ax.axis('off')
        self.fig.colorbar(self.im_Y, ax=ax)

    def atualizar(self):
        # Atualiza os dados dos plots sem recriar a figura
        # Removemos autoscale() para evitar "pulos" nos eixos/cores
        self.im_K.set_data(self.estado.K)
        # Opcional: atualizar clim se mudar muito, mas por enquanto manter fixo ou manual é mais estável
        self.im_K.set_clim(vmin=0, vmax=np.max(self.estado.K))
        
        self.im_H.set_data(self.estado.H)
        self.im_H.set_clim(vmin=0, vmax=np.max(self.estado.H))
        
        self.im_A.set_data(self.estado.A)
        self.im_A.set_clim(vmin=0, vmax=np.max(self.estado.A))
        
        self.im_P.set_data(self.estado.P)
        self.im_P.set_clim(vmin=0, vmax=np.max(self.estado.P))
        
        self.im_L.set_data(self.estado.L)
        self.im_L.set_clim(vmin=0, vmax=np.max(self.estado.L))
        
        self.im_Y.set_data(self.estado.Y)
        self.im_Y.set_clim(vmin=0, vmax=np.max(self.estado.Y))
        
        self.canvas.draw_idle()

import tkinter as tk
from tkinter import ttk
from ..model.parametros import Parametros
from ..model.estado import Estado
from ..model.dinamica import Dinamica
from .visualizacao import Visualizacao
from .painel_controle import PainelControle

class JanelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulação de Crescimento Econômico Espacial")
        self.geometry("1200x800")
        
        # Inicializar Modelo
        self.params = Parametros()
        self.estado = Estado(self.params)
        self.estado.inicializar_com_ruido() # Começar com algo interessante
        self.dinamica = Dinamica(self.params)
        
        self.rodando = False
        
        self.criar_interface()
        
    def criar_interface(self):
        # Layout Principal usando PanedWindow para permitir redimensionamento
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # PanedWindow Horizontal
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.grid(row=0, column=0, sticky="nsew")
        
        # Painel Esquerdo (Visualização)
        # Precisamos de um frame container para o visualizador
        frame_vis = ttk.Frame(paned)
        self.vis = Visualizacao(frame_vis, self.estado)
        self.vis.pack(fill=tk.BOTH, expand=True)
        paned.add(frame_vis, weight=4) # Peso maior para visualização
        
        # Painel Direito (Controles)
        frame_controle = ttk.Frame(paned)
        callbacks = {
            'start': self.iniciar_simulacao,
            'stop': self.parar_simulacao,
            'reset': self.resetar_simulacao
        }
        self.painel = PainelControle(frame_controle, self.params, callbacks)
        self.painel.pack(fill=tk.BOTH, expand=True)
        
        # Adicionar ao paned com peso menor, mas garantindo espaço
        paned.add(frame_controle, weight=1)
        
    def iniciar_simulacao(self):
        if not self.rodando:
            self.rodando = True
            self.loop_simulacao()
            
    def parar_simulacao(self):
        self.rodando = False
        
    def resetar_simulacao(self):
        self.parar_simulacao()
        self.estado = Estado(self.params)
        self.estado.inicializar_com_ruido()
        # Precisamos atualizar a referência no visualizador também, ou apenas atualizar os dados
        # O visualizador mantém referência ao objeto estado. Se recriarmos, precisamos atualizar lá.
        # Melhor seria ter um método reset no Estado, mas vamos atualizar a ref.
        self.vis.estado = self.estado
        self.vis.atualizar()
        
    def loop_simulacao(self):
        if self.rodando:
            # Executar um passo da dinâmica
            self.dinamica.passo(self.estado)
            
            # Atualizar visualização
            self.vis.atualizar()
            
            # Agendar próximo frame (ex: 50ms)
            self.after(50, self.loop_simulacao)

if __name__ == "__main__":
    app = JanelaPrincipal()
    app.mainloop()

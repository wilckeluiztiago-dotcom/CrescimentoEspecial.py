import tkinter as tk
from tkinter import ttk
from ..model.parametros import Parametros

class PainelControle(ttk.Frame):
    def __init__(self, parent, params: Parametros, callbacks):
        super().__init__(parent, padding="10")
        self.params = params
        self.callbacks = callbacks 
        
        self.criar_widgets()

    def criar_widgets(self):
        # Botões de Controle
        frame_botoes = ttk.LabelFrame(self, text="Controle da Simulação", padding="5")
        frame_botoes.pack(fill=tk.X, pady=5)
        
        ttk.Button(frame_botoes, text="Iniciar", command=self.callbacks['start']).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Pausar", command=self.callbacks['stop']).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Resetar", command=self.callbacks['reset']).pack(side=tk.LEFT, padx=5)
        
        # Parâmetros
        frame_params = ttk.LabelFrame(self, text="Parâmetros", padding="5")
        frame_params.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.criar_slider(frame_params, "Taxa de Poupança (s)", 's_rate', 0.0, 1.0)
        self.criar_slider(frame_params, "Difusão Tec. (D_A)", 'D_A', 0.0, 2.0)
        self.criar_slider(frame_params, "Taxa Inovação (xi)", 'xi', 0.0, 0.1)
        self.criar_slider(frame_params, "Poluição por Prod. (mu)", 'mu', 0.0, 0.1)
        self.criar_slider(frame_params, "Depuração Poluição (nu)", 'nu', 0.0, 0.5)
        self.criar_slider(frame_params, "Mobilidade Pop. (m_L)", 'm_L', 0.0, 1.0)
        
    def criar_slider(self, parent, label, param_name, min_val, max_val):
        # Frame container para o item de controle (Label em cima, Slider+Entry embaixo)
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)
        
        # Label na linha de cima
        lbl = ttk.Label(frame, text=label)
        lbl.pack(side=tk.TOP, anchor=tk.W, padx=5)
        
        # Frame para Slider e Entry na linha de baixo
        subframe = ttk.Frame(frame)
        subframe.pack(fill=tk.X, expand=True)
        
        # Variável Tkinter para rastrear o valor
        var = tk.DoubleVar(value=getattr(self.params, param_name))
        
        # Entry
        entry = ttk.Entry(subframe, width=8)
        
        def update_from_slider(val):
            float_val = float(val)
            setattr(self.params, param_name, float_val)
            current_text = entry.get()
            new_text = f"{float_val:.3f}"
            if current_text != new_text:
                entry.delete(0, tk.END)
                entry.insert(0, new_text)

        def update_from_entry(event):
            try:
                val = float(entry.get())
                val = max(min_val, min(max_val, val))
                var.set(val)
                setattr(self.params, param_name, val)
            except ValueError:
                pass

        # Slider expandindo
        scale = ttk.Scale(subframe, from_=min_val, to=max_val, variable=var, command=update_from_slider)
        scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Entry na direita
        entry.pack(side=tk.RIGHT, padx=5)
        entry.insert(0, f"{var.get():.3f}")
        entry.bind('<Return>', update_from_entry)
        entry.bind('<FocusOut>', update_from_entry)

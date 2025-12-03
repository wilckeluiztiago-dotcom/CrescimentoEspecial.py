import numpy as np
from .parametros import Parametros

class Estado:
    """
    Armazena o estado atual do sistema (grades 2D para todas as variáveis).
    """
    def __init__(self, params: Parametros):
        self.params = params
        shape = (params.Nx, params.Ny)
        
        # Inicialização das grades (Condições Iniciais)
        # Podemos adicionar ruído ou condições específicas depois
        self.K = np.ones(shape) * 1.0  # Capital Físico
        self.H = np.ones(shape) * 1.0  # Capital Humano
        self.A = np.ones(shape) * 1.0  # Tecnologia
        self.P = np.zeros(shape)       # Poluição
        self.L = np.ones(shape) * 1.0  # População
        self.B = np.ones(shape) * 1.0  # Recursos Naturais (Fixo por enquanto)
        
        # Variáveis derivadas (para visualização/cálculo)
        self.Y = np.zeros(shape)       # Produto
        self.W = np.zeros(shape)       # Salário
        self.U = np.zeros(shape)       # Utilidade
        
        # Configurar grade espacial
        self.dx = params.L_x / params.Nx
        self.dy = params.L_y / params.Ny
        self.x = np.linspace(0, params.L_x, params.Nx)
        self.y = np.linspace(0, params.L_y, params.Ny)
        self.X, self.Y_grid = np.meshgrid(self.x, self.y)

    def inicializar_com_ruido(self, nivel=0.1):
        """Adiciona uma perturbação aleatória às condições iniciais."""
        shape = self.K.shape
        self.K += np.random.normal(0, nivel, shape)
        self.H += np.random.normal(0, nivel, shape)
        self.A += np.random.normal(0, nivel, shape)
        self.L += np.random.normal(0, nivel, shape)
        
        # Garantir positividade
        self.K = np.maximum(self.K, 0.1)
        self.H = np.maximum(self.H, 0.1)
        self.A = np.maximum(self.A, 0.1)
        self.L = np.maximum(self.L, 0.1)

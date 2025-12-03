import unittest
import numpy as np
import sys
import os

# Adicionar diretório raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.model.parametros import Parametros
from src.model.estado import Estado
from src.model.dinamica import Dinamica

class TestModelo(unittest.TestCase):
    def setUp(self):
        self.params = Parametros(Nx=20, Ny=20, dt=0.1)
        self.estado = Estado(self.params)
        self.estado.inicializar_com_ruido()
        self.dinamica = Dinamica(self.params)

    def test_nao_negatividade(self):
        """Verifica se as variáveis permanecem não-negativas após um passo."""
        self.dinamica.passo(self.estado)
        
        self.assertTrue(np.all(self.estado.K >= 0), "Capital Físico negativo")
        self.assertTrue(np.all(self.estado.H >= 0), "Capital Humano negativo")
        self.assertTrue(np.all(self.estado.A >= 0), "Tecnologia negativa")
        self.assertTrue(np.all(self.estado.P >= 0), "Poluição negativa")
        self.assertTrue(np.all(self.estado.L >= 0), "População negativa")

    def test_evolucao(self):
        """Verifica se o estado muda após vários passos."""
        K_inicial = self.estado.K.copy()
        
        for _ in range(10):
            self.dinamica.passo(self.estado)
            
        # Verifica se houve mudança (não estático)
        self.assertFalse(np.allclose(self.estado.K, K_inicial), "Estado não evoluiu")

    def test_conservacao_massa_aprox(self):
        """Verifica se não há explosão numérica imediata."""
        for _ in range(50):
            self.dinamica.passo(self.estado)
            
        self.assertTrue(np.all(np.isfinite(self.estado.K)), "Explosão numérica em K")

if __name__ == '__main__':
    unittest.main()

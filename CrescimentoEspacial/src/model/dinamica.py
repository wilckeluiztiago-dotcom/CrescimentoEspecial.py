import numpy as np
from scipy.ndimage import laplace, convolve
from .parametros import Parametros
from .estado import Estado

class Dinamica:
    """
    Implementa as equações de evolução temporal (EDPs).
    """
    def __init__(self, params: Parametros):
        self.p = params
        # Kernel para spillovers globais (pré-calculado seria melhor, mas faremos simples aqui)
        # Para eficiência, usaremos uma aproximação ou um kernel pequeno se a grade for grande.
        # Aqui, criamos um kernel gaussiano/exponencial para convolução.
        self.kernel_spillover = self._criar_kernel_spillover()

    def _criar_kernel_spillover(self):
        # Cria um kernel 2D para aproximar a integral global
        # Integral exp(-|x-y|)
        # Limitamos o tamanho do kernel para desempenho (ex: 11x11 ou tamanho da grade)
        # Se a grade for pequena (50x50), podemos usar full.
        range_x = np.linspace(-self.p.L_x/2, self.p.L_x/2, self.p.Nx)
        range_y = np.linspace(-self.p.L_y/2, self.p.L_y/2, self.p.Ny)
        XX, YY = np.meshgrid(range_x, range_y)
        dist = np.sqrt(XX**2 + YY**2)
        kernel = np.exp(-dist)
        return kernel / np.sum(kernel) # Normalizar para manter escala controlada

    def calcular_derivadas_espaciais(self, Z, dx, dy):
        """Calcula Laplaciano e Gradiente."""
        # Laplaciano (Diferenças Finitas centrais)
        # scipy.ndimage.laplace usa padding, precisamos cuidar das bordas se necessário.
        # Aqui assumimos condições de contorno reflexivas (mode='nearest')
        lap = laplace(Z, mode='nearest') / (dx * dy) # Aproximação simples assumindo dx=dy
        
        # Gradiente
        grad_y, grad_x = np.gradient(Z, dy, dx)
        
        return lap, grad_x, grad_y

    def passo(self, estado: Estado):
        p = self.p
        dt = p.dt
        dx, dy = estado.dx, estado.dy
        
        # 1. Calcular Produção Y
        # Y = A^alpha * K^beta * H^gamma * L^(1-alpha-beta-gamma) * B^phi
        # Assumindo retornos constantes de escala se phi não for dado explicitamente para fechar em 1
        expoente_L = 1.0 - p.alpha - p.beta - p.gamma
        Y = (estado.A ** p.alpha) * (estado.K ** p.beta) * (estado.H ** p.gamma) * (estado.L ** expoente_L) * (estado.B ** p.phi)
        estado.Y = Y # Atualiza para visualização
        
        # 2. Dinâmica do Capital Físico (K)
        # dK/dt = s(Y) - delta K + D_K lap(K) - eta K P
        lap_K, _, _ = self.calcular_derivadas_espaciais(estado.K, dx, dy)
        dK = (p.s_rate * Y) - (p.delta_K * estado.K) + (p.D_K * lap_K) - (p.eta * estado.K * estado.P)
        
        # 3. Dinâmica do Capital Humano (H)
        # Salário w = dY/dH = gamma * Y / H
        w = p.gamma * Y / (estado.H + 1e-6) # Evitar divisão por zero
        estado.W = w
        
        # Termo de migração: - div(v_H * H * grad(w))
        # = - v_H * [ grad(H).grad(w) + H * lap(w) ]
        # Ou numericamente: calcular fluxo J = v_H * H * grad(w) e depois -div(J)
        _, grad_w_x, grad_w_y = self.calcular_derivadas_espaciais(w, dx, dy)
        fluxo_x = p.v_H * estado.H * grad_w_x
        fluxo_y = p.v_H * estado.H * grad_w_y
        # Divergente do fluxo
        # Divergente do fluxo
        # np.gradient retorna (grad_axis_0, grad_axis_1) -> (grad_y, grad_x)
        _, div_fluxo_x = np.gradient(fluxo_x, dy, dx) # queremos d(fluxo_x)/dx
        div_fluxo_y, _ = np.gradient(fluxo_y, dy, dx) # queremos d(fluxo_y)/dy
        migracao_H = -(div_fluxo_x + div_fluxo_y)
        
        lap_H, _, _ = self.calcular_derivadas_espaciais(estado.H, dx, dy)
        dH = (p.lam * estado.H * (estado.A ** p.sigma) * (estado.H ** (1-p.sigma))) + \
             (p.D_H * lap_H) + migracao_H - (p.delta_H * estado.H)

        # 4. Dinâmica Tecnológica (A)
        # Spillovers globais: integral
        # Usando convolução via FFT para rapidez se o kernel for grande, ou direta.
        # Aqui usamos scipy.ndimage.convolve com o kernel pré-calculado
        # O termo é chi * integral. A integral é a convolução.
        spillover = convolve(estado.A, self.kernel_spillover, mode='nearest')
        
        lap_A, _, _ = self.calcular_derivadas_espaciais(estado.A, dx, dy)
        inovacao = p.xi * (estado.H ** p.psi) * (estado.K ** p.omega) * (1 - estado.A / p.A_max)
        dA = inovacao + (p.D_A * lap_A) + (p.chi * spillover)
        
        # 5. Dinâmica da Poluição (P)
        lap_P, _, _ = self.calcular_derivadas_espaciais(estado.P, dx, dy)
        dP = (p.mu * Y) + (p.D_P * lap_P) - (p.nu * estado.P) - (p.kappa * (estado.P ** 2))
        
        # 6. Dinâmica Populacional (L)
        # Utilidade u = ln(Y/L) - theta * P
        renda_per_capita = Y / (estado.L + 1e-6)
        u = np.log(renda_per_capita + 1e-6) - (p.theta * estado.P)
        estado.U = u
        
        # Migração por utilidade: - div(m_L * L * grad(u))
        _, grad_u_x, grad_u_y = self.calcular_derivadas_espaciais(u, dx, dy)
        fluxo_L_x = p.m_L * estado.L * grad_u_x
        fluxo_L_y = p.m_L * estado.L * grad_u_y
        # Divergente
        _, div_fluxo_L_x = np.gradient(fluxo_L_x, dy, dx)
        div_fluxo_L_y, _ = np.gradient(fluxo_L_y, dy, dx)
        migracao_L = -(div_fluxo_L_x + div_fluxo_L_y)
        
        dL = (p.r * estado.L * (1 - estado.L / p.L_max)) + migracao_L
        
        # Atualização de Euler (Simples)
        estado.K += dK * dt
        estado.H += dH * dt
        estado.A += dA * dt
        estado.P += dP * dt
        estado.L += dL * dt
        
        # Garantir não-negatividade
        estado.K = np.maximum(estado.K, 0)
        estado.H = np.maximum(estado.H, 0)
        estado.A = np.maximum(estado.A, 0)
        estado.P = np.maximum(estado.P, 0)
        estado.L = np.maximum(estado.L, 0)

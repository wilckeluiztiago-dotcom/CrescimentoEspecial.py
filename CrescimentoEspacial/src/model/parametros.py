from dataclasses import dataclass

@dataclass
class Parametros:
    """
    Classe que armazena todos os parâmetros do modelo EDP de Crescimento Econômico Espacial.
    """
    # Dimensões e Espaço
    L_x: float = 100.0  # Tamanho do domínio em X
    L_y: float = 100.0  # Tamanho do domínio em Y
    Nx: int = 50        # Pontos da grade em X
    Ny: int = 50        # Pontos da grade em Y
    dt: float = 0.1     # Passo de tempo
    
    # Função de Produção (Cobb-Douglas Generalizada)
    alpha: float = 0.3  # Elasticidade Tecnologia
    beta: float = 0.3   # Elasticidade Capital Físico
    gamma: float = 0.2  # Elasticidade Capital Humano
    # phi (Recursos Naturais) é implícito ou 1-alpha-beta-gamma se retornos constantes
    phi: float = 0.1    
    
    # Dinâmica do Capital Físico (K)
    s_rate: float = 0.2 # Taxa de poupança (s(Y) = s_rate * Y)
    delta_K: float = 0.05 # Depreciação do capital físico
    D_K: float = 1.0    # Difusão espacial do capital
    eta: float = 0.01   # Custo da poluição no capital
    
    # Dinâmica do Capital Humano (H)
    lam: float = 0.05   # Taxa de aprendizado
    sigma: float = 0.5  # Expoente de aprendizado
    D_H: float = 0.5    # Difusão do conhecimento tácito
    delta_H: float = 0.02 # Depreciação do capital humano
    v_H: float = 0.1    # Mobilidade baseada em salários
    
    # Dinâmica Tecnológica (A)
    xi: float = 0.01    # Taxa de inovação local
    psi: float = 0.5    # Expoente H na inovação
    omega: float = 0.5  # Expoente K na inovação
    A_max: float = 10.0 # Nível tecnológico máximo local
    D_A: float = 0.8    # Difusão tecnológica
    chi: float = 0.05   # Intensidade dos spillovers globais
    
    # Dinâmica da Poluição (P)
    mu: float = 0.02    # Taxa de geração de poluição por produto
    D_P: float = 2.0    # Difusão atmosférica
    nu: float = 0.1     # Depuração natural
    kappa: float = 0.001 # Limiar não-linear de saturação
    
    # Dinâmica Populacional (L)
    r: float = 0.03     # Taxa de crescimento intrínseco
    L_max: float = 100.0 # Capacidade de suporte local
    m_L: float = 0.2    # Mobilidade populacional por utilidade
    theta: float = 1.0  # Peso da poluição na desutilidade

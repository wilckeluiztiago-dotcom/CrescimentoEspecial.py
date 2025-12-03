# Modelo EDP de Crescimento Econômico Espacial

Este projeto implementa uma simulação complexa de crescimento econômico espacial baseada em um sistema acoplado de Equações Diferenciais Parciais (EDPs). O modelo considera a interação entre Capital Físico, Capital Humano, Tecnologia, Poluição e População em um domínio 2D.

## Modelo Matemático

### 1. Variáveis de Estado
- $K(x,t)$: Capital físico
- $H(x,t)$: Capital humano
- $A(x,t)$: Tecnologia
- $P(x,t)$: Poluição
- $L(x,t)$: Densidade populacional
- $B(x,t)$: Recursos naturais (fixo ou dinâmico)

### 2. Equações de Evolução

#### a) Capital Físico
$$ \frac{\partial K}{\partial t} = s(Y) - \delta_K K + D_K \nabla^2 K - \eta K P $$
Onde $Y = A^\alpha K^\beta H^\gamma L^{1-\alpha-\beta-\gamma} B^\phi$ é a produção.

#### b) Capital Humano
$$ \frac{\partial H}{\partial t} = \lambda H A^\sigma H^{1-\sigma} + D_H \nabla^2 H - \nabla \cdot [v_H H \nabla w] - \delta_H H $$
Onde $w = \frac{\partial Y}{\partial H}$ é o salário marginal.

#### c) Tecnologia
$$ \frac{\partial A}{\partial t} = \xi H^\psi K^\omega (1 - \frac{A}{A_{max}}) + D_A \nabla^2 A + \chi \int_\Omega e^{-|x-y|} A(y,t) dy $$

#### d) Poluição
$$ \frac{\partial P}{\partial t} = \mu Y + D_P \nabla^2 P - \nu P - \kappa P^2 $$

#### e) População
$$ \frac{\partial L}{\partial t} = r L (1 - \frac{L}{L_{max}}) - \nabla \cdot [m_L L \nabla u] $$
Onde $u = \ln(Y/L) - \theta P$ é a utilidade per capita.

## Requisitos
- Python 3.x
- NumPy
- Matplotlib
- SciPy
- Tkinter (geralmente incluído no Python)

## Execução
Execute o arquivo principal:
```bash
python main.py
```

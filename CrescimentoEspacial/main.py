import sys
import os

# Adicionar o diretório atual ao path para importar módulos corretamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.gui.janela_principal import JanelaPrincipal

def main():
    app = JanelaPrincipal()
    app.mainloop()

if __name__ == "__main__":
    main()

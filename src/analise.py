# analise.py
from extracao import salvar_dados
from visualizacao import gerar_grafico

def main():
    salvar_dados()
    gerar_grafico(nome_imagem='grafico-cdi.png')

if __name__ == '__main__':
    main()

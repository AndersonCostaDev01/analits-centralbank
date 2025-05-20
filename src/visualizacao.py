# visualizacao.py
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import sys
import os

def gerar_grafico(nome_csv='taxa-cdi.csv', nome_imagem='grafico.png'):
    if not os.path.exists(nome_csv):
        print("Arquivo CSV não encontrado.")
        return

    df = pd.read_csv(nome_csv)
    df['data_hora'] = pd.to_datetime(df['data'] + ' ' + df['hora'])

    plt.figure(figsize=(12, 6))
    sns.lineplot(x='data_hora', y='cdi', data=df, marker='o')
    plt.title('Variação do CDI Simulado ao Longo do Tempo')
    plt.xlabel('Data e Hora')
    plt.ylabel('CDI (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.savefig(nome_imagem)
    print(f"Gráfico salvo como: {nome_imagem}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Informe o nome do arquivo PNG de saída (ex: grafico.png)")
    else:
        gerar_grafico(nome_imagem=sys.argv[1])

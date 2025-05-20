import csv
import json
import os
from datetime import datetime
from random import random
from matplotlib import pyplot as plt
import requests
import pandas as pd
import seaborn as sns


# URL da API do Banco Central
url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados'


# Função para extrair o último valor da API
def extrair_dados():
    try:
        hoje = datetime.today().strftime('%d/%m/%Y')
        url_corrigida = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json&dataInicial=01/01/2024&dataFinal={hoje}'
        headers = {'Accept': 'application/json'}
        
        response = requests.get(url_corrigida, headers=headers)
        response.raise_for_status()
        
        dados = response.json()
        if not dados:
            print("Nenhum dado retornado pela API.")
            return None
        
        return dados[-1]['valor']  # último valor da série
    except requests.exceptions.RequestException as err:
        print('Erro ao buscar dados da API:', err)
        return None



# Função para salvar dados em um arquivo CSV
def salvar_dados():
    valor = extrair_dados()
    if valor is None:
        return

    for _ in range(10):
        agora = datetime.now()
        data_str = agora.strftime('%Y-%m-%d')
        hora_str = agora.strftime('%H:%M:%S')

        cdi = float(valor.replace(',', '.')) + (random() - 0.5)

        modo = 'a' if os.path.exists('dados.csv') else 'w'
        with open('dados.csv', modo, newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if modo == 'w':
                writer.writerow(['data', 'hora', 'cdi'])
            writer.writerow([data_str, hora_str, cdi])


# Função para gerar gráfico com Seaborn
def gerar_grafico():
    if not os.path.exists('dados.csv'):
        print("Nenhum dado disponível para gerar o gráfico.")
        return

    df = pd.read_csv('dados.csv')
    df['data_hora'] = df['data'] + ' ' + df['hora']
    df['data_hora'] = pd.to_datetime(df['data_hora'])

    plt.figure(figsize=(12, 6))
    sns.lineplot(x='data_hora', y='cdi', data=df, marker='o')
    plt.title('Variação do CDI Simulado ao Longo do Tempo')
    plt.xlabel('Data e Hora')
    plt.ylabel('CDI (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()


# Função principal
def main():
    salvar_dados()
    gerar_grafico()


if __name__ == '__main__':
    main()

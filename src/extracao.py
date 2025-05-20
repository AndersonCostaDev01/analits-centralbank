# extracao.py
import csv
import json
import os
from datetime import datetime
from random import random
import requests

def extrair_dados():
    try:
        hoje = datetime.today().strftime('%d/%m/%Y')
        url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json&dataInicial=01/01/2024&dataFinal={hoje}'
        headers = {'Accept': 'application/json'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        dados = response.json()
        if not dados:
            print("Nenhum dado retornado pela API.")
            return None
        return dados[-1]['valor']
    except requests.exceptions.RequestException as err:
        print('Erro ao buscar dados da API:', err)
        return None

def salvar_dados(nome_arquivo='taxa-cdi.csv'):
    valor = extrair_dados()
    if valor is None:
        return

    for _ in range(10):
        agora = datetime.now()
        data_str = agora.strftime('%Y-%m-%d')
        hora_str = agora.strftime('%H:%M:%S')
        cdi = float(valor.replace(',', '.')) + (random() - 0.5)

        modo = 'a' if os.path.exists(nome_arquivo) else 'w'
        with open(nome_arquivo, modo, newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if modo == 'w':
                writer.writerow(['data', 'hora', 'cdi'])
            writer.writerow([data_str, hora_str, cdi])

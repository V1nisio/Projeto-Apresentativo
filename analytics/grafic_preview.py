import matplotlib
matplotlib.use('Agg') 

import matplotlib.pyplot as plt
import requests
import os

def gerar_grafico_dinamico(moeda_destino="USD"):
    try:
        par = f"{moeda_destino}-BRL"
        print(f"Gerando gráfico para: {par}")
        
        url = f"https://economia.awesomeapi.com.br/json/daily/{par}/30"
        r = requests.get(url)
        dados = r.json()

        precos = [float(item['bid']) for item in dados][::-1]

        plt.figure(figsize=(10, 5))
        plt.plot(precos, marker='o', color='#2563eb', linewidth=2) 
        
        plt.title(f"Histórico 30 dias: {moeda_destino} para BRL", fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.5)
        
        diretorio_atual = os.path.dirname(__file__) 
        caminho_img = os.path.join(diretorio_atual, '..', 'static', 'grafico_30_dias.png')
        caminho_img = os.path.abspath(caminho_img)

        plt.savefig(caminho_img)
        plt.close()
        
        print(f"Sucesso! Gráfico salvo em: {caminho_img}")
        return True
    except Exception as e:
        print(f"Erro ao gerar gráfico: {e}")
        return False

if __name__ == "__main__":
    gerar_grafico_dinamico("USD")
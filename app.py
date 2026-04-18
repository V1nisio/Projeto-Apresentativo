from flask import Flask, render_template, request
import requests
from analytics.grafic_preview import gerar_grafico_dinamico

app = Flask(__name__)

def pegar_cotacoes():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,GBP-BRL,BTC-BRL"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    moeda_nome = ""

    if request.method == "POST":
        valor_brl = float(request.form.get("valor", 0))
        moeda_escolhida = request.form.get("moeda_grafico", "USD") 

        dados = pegar_cotacoes()
        if dados:
            resultado = {
                "original": valor_brl,
                "usd": valor_brl / float(dados["USDBRL"]["bid"]),
                "eur": valor_brl / float(dados["EURBRL"]["bid"]),
                "gbp": valor_brl / float(dados["GBPBRL"]["bid"]),
                "btc": valor_brl / float(dados["BTCBRL"]["bid"])
            }

        gerar_grafico_dinamico(moeda_escolhida)

        nomes = {"USD": "do Dólar", "EUR": "do Euro", "GBP": "da Libra", "BTC": "do Bitcoin"}
        moeda_nome = nomes.get(moeda_escolhida, "da Moeda")

    return render_template("index.html", resultado=resultado, moeda_nome=moeda_nome)

if __name__ == "__main__":
    app.run(debug=True)
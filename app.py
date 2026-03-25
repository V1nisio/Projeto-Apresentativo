from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def pegar_cotacoes():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,GBP-BRL"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        valor_brl = float(request.form.get("valor", 0))
        dados = pegar_cotacoes()
        if dados:
            resultado = {
                "original": valor_brl,
                "usd": valor_brl / float(dados["USDBRL"]["bid"]),
                "eur": valor_brl / float(dados["EURBRL"]["bid"]),
                "gbp": valor_brl / float(dados["GBPBRL"]["bid"])
            }
    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS 
from modelo import ModeloBigrama
from storage import carregar_modelo, salvar_modelo
from corpus_loader import carregar_corpus 

app = Flask(__name__)
CORS(app)

modelo = ModeloBigrama()

if not carregar_modelo(modelo):
    carregar_corpus(modelo)

@app.post("/treinar")
def treinar():
    data = request.get_json()
    frase = data.get("frase", "")
    
    if not frase:
        return jsonify({"erro": "frase vazia"}), 400
    modelo.treinar(frase)
    salvar_modelo(modelo)
    total_bigramas = sum(len(v) for v in modelo.bigram_counts.values())
    return jsonify({"ok": True, "bigramas": total_bigramas, "frases_treinadas": modelo.sentences_trained})

@app.get("/sugerir")
def sugerir():
    q = request.args.get("q", "")
    tokens = modelo.tokenizar(q)
    if not tokens:
        return jsonify([])
    return jsonify(modelo.sugerir_proxima(tokens[-1]))

@app.get("/frases")
def frases():
    q = request.args.get("q", "")
    return jsonify(modelo.gerar_frases(q))

@app.get("/status")
def status():
    total_bigramas = sum(len(v) for v in modelo.bigram_counts.values())
    return jsonify({"bigramas": total_bigramas, "frases_treinadas": modelo.sentences_trained})    

if __name__ == "__main__":
    app.run(debug=True)
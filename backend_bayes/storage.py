import json
import os
from collections import defaultdict, Counter

MODELO_PATH = "data/modelo.json"

def salvar_modelo(modelo):
    dados = {
        "bigram_counts": {w1: dict(w2s) for w1, w2s in modelo.bigram_counts.items()},
        "final_words": list(modelo.final_words),
        "sentences_trained": modelo.sentences_trained
    }
    os.makedirs("data", exist_ok=True)
    with open(MODELO_PATH, "w", encoding ="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def carregar_modelo(modelo):
    if not os.path.exists(MODELO_PATH):
        return False
    with open(MODELO_PATH, "r", encoding="utf-8") as f:
        dados = json.load(f)
    modelo.bigram_counts = defaultdict(Counter, { w1: Counter(w2s) for w1, w2s in dados["bigram_counts"].items()})
    modelo.final_words = set(dados["final_words"])
    modelo.sentences_trained = dados["sentences_trained"]
    return True
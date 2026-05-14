import nltk
from storage import MODELO_PATH, salvar_modelo
import os

def carregar_corpus(modelo):
    if os.path.exists(MODELO_PATH):
        return

    print("Nenhum modelo encontrado. Carregando corpus mac_morpho...")
    nltk.download("mac_morpho", quiet=True)

    sentencas = nltk.corpus.mac_morpho.sents()
    total = len(sentencas)

    for i, sentenca in enumerate(sentencas):
        palavras = [token.lower() for token in sentenca]
        frase = " ".join(palavras)
        modelo.treinar(frase)
        if i % 5000 == 0:
            print(f" {i}/{total} sentenças processadas...")

    salvar_modelo(modelo)
    print(f"Corpus carregado. {modelo.sentences_trained} frases, {sum(len(v) for v in modelo.bigram_counts.values())} bigramas.")
import re
from collections import defaultdict, Counter

class ModeloBigrama:
    def __init__(self):
        self.bigram_counts = defaultdict(Counter)
        self.final_words = set()
        self.sentences_trained = 0

    def tokenizar(self, frase: str) -> list[str]:
        frase = frase.lower()
        frase = re.sub(r"[^a-záéíóúâêîôûàãõç\s]", " ", frase)
        tokens = [t for t in frase.split() if t]
        return tokens
    
    def treinar(self, frase: str):
        tokens = self.tokenizar(frase)
        if len(tokens) < 2:
            return
        for i in range(len(tokens) - 1):
            w1, w2 = tokens[i], tokens[i + 1]
            self.bigram_counts[w1][w2] += 1
        self.final_words.add(tokens[-1])
        self.sentences_trained =+ 1

    def calcular_probabilidade(self, w1:str, w2:str) -> float:
        total = sum(self.bigram_counts[w1].values())
        if total == 0:
            return 0.0
        return self.bigram_counts[w1][w2]/total

    def sugerir_proxima(self, palavra: str, n: int = 5) -> list:
        if palavra in self.final_words and palavra not in self.bigram_counts:
            return []
        contagens = self.bigram_counts.get(palavra, {})
        if not contagens:
            return []
        sugestoes = [
            {"palavra": w2, "probabilidade": self.calcular_probabilidade(palavra, w2)}
            for w2 in contagens
        ]
        sugestoes.sort(key=lambda x: x["probabilidade"], reverse=True)
        return sugestoes[:n]

    def gerar_frases(self, texto: str, k: int = 5, max_tokens: int = 8) -> list:
        tokens = self.tokenizar(texto)
        if not tokens:
            return []
        frases = []
        for _ in range(k):
            atual = tokens[-1]
            frase = tokens[:]
            prob_acumulada = 1.0

            while len(frase) < max_tokens:
                if atual in self.final_words:
                    break
                sugestoes = self.sugerir_proxima(atual, n=1)
                if not sugestoes:
                    break
                prox = sugestoes[0]["palavra"]
                prob_acumulada *= sugestoes[0]["probabilidade"]
                frase.append(prox)
                atual = prox
            
            frases.append({"frase": " ".join(frase), "probabilidade": round(prob_acumulada, 6)})
        return frases
        
        

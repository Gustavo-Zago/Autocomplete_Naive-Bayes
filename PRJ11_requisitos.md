# PRJ.11 — Autocomplete com Naive Bayes
## Documento de Requisitos de Software

**Versão:** 1.0  
**Data:** 20/04/2026  
**Status:** Em revisão

---

## 1. Visão Geral

Sistema web de autocompletar texto baseado em modelo de linguagem por bigramas com probabilidade condicional (princípio Naive Bayes), treinado incrementalmente por frases fornecidas pelo usuário e por corpus externo em português (NLTK `mac_morpho`). A interface replica a estética visual do Google circa 1998–2002.

**Stack:** React (Vite) + Python (Flask) + JSON para persistência.

---

## 2. Requisitos Funcionais

### RF01 — Treinamento por frase do usuário
O sistema deve aceitar frases digitadas pelo usuário, tokenizá-las em letras minúsculas (removendo pontuação) e atualizar o modelo de bigramas em memória e em arquivo persistente.

**Critério de aceite:** Após submeter a frase `"quem descobriu o Brasil"`, o bigrama `(quem → descobriu)` deve existir no modelo com contagem ≥ 1.

---

### RF02 — Treinamento por corpus externo
O sistema deve, na primeira inicialização, carregar e processar o corpus `mac_morpho` do NLTK para popular o modelo base com bigramas do português brasileiro.

**Critério de aceite:** Ao iniciar sem `modelo.json`, o sistema processa o corpus e salva o arquivo antes de aceitar requisições.

---

### RF03 — Persistência do modelo
O modelo (dicionário de bigramas com contagens + conjunto de palavras finais) deve ser salvo em `modelo.json` após cada atualização via frase do usuário. Ao iniciar, o sistema carrega o arquivo se existir.

**Critério de aceite:** Após treinar uma frase, encerrar o servidor e reiniciar, o bigrama treinado ainda deve estar disponível.

---

### RF04 — Sugestão de próxima palavra
Dado o último token do texto digitado, o sistema retorna as N palavras mais prováveis como próxima palavra, ordenadas por:

```
P(w2 | w1) = count(w1 → w2) / Σ count(w1 → k)
```

**Critério de aceite:** `GET /sugerir?q=quem` retorna lista com `"descobriu"` e `"mexeu"`, com `"descobriu"` primeiro se aparecer mais vezes.

---

### RF05 — Sugestão de frases completas
O sistema deve gerar as K frases completas mais prováveis a partir do texto digitado, encadeando bigramas recursivamente — sempre escolhendo a próxima palavra mais provável — até atingir uma palavra final ou um limite de comprimento (máximo 8 tokens).

**Critério de aceite:** Digitando `"quem"`, o sistema retorna frases como `"quem descobriu o Brasil"` com sua probabilidade acumulada.

---

### RF06 — Regra de palavra final
Palavras que aparecem **exclusivamente** em posição final de frases no corpus treinado não devem gerar sugestão de continuação.

**Critério de aceite:** Após treinar `"quem descobriu o Brasil"`, a palavra `"Brasil"` (exclusivamente final) não deve retornar sugestões.

---

### RF07 — Sugestões em tempo real
As sugestões devem aparecer enquanto o usuário digita, com debounce de 300ms, sem necessidade de pressionar Enter.

**Critério de aceite:** Ao digitar `"qu"` → `"que"` → `"quem"`, sugestões aparecem automaticamente após 300ms de inatividade, sem nenhum botão de submissão.

---

### RF08 — Aceitar sugestão via interação
O usuário deve poder selecionar uma sugestão com clique do mouse ou com as teclas `↑` `↓` para navegar e `Tab` ou `Enter` para aceitar, inserindo a sugestão completa no campo de texto.

**Critério de aceite:** Após aceitar uma sugestão, o campo de texto exibe a frase sugerida completa e novas sugestões são recalculadas.

---

### RF09 — Interface estilo Google anos 90
A UI deve replicar a estética do Google circa 1998–2002: logo colorido centralizado, campo único de busca centralizado, dropdown de sugestões abaixo do campo.

**Critério de aceite:** Interface revisada e aprovada pela dupla antes da apresentação.

---

### RF10 — Status do modelo
A interface deve exibir quantos bigramas e quantas frases o modelo já aprendeu.

**Critério de aceite:** `GET /status` retorna `{ bigramas: N, frases_treinadas: M }` e esses valores aparecem na interface.

---

## 3. Requisitos Não Funcionais

### RNF01 — Implementação do modelo em Python puro
A lógica do modelo (tokenização, contagem de bigramas, cálculo de probabilidade, predição) deve ser implementada sem uso de bibliotecas de ML (`sklearn`, `nltk.NaiveBayesClassifier`, `torch`, etc.). O NLTK é permitido **apenas** para acesso ao corpus.

### RNF02 — Stack definida
- **Backend:** Python 3.11+ com Flask
- **Frontend:** React 18+ com Vite e TypeScript
- **Persistência:** arquivo `modelo.json` local
- **Corpus:** NLTK `mac_morpho`

### RNF03 — Tempo de resposta
Sugestões devem ser retornadas em menos de 200ms para consultas ao modelo já carregado em memória.

### RNF04 — Portabilidade
O projeto deve rodar localmente com no máximo dois comandos (ex: `pip install -r requirements.txt && python app.py` e `npm install && npm run dev`).

### RNF05 — Prazo estimado
3 a 4 semanas a partir do início do desenvolvimento.

---

## 4. User Stories

### US01 — Treinar com minha frase
> **Como** usuário,  
> **quero** digitar uma frase e adicioná-la ao modelo,  
> **para que** o sistema aprenda as relações entre as palavras que eu uso.

**Critério de aceite:**
- Campo dedicado para inserção de frases de treino
- Ao submeter, modelo é atualizado e persistido imediatamente
- Contador de bigramas/frases é incrementado visualmente

---

### US02 — Ver sugestões enquanto digito
> **Como** usuário,  
> **quero** ver sugestões de próximas palavras enquanto digito,  
> **para que** eu possa completar meu texto mais rápido.

**Critério de aceite:**
- Sugestões aparecem automaticamente após 300ms sem digitar
- Exibe no máximo 5 sugestões
- Cada sugestão mostra a frase completa e a probabilidade acumulada

---

### US03 — Aceitar sugestão com teclado ou mouse
> **Como** usuário,  
> **quero** selecionar uma sugestão com `Tab`, `Enter` ou clique,  
> **para que** eu não precise redigitar a palavra sugerida.

**Critério de aceite:**
- `↑` `↓` navegam entre sugestões
- `Tab` ou `Enter` aceitam a sugestão destacada
- Clique no item também aceita a sugestão

---

### US04 — Modelo persistente entre sessões
> **Como** usuário,  
> **quero** que o modelo lembre das frases que treinei anteriormente,  
> **para que** eu não precise retreinar toda vez que abro o sistema.

**Critério de aceite:**
- Ao reiniciar o servidor, frases treinadas anteriormente ainda geram sugestões
- Status exibe o número correto de bigramas carregados

---

### US05 — Sugestões baseadas em corpus real
> **Como** usuário,  
> **quero** que o sistema já funcione minimamente antes de eu treinar qualquer frase,  
> **para que** as sugestões sejam úteis desde o primeiro uso.

**Critério de aceite:**
- Na primeira inicialização, corpus `mac_morpho` é carregado automaticamente
- Palavras comuns do português já geram sugestões antes de qualquer treino manual

---

### US06 — Não sugerir após palavras finais
> **Como** usuário,  
> **quero** que o sistema não sugira continuação de palavras que encerram frases,  
> **para que** as sugestões façam sentido semântico.

**Critério de aceite:**
- Palavras exclusivamente finais no corpus não geram dropdown de sugestão
- Comportamento verificável digitando uma palavra sabidamente final

---

## 5. Backlog Priorizado

| ID | User Story | Prioridade | Estimativa | Sprint |
|----|-----------|-----------|------------|--------|
| B01 | Estrutura base do projeto (monorepo, Flask, Vite) | Alta | 0.5 dia | 1 |
| B02 | Modelo de bigramas em Python puro (US01, US06) | Alta | 1 dia | 1 |
| B03 | Carregamento do corpus mac_morpho (US05) | Alta | 0.5 dia | 1 |
| B04 | Persistência em modelo.json (US04) | Alta | 0.5 dia | 1 |
| B05 | API REST — endpoints `/treinar`, `/sugerir`, `/frases`, `/status` | Alta | 1 dia | 1 |
| B06 | Geração de frases completas por encadeamento (US02) | Alta | 1 dia | 2 |
| B07 | Frontend React — campo de busca + debounce (US02) | Alta | 1 dia | 2 |
| B08 | Frontend React — dropdown de sugestões (US02, US03) | Alta | 1 dia | 2 |
| B09 | Navegação por teclado no dropdown (US03) | Média | 0.5 dia | 2 |
| B10 | Campo de treino manual na interface (US01) | Média | 0.5 dia | 2 |
| B11 | Estilo visual Google anos 90 (RF09) | Média | 1 dia | 3 |
| B12 | Contador de status na interface (RF10) | Baixa | 0.5 dia | 3 |
| B13 | Testes manuais e ajustes finais | Baixa | 1 dia | 3 |

---

## 6. Tasks por Backlog Item

### B01 — Estrutura base do projeto
- [ ] Criar monorepo com pastas `/backend` e `/frontend`
- [ ] Inicializar projeto Flask em `/backend/app.py`
- [ ] Inicializar Vite + React + TypeScript em `/frontend`
- [ ] Criar `requirements.txt` com Flask e NLTK
- [ ] Criar `README.md` com instruções de setup

### B02 — Modelo de bigramas em Python puro
- [ ] Criar `modelo.py` com classe `ModeloBigrama`
- [ ] Implementar `tokenizar(frase: str) -> list[str]`
- [ ] Implementar `treinar(frase: str)` — atualiza `bigram_counts` e `final_words`
- [ ] Implementar lógica de separação entre `final_words` e `non_final_words`
- [ ] Implementar `calcular_probabilidade(w1, w2) -> float`
- [ ] Implementar `sugerir_proxima(palavra, n=5) -> list[tuple]`

### B03 — Carregamento do corpus mac_morpho
- [ ] Criar `corpus_loader.py`
- [ ] Implementar download automático do corpus via `nltk.download`
- [ ] Implementar `carregar_corpus()` que itera as sentenças e chama `treinar()`
- [ ] Executar apenas se `modelo.json` não existir

### B04 — Persistência em modelo.json
- [ ] Implementar `salvar_modelo()` — serializa `bigram_counts` e `final_words` em JSON
- [ ] Implementar `carregar_modelo()` — desserializa e restaura o estado
- [ ] Chamar `salvar_modelo()` após cada `treinar()` via usuário

### B05 — API REST
- [ ] `POST /treinar` — recebe `{ frase: string }`, treina e retorna status
- [ ] `GET /sugerir?q=palavra` — retorna `[{ palavra, probabilidade }]`
- [ ] `GET /frases?q=texto` — retorna `[{ frase, probabilidade }]`
- [ ] `GET /status` — retorna `{ bigramas, frases_treinadas }`
- [ ] Configurar CORS para aceitar requisições do frontend React

### B06 — Geração de frases completas
- [ ] Implementar `gerar_frases(texto, k=5, max_tokens=8) -> list[tuple]`
- [ ] Lógica de encadeamento: dado o último token, anexar a palavra mais provável até atingir palavra final ou limite
- [ ] Calcular probabilidade acumulada da frase: `P(frase) = ∏ P(wi | wi-1)`

### B07 — Campo de busca com debounce
- [ ] Criar componente `SearchBox.tsx`
- [ ] Hook `useDebounce(value, delay)` — atrasa o disparo da busca em 300ms
- [ ] Chamada ao endpoint `GET /frases?q=...` a cada mudança com debounce
- [ ] Gerenciar estado de loading durante a requisição

### B08 — Dropdown de sugestões
- [ ] Criar componente `Suggestions.tsx`
- [ ] Renderizar lista de sugestões com frase + probabilidade formatada
- [ ] Fechar ao clicar fora (`useEffect` com listener no `document`)
- [ ] Ao clicar em sugestão, preencher o campo e fechar dropdown

### B09 — Navegação por teclado
- [ ] Capturar teclas `↑`, `↓`, `Tab`, `Enter` no `SearchBox`
- [ ] `↑`/`↓` movem o índice de seleção ativo no dropdown
- [ ] `Tab`/`Enter` aceitam a sugestão ativa
- [ ] `Escape` fecha o dropdown sem aceitar

### B10 — Campo de treino manual
- [ ] Criar componente `TrainInput.tsx`
- [ ] Campo de texto + botão "Adicionar ao modelo"
- [ ] `POST /treinar` ao submeter
- [ ] Exibir feedback de sucesso ("Frase adicionada! +N bigramas")

### B11 — Estilo visual Google anos 90
- [ ] Pesquisar referências visuais do Google 1998–2002
- [ ] Criar logo "PRJ.11" com letras coloridas (azul, vermelho, amarelo, verde)
- [ ] Estilizar campo de busca centralizado com borda simples e sombra discreta
- [ ] Estilizar dropdown com fundo branco, bordas finas, hover cinza claro
- [ ] Escolher tipografia adequada (Arial ou Times, conforme época)
- [ ] Layout centralizado vertical e horizontalmente

### B12 — Contador de status
- [ ] Criar componente `ModelStatus.tsx`
- [ ] Chamar `GET /status` ao montar e após cada treino
- [ ] Exibir: "Modelo com X bigramas — Y frases treinadas"

### B13 — Testes manuais e ajustes finais
- [ ] Treinar as frases do enunciado e verificar RF06 (palavras finais)
- [ ] Testar fluxo completo: digitar → ver sugestão → aceitar → nova sugestão
- [ ] Testar persistência: treinar → encerrar servidor → reiniciar → verificar
- [ ] Verificar tempo de resposta < 200ms nas sugestões
- [ ] Revisão visual da interface com a dupla

---

## 7. Fora do Escopo

- Autenticação ou multiusuário
- Deploy em nuvem
- Suporte a múltiplos idiomas
- Correção ortográfica
- Trigramas ou n-gramas de ordem maior (possível evolução futura)
- Testes automatizados (unitários/integração)

---

## 8. Glossário

| Termo | Definição |
|-------|-----------|
| **Bigrama** | Par de palavras consecutivas `(w1, w2)` extraído de uma frase |
| **Palavra final** | Palavra que aparece exclusivamente na última posição das frases treinadas |
| **Probabilidade condicional** | `P(w2 \| w1)` — chance de `w2` aparecer dado que a palavra anterior é `w1` |
| **Encadeamento** | Processo de gerar uma frase completa conectando bigramas sequencialmente |
| **Corpus** | Conjunto de textos usados para treinar o modelo (aqui: `mac_morpho`) |
| **Debounce** | Técnica que atrasa a execução de uma função até que o usuário pare de digitar |
| **Persistência** | Capacidade do modelo de salvar e recuperar seu estado entre execuções |


# Decisões técnicas

> RASCUNHO: reescreva com suas palavras e experiências reais antes de entregar. Você precisa saber explicar cada linha.

## Por que este tema

Quero trabalhar com DevOps, e quem faz pipeline convive com logs de erro enormes e difíceis de ler. Uma IA é boa em ler texto bagunçado e propor hipóteses, então o Pipeline Doctor une as duas coisas da trilha: DevOps e IA Generativa.

## Stack e por quê

- **Python + FastAPI:** poucas linhas para uma API com validação automática (Pydantic) e documentação em `/docs`. O mesmo Pydantic define o schema que a IA precisa respeitar.
- **Gemini (google-genai):** tem camada gratuita e suporta saída estruturada (JSON com schema), o que evita parsear texto livre.
- **Frontend HTML/JS puro, servido pelo próprio backend:** uma única URL pública, sem CORS, sem etapa de build. Menos peças para quebrar.
- **pytest + pytest-cov:** padrão do ecossistema Python; o limite de 70% está no `pytest.ini`, então o CI falha sozinho se a cobertura cair.
- **GitHub Actions + Render:** CI gratuito integrado ao repositório e deploy automático a cada push na `main`.

## Segurança

Logs de CI frequentemente contêm segredos. Mandá-los crus para uma API externa seria um vazamento, então criei o redator, que limpa o texto antes da chamada. Também tratei o log como entrada não confiável (prompt injection) e validei a resposta da IA contra um schema.

## Maior dificuldade

(Escreva a sua. Exemplos possíveis: instalar dependências no Python 3.14 sem wheels, ajustar as regex do redator para não remover texto demais, configurar o deploy.)

## O que aprendi

- Simular a IA com mock deixa os testes rápidos, grátis e determinísticos; o código de integração fica isolado numa função pequena (`_chamar_gemini`).
- Validar a saída da IA é tão importante quanto validar a entrada do usuário.
- Cobertura alta não basta: os testes mais valiosos foram os que provam que o segredo nunca chega à IA.

## O que faria diferente

Persistiria o histórico de diagnósticos num banco para detectar falhas recorrentes, trocaria o rate limit em memória por Redis e criaria um GitHub App para comentar o diagnóstico direto no pull request.

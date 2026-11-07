# Decisões

## Por que esse tema

Escolhi fazer um sistema que lê o log de uma falha de CI/CD e explica o que deu errado. Logs de erro são longos, confusos e quase sempre aparecem na hora errada, e entender o que está escrito neles é um bom trabalho para uma IA. Também achei que combinava com a trilha: é um projeto de IA feito para quem trabalha com DevOps.

O ponto que mais me preocupou foi a segurança. Log de pipeline costuma ter token e senha no meio, e mandar isso cru para uma API externa seria vazar segredo. Por isso o sistema passa o log por um filtro que troca esses trechos por `[REDACTED]` antes de qualquer chamada à IA. O log também é tratado como texto não confiável, para ele não conseguir dar ordens ao modelo, e a resposta do Gemini precisa seguir um formato fixo ou é descartada.

## Stack e por quê

- **Python com FastAPI.** É o que me deixa escrever menos código. O Pydantic valida a entrada do usuário e também o formato da resposta da IA.
- **Gemini.** Tem plano gratuito e aceita pedir a resposta em JSON com um schema, então não preciso interpretar texto solto.
- **Frontend em HTML e JavaScript puros, servido pelo próprio backend.** Fica uma URL só, sem CORS e sem etapa de build.
- **SQLite** para o histórico dos últimos diagnósticos. Guarda só o resumo, nunca o log, porque a página é pública.
- **GitHub Actions e Render.** O CI roda os testes e o build do Docker a cada push, e o Render publica sozinho a partir do GitHub.

## Maior dificuldade

A parte que mais deu trabalho foi a integração com o Gemini, porque os testes passavam e a chamada real não funcionava. Com a IA simulada tudo ficava verde, mas na primeira chamada de verdade apareceu um erro de "client has been closed". O cliente da biblioteca estava sendo descartado antes de a resposta chegar, e a solução foi guardá-lo numa variável.

Depois descobri que o modelo que eu tinha escolhido, o `gemini-2.5-flash`, não estava mais disponível para contas novas. O modelo seguinte demorava tanto que estourava o tempo, então coloquei um timeout de 20 segundos. Já em produção, o Gemini devolveu erro 503 por excesso de demanda na minha primeira chamada. Isso me fez criar uma lista de modelos reserva: se um falha, o sistema tenta o próximo.

Também perdi tempo com o Python 3.14 da minha máquina, que não tinha pacotes prontos para as versões que eu tinha fixado. Soltei as versões e deixei o CI no Python 3.12.

## O que aprendi

Mock é ótimo para ter teste rápido, mas não substitui chamar o serviço de verdade pelo menos uma vez. Os três problemas acima só apareceram assim. Aprendi também que serviço externo falha, e que o sistema precisa ter plano para isso, com timeout, fallback e uma mensagem de erro que faça sentido para o usuário.

## O que eu faria diferente

Testaria a integração real com a IA no primeiro dia, e não depois de terminar tudo. Trocaria o SQLite por um Postgres, já que o disco do plano gratuito do Render é apagado a cada reinício e o histórico some. E criaria um GitHub App para comentar o diagnóstico direto no pull request que falhou, que é onde a pessoa realmente precisa dele.

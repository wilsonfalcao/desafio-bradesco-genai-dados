# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores |
| `perfil_investidor.json` | JSON | Personalizar recomendações |
| `produtos_financeiros.json` | JSON | Sugerir produtos adequados ao perfil |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente |

> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Não, usei as poucas informações já disponíveis.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

[ex: Os JSON/CSV são carregados no início da sessão e incluídos no contexto do prompt]

O agente acessa a base de conhecimento através do retorno da função carregar_contexto onde seta todo o prompt com contexto do agente e informações de antendimento e estratégias financeiras.


### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Sim, o dados de análise de perfil, histórico, transações e produtos são setado diretamente no prompt e são carregados uma única vez.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
--- PERFIL DO INVESTIDOR ---
Nome: {perfil['nome']}
Idade: {perfil['idade']}
Profissão: {perfil['profissao']}
Renda Mensal: R$ {perfil['renda_mensal']}
Perfil de Risco: {perfil['perfil_investidor'].upper()}
Objetivo Principal: {perfil['objetivo_principal']}
Patrimônio Total: R$ {perfil['patrimonio_total']}
Reserva de Emergência Atual: R$ {perfil['reserva_emergencia_atual']}
Aceita Risco: {'Sim' if perfil['aceita_risco'] else 'Não'}

--- RESUMO FINANCEIRO DO MÊS ---
Entradas Totais: R$ {total_entradas:.2f}
Saídas Totais: R$ {total_saidas:.2f}
Saldo Restante: R$ {saldo_mes:.2f}

--- ÚLTIMAS TRANSAÇÕES ---
        {lista_transacoes}

--- METAS ATUAIS ---
{json.dumps(perfil['metas'], indent=2, ensure_ascii=False)}
...
```

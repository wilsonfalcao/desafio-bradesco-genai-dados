import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

st.set_page_config(
    page_title="MacGyver - Agente Financeiro",
    page_icon="👱‍♂️",
    layout="centered"
)

st.markdown("""
# 👱‍♂️ MacGyver  
### Agente Financeiro Estratégico

Calma, calma… deixa eu analisar seus dados financeiros com atenção, sempre deve ter um jeito de fazer esse saldo parado trabalhar melhor, 
com lógica, segurança e liquidez, sem pressão comercial, 
sem promessas irreais, apenas estratégia baseada em dados concretos.
""")

st.divider()

@st.cache_data
def carregar_contexto_cliente(perfil_path, produtos_path, historico_csv_path, transacoes_csv_path):
    try:
        
        with open(produtos_path, "r", encoding="utf-8") as f:
            produtos = json.load(f)
            
        with open(perfil_path, "r", encoding="utf-8") as f:
            perfil = json.load(f)

        transacoes_df = pd.read_csv(transacoes_csv_path)
        historico_df = pd.read_csv(historico_csv_path)

        total_entradas = transacoes_df[transacoes_df['tipo'] == 'entrada']['valor'].sum()
        total_saidas = transacoes_df[transacoes_df['tipo'] == 'saida']['valor'].sum()
        saldo_mes = total_entradas - total_saidas

        lista_transacoes = ""
        for _, row in transacoes_df.tail(10).iterrows():
            lista_transacoes += f"- {row['data']}: {row['descricao']} ({row['categoria']}) | R$ {row['valor']} [{row['tipo']}]\n"

        prompt = f"""
        Você é MacGyver, um agente financeiro educativo, direto, lógico e equilibrado, inspirado no comportamento estratégico e didático de Angus MacGyver
        da série MacGyver; sua função é ajudar correntistas a identificar oportunidades de otimização de saldo parado em conta corrente.
        
        IMPORTANTE:
        Você deve atuar em formato de CONVERSA.
        NUNCA entregue análise completa na primeira resposta.
        Sua comunicação deve ser progressiva e em etapas.
        Seu objetivo é atender cada cliente entendendo o saldo parado em estratégia inteligente de curto prazo com liquidez, segurança e coerência com o perfil do cliente,
        sempre com base estrita nos dados fornecidos e admitindo explicitamente quando algo não puder ser determinado com segurança.

        USE AS EXPRESSÕES:
        mantenha a calma diante da volatilidade do mercado, calma, calma,
        lembre que sempre deve ter um jeito de reorganizar o orçamento,
        analise cada despesa como recurso estratégico disponível,
        evite decisões impulsivas como quem recusa usar armas,
        prefira estratégia e proteção de capital antes de risco alto,
        diga isso pode funcionar ao testar nova alocação com cautela,
        confia em mim ao apresentar plano baseado em dados concretos,
        isso não estava no plano ao ajustar rota após evento inesperado,
        já fiz coisa pior ao enfrentar ciclos econômicos desafiadores,
        improvise com inteligência usando liquidez e reservas disponíveis,
        pense antes de agir ao avaliar crédito, juros e endividamento,
        use criatividade antes da força bruta ao cortar custos,
        transforme limitações financeiras em soluções estruturadas,
        mantenha postura ética e racional ao recomendar investimentos,
        priorize segurança e consistência antes de buscar ganhos rápidos,
        avalie riscos com serenidade mesmo sob pressão do mercado,
        trate cada crise como oportunidade de ajuste estratégico,
        aja com liderança serena ao orientar decisões patrimoniais.

        EXEMPLOS DE COMUNICAÇÃO:
        Saudação: [ex: "Olá. Tudo bem. Antes de qualquer decisão, preciso entender o cenário completo.Me explica passo a passo"]
        Confirmação: [ex: "Se eu entendi bem, seu foco é liquidez imediata. Antes de avançar, me confirma o prazo que você tem em mente"]
        Erro/Limitação: [ex: "Ok. Não era o plano inicial, mas dá pra contornar. Vou te orientar no próximo passo"]
        
        === REGRAS DE FLUXO ===
        
        ETAPA 1 — DIAGNÓSTICO INICIAL:
        - Apresente-se como MacGyver.
        - Responda de forma curta.
        - Demonstre o que você pode fazer.
        - Valide o perfil de cliente.
        - Faça no máximo 2 perguntas objetivas antes de avançar.
        
        ETAPA 2 — CONFIRMAÇÃO:
        - Só avance se o cliente responder.
        - Valide entendimento com frases como:
          "Certo..."
          "Se eu entendi bem..."
          "Antes de avançar..."
        
        ETAPA 3 — ANÁLISE ESTRATÉGICA:
        - Faça projeções de juros e rendimento apenas com dados (RESUMO FINANCEIRO DO MÊS, Saídas totais, Entradas Totais)
        - Crie projeções de rendimento comparando taxas de juros atual e projetando para frente com no máximo 12 meses
        - Só entregue análise detalhada se o cliente pedir.
        - Caso contrário, mantenha resposta resumida e estruturada.
        - Sempre informe que o calculo é baseado com a taxa de juros atual (Selic ou IPCA) e que são atualizadas conforme o Banco Central
        
        NUNCA:
        - Entregar relatório longo sem solicitação.
        - Projetar rentabilidade futura com mais de 12 meses.
        - Sugerir produtos fora da lista.
        - Inventar dados.
        
        === DADOS DISPONÍVEIS ===
        
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
        
        HISTÓRICO DE ATENDIMENTOS:
        {historico_df.to_string(index=False)}
        
        PRODUTOS PERMITIDOS:
        {json.dumps(produtos, indent=2, ensure_ascii=False)}
        
        === OBJETIVO ===
        Identificar possível saldo ocioso e janela segura de liquidez diária,
        respeitando estritamente os dados fornecidos.
        
        Agora inicie apenas a ETAPA 1.
        """        
        return prompt
    except FileNotFoundError as e:
        return None

with st.sidebar:
    st.header("Configurações")
    api_key = "AIzaSyBNMqnvgdo2N0Pj9CatzI4pm1vetHKATcM" #st.text_input("Insira sua API Key do Google Gemini:", type="password")
    st.markdown("[Obtenha sua chave no Google AI Studio](https://aistudio.google.com/)")

contexto_sistema = carregar_contexto_cliente(
    "data/perfil_investidor.json",
    "data/produtos_financeiros.json",
    "data/historico_atendimento.csv",
    "data/transacoes.csv"
)

if contexto_sistema is None:
    st.error("Erro: Arquivos de base de dados não encontrados. Certifique-se de que os arquivos .csv e .json estão na mesma pasta do `app.py`.")
    st.stop()

if api_key:

    genai.configure(api_key=api_key)

    configuracao = {
        "temperature": 0.2,
        "top_p": 0.95,
        "max_output_tokens": 1024,
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=contexto_sistema,
        generation_config=configuracao
    )
    
    
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
        
    
    for message in st.session_state.chat_session.history:
        role = "user" if message.role == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

    cols = st.columns(3)
    acao = None
    if cols[0].button("💰 Analisar Saldo"):
        acao = "Quanto sobrou do meu salário e o que faço com isso?"
    if cols[1].button("📈 Ver Investimentos"):
        acao = "Quais produtos combinam com meu perfil moderado?"
    if cols[2].button("🚩 Alerta de Gastos"):
        acao = "Tive algum gasto excessivo nas minhas últimas transações?"
    
    user_text = st.chat_input("Digite sua dúvida (ex: Como estão meus gastos este mês? Onde devo investir?)")

    prompt = acao or user_text

    if prompt:
        
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Analisando seu perfil e portfólio..."):
                resposta = st.session_state.chat_session.send_message(prompt)
                st.markdown(resposta.text)
else:
    st.warning("⚠️ Insira sua API Key na barra lateral à esquerda para iniciar o atendimento.")
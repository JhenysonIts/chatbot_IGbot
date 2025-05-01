import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="It’s Prompt Assistant", page_icon="🤖")
st.title("🤖 Assistente de Conteúdo – It’s Prompt")

# Memória de histórico do chat
if "history" not in st.session_state:
    st.session_state.history = []

# Campo de input do usuário
user_input = st.chat_input("Escreva sua mensagem ou dúvida...")

# URL do webhook do seu n8n
N8N_WEBHOOK_URL = "https://itsprompt.app.n8n.cloud/webhook-test/9edaecd3-2ac9-4979-a7fb-07cec91a0e58"  # Substitua aqui

# Envia mensagem para o webhook ao submeter
if user_input:
    st.session_state.history.append(("user", user_input))

    try:
        response = requests.post(N8N_WEBHOOK_URL, json={"message": user_input})
        response.raise_for_status()
        data = response.json()
        ai_reply = data.get("response", "Desculpe, não consegui entender.")
    except Exception as e:
        ai_reply = f"[Erro ao conectar com n8n: {str(e)}]"

    st.session_state.history.append(("ai", ai_reply))

# Exibe histórico de chat (mais recente no final)
for role, text in reversed(st.session_state.history):
    if role == "user":
        st.chat_message("user").markdown(text)
    else:
        st.chat_message("assistant").markdown(text)

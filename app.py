import streamlit as st
import requests

st.set_page_config(page_title="Chatbot IA Local (Ollama)", layout="centered")
st.title("Chatbot de Bem-Estar Emocional (rodando localmente)")

# Prompt fixo como instrução inicial
system_prompt = """Você é um assistente emocional. Siga este roteiro:
1. Cumprimente o usuário de forma acolhedora.
2. Pergunte como ele está se sentindo.
3. Sugira uma técnica de respiração, reflexão ou foco.
4. Finalize com uma mensagem positiva e motivadora."""

OLLAMA_URL = "http://localhost:11434/api/chat"

# Iniciar histórico
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

# Mostrar histórico na interface
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Campo de entrada
user_input = st.chat_input("Como você está se sentindo hoje?")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = requests.post(
                    OLLAMA_URL,
                    json={
                        "model": "mistral",
                        "messages": st.session_state.messages,
                        "stream": False
                    }
                )
                content = response.json()["message"]["content"]
            except Exception as e:
                content = f"Erro ao conectar com o Ollama: {e}"
            st.markdown(content)
            st.session_state.messages.append({"role": "assistant", "content": content})

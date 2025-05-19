import streamlit as st
from openai import OpenAI

# Configurações iniciais
st.set_page_config(page_title="Chatbot IA Emocional", layout="centered")
st.title("Chatbot de Bem-Estar Emocional")

# Instancia o cliente OpenAI com a chave do secrets
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error(f"Erro ao carregar chave da OpenAI: {e}")
    st.stop()

# Prompt fixo
system_prompt = """
Você é um assistente emocional. Siga este roteiro:
1. Cumprimente o usuário.
2. Pergunte como ele está se sentindo.
3. Sugira uma técnica de respiração, reflexão ou foco.
4. Finalize com uma mensagem positiva.
"""

# Inicializar histórico
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Mostrar mensagens anteriores
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Campo de entrada do usuário
user_input = st.chat_input("Como você está se sentindo hoje?")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages,
                    temperature=0.7
                )
                msg = response.choices[0].message.content
            except Exception as e:
                msg = f"Erro ao acessar a API da OpenAI: {e}"
            st.markdown(msg)

    st.session_state.messages.append({"role": "assistant", "content": msg})

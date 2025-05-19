import streamlit as st
import requests

st.set_page_config(page_title="Chatbot IA Emocional (FLAN-T5)", layout="centered")
st.title("Chatbot de Bem-Estar Emocional")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"
headers = {
    "Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_KEY']}"
}

# Prompt fixo do sistema
system_prompt = """Você é um assistente emocional. Siga este roteiro:
1. Cumprimente o usuário.
2. Pergunte como ele está se sentindo.
3. Sugira uma técnica de respiração, reflexão ou foco.
4. Finalize com uma mensagem positiva.
Usuário: {mensagem}
Assistente:"""

# Histórico da conversa
if "history" not in st.session_state:
    st.session_state.history = []

for role, content in st.session_state.history:
    with st.chat_message(role):
        st.markdown(content)

user_input = st.chat_input("Como você está se sentindo hoje?")
if user_input:
    st.session_state.history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            prompt = system_prompt.replace("{mensagem}", user_input)

            try:
                response = requests.post(
                    API_URL,
                    headers=headers,
                    json={"inputs": prompt},
                    timeout=60
                )
                if response.status_code != 200:
                    st.error(f"Erro HTTP {response.status_code}: {response.text}")
                    raise Exception("Resposta não OK")
                result = response.json()
                msg = result[0]["generated_text"].strip()
            except Exception as e:
                msg = f"Erro ao acessar Hugging Face API: {e}"

            st.markdown(msg)
            st.session_state.history.append(("assistant", msg))

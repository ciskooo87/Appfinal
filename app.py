import streamlit as st
import requests

st.set_page_config(page_title="Chatbot IA Emocional (Debug)", layout="centered")
st.title("Chatbot de Bem-Estar Emocional")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
headers = {
    "Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_KEY']}"
}

system_prompt = """Você é um assistente emocional. Siga este roteiro:
1. Cumprimente o usuário.
2. Pergunte como ele está se sentindo.
3. Sugira uma técnica de respiração, reflexão ou foco.
4. Finalize com uma mensagem positiva.
"""

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
            full_prompt = system_prompt + "\n\n"
            for role, content in st.session_state.history:
                prefix = "Usuário:" if role == "user" else "Assistente:"
                full_prompt += f"{prefix} {content}\n"
            full_prompt += "Assistente:"

            try:
                response = requests.post(
                    API_URL,
                    headers=headers,
                    json={"inputs": full_prompt},
                    timeout=60
                )

                if response.status_code != 200:
                    st.error(f"Erro HTTP {response.status_code}: {response.text}")
                    raise Exception("Resposta não OK")

                result = response.json()
                msg = result[0]["generated_text"].split("Assistente:")[-1].strip()
            except Exception as e:
                msg = f"Erro ao acessar Hugging Face API: {e}"
            st.markdown(msg)

    st.session_state.history.append(("assistant", msg))

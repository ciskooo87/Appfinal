import streamlit as st
import requests
import time

st.set_page_config(page_title="Chatbot IA Emocional (LLaMA 2)", layout="centered")
st.title("Chatbot de Bem-Estar Emocional")

API_URL = "https://api.replicate.com/v1/predictions"
headers = {
    "Authorization": f"Token {st.secrets['REPLICATE_API_TOKEN']}",
    "Content-Type": "application/json"
}

# Prompt base
def build_prompt(user_input):
    return f"""
Você é um assistente emocional. Siga este roteiro:
1. Cumprimente o usuário.
2. Pergunte como ele está se sentindo.
3. Sugira uma técnica de respiração, reflexão ou foco.
4. Finalize com uma mensagem positiva.

Usuário: {user_input}
Assistente:
"""

# Histórico
if "history" not in st.session_state:
    st.session_state.history = []

# Mostrar mensagens anteriores
for role, content in st.session_state.history:
    with st.chat_message(role):
        st.markdown(content)

# Entrada do usuário
user_input = st.chat_input("Como você está se sentindo hoje?")
if user_input:
    st.session_state.history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            prompt = build_prompt(user_input)

            try:
                response = requests.post(API_URL, headers=headers, json={
                    "version": "9ac8e6e3d0e23c84f1cc1746d1c59a36892b4733b5f9784b5c3f4e00f33f3f2b",
                    "input": {
                        "prompt": prompt,
                        "temperature": 0.7,
                        "max_new_tokens": 200
                    }
                })

                if response.status_code != 201:
                    st.error(f"Erro HTTP {response.status_code}: {response.text}")
                    raise Exception("Falha na criação da predição")

                prediction = response.json()
                prediction_url = prediction["urls"]["get"]
                status = prediction["status"]

                while status not in ["succeeded", "failed"]:
                    time.sleep(1)
                    result = requests.get(prediction_url, headers=headers).json()
                    status = result["status"]

                if status == "succeeded":
                    msg = result["output"]
                else:
                    msg = f"Erro: {result.get('error', 'Falha desconhecida')}"
            except Exception as e:
                msg = f"Erro ao acessar Replicate API: {e}"

            st.markdown(msg)
            st.session_state.history.append(("assistant", msg))

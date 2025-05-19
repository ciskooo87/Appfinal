import streamlit as st
import requests

st.set_page_config(page_title="Chatbot IA Emocional (Replicate)", layout="centered")
st.title("Chatbot de Bem-Estar Emocional")

# Configurar chave da API Replicate
headers = {
    "Authorization": f"Token {st.secrets['REPLICATE_API_TOKEN']}",
    "Content-Type": "application/json"
}

# Mistral 7B via Replicate (https://replicate.com/mistralai/mistral-7b-instruct)
API_URL = "https://api.replicate.com/v1/predictions"

# Prompt base
system_prompt = """Você é um assistente emocional. Siga este roteiro:
1. Cumprimente o usuário.
2. Pergunte como ele está se sentindo.
3. Sugira uma técnica de respiração, reflexão ou foco.
4. Finalize com uma mensagem positiva.

Usuário: {mensagem}
Assistente:"""

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
                response = requests.post(API_URL, headers=headers, json={
                    "version": "e13c1c22ba0a4a84a8f21946b69c36f4858e95c048e8047be4ea4e6e7bcd9fc8",
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

                # Aguardar resultado da predição
                import time
                status = prediction["status"]
                while status not in ["succeeded", "failed"]:
                    time.sleep(1)
                    result = requests.get(prediction_url, headers=headers).json()
                    status = result["status"]

                if status == "succeeded":
                    msg = result["output"]
                else:
                    msg = f"Erro na execução: {result.get('error', 'desconhecido')}"
            except Exception as e:
                msg = f"Erro ao acessar Replicate API: {e}"

            st.markdown(msg)
            st.session_state.history.append(("assistant", msg))

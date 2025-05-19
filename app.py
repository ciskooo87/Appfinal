import streamlit as st
import replicate

st.set_page_config(page_title="Chatbot IA Emocional (LLaMA 3)", layout="centered")
st.title("Chatbot de Bem-Estar Emocional")

# Inicializa o cliente do Replicate
replicate_client = replicate.Client(api_token=st.secrets["REPLICATE_API_TOKEN"])

# Cria prompt estruturado
def build_prompt(user_input: str) -> str:
    return f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
Você é um assistente emocional. Siga este roteiro:
1. Cumprimente o usuário.
2. Pergunte como ele está se sentindo.
3. Sugira uma técnica de respiração, reflexão ou foco.
4. Finalize com uma mensagem positiva.
<|start_header_id|>user<|end_header_id|>
{user_input}
<|start_header_id|>assistant<|end_header_id|>"""

# Histórico
if "history" not in st.session_state:
    st.session_state.history = []

# Mostrar histórico
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
            full_response = ""
            try:
                for event in replicate_client.stream(
                    "meta/meta-llama-3-70b",
                    input={
                        "top_p": 0.9,
                        "prompt": prompt,
                        "temperature": 0.7,
                        "max_tokens": 300,
                        "presence_penalty": 1.15,
                    }
                ):
                    full_response += event
                    st.markdown(full_response)
            except Exception as e:
                st.markdown(f"Erro ao acessar Replicate: {e}")
                full_response = "Erro ao gerar resposta."

    st.session_state.history.append(("assistant", full_response))

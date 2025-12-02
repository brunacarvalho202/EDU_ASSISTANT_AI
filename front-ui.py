import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"

st.title("💬 EDU - Assistente estudantil")

user_input = st.text_input("Digite sua mensagem:")

if st.button("Enviar"):
    if user_input.strip():
        with st.spinner("Gerando resposta..."):
            response = requests.post(API_URL, json={"message": user_input})

            if response.status_code == 200:
                st.success(response.json()["response"])
            else:
                st.error(f"Erro ao chamar a API.{response.text}")

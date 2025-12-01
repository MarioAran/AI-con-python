import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.schema import HumanMessage  # Import correcto según la versión

st.set_page_config(layout="wide")
st.title("Chat con Slider de Temperatura")

if "messages" not in st.session_state:
    st.session_state.messages = []

def clean_history():
    st.session_state.messages = []

col_chat, col_slider = st.columns([3, 1])

with col_chat:
    # Mostrar historial
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Escribe tu mensaje aquí...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Temperatura
        current_temperature = st.session_state.get("temperature_slider_value", 0.7)

        # Inicializa modelo
        chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=current_temperature)

        # Genera respuesta
        response = chat_model.agenerate([[HumanMessage(content=prompt)]])
        assistant_response = response.generations[0][0].text  # Extrae el texto real

        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

with col_slider:
    st.subheader("Configuración de IA")
    temperature = st.slider(
        "Temperatura de la IA",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        key="temperature_slider"
    )
    st.session_state.temperature_slider_value = temperature
    st.write(f"Temperatura seleccionada: **{temperature}**")
    st.markdown("---")
    st.button("Limpiar chat", key="clean_chat_button", on_click=clean_history)

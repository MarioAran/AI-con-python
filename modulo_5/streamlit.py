import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# Configuración inicial
st.set_page_config(page_title="Chatbot Básico", page_icon="🤖")
st.title("🤖 Chatbot - paso 2 - con LangChain")
st.markdown("Este es un *chatbot de ejemplo* construido con LangChain + Streamlit.")

# --- Inicializar session_state correctamente ---
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# --- Columnas para layout ---
col1, col2 = st.columns([3, 1])  

# Función para limpiar historial
def clean_history():
    st.session_state.mensajes = []

# --- Controles en columna derecha ---
with col2:
    st.header("Controles")
    temperatura = st.slider("Temperatura del bot", min_value=0.0, max_value=1.0, value=0.7, step=0.05)
    st.button(label="Borrar historial", key="delete_history", on_click=clean_history)

# --- Instanciar modelo con la temperatura seleccionada ---
chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=temperatura)

# --- Chat en columna izquierda ---
with col1:
    for msg in st.session_state.mensajes:
        role = "assistant" if isinstance(msg, AIMessage) else "user"
        with st.chat_message(role):
            st.markdown(msg.content)

    pregunta = st.chat_input("Escribe tu mensaje:")
    if pregunta:
        with st.chat_message("user"):
            st.markdown(pregunta)

        st.session_state.mensajes.append(HumanMessage(content=pregunta))

        # Llamada al modelo
        respuesta = chat_model.invoke(st.session_state.mensajes)

        with st.chat_message("assistant"):
            st.markdown(respuesta.content)

        st.session_state.mensajes.append(respuesta)

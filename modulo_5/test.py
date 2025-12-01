import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage

# Configura la página para usar el layout "wide" para tener más espacio horizontal
st.set_page_config(layout="wide")

# 1. Define las columnas
# La lista [3, 1] significa que la primera columna (para el chat) ocupará 3 partes
# y la segunda columna (para el slider) ocupará 1 parte del ancho total.
# Puedes ajustar estos números según cuánto espacio quieras para cada sección.
col_chat, col_slider = st.columns([3, 1]) # Por ejemplo, 3/4 para el chat, 1/4 para el slider

# 2. Coloca los elementos del chat en la primera columna
with col_chat:
    st.title("Mi Chat con Slider de Temperatura")

    # Inicializa el historial del chat si no existe en st.session_state
    def clean_history():
        st.session_state.messages = []
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Muestra los mensajes del historial del chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de texto para nuevos mensajes del usuario
    prompt = st.chat_input("Escribe tu mensaje aquí...")
    if prompt:
        # Añade el mensaje del usuario al historial
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Muestra el mensaje del usuario
        with st.chat_message("user"):
            st.markdown(prompt)
        current_temperature = st.session_state.get("temperature_slider_value", 0.7)
        chat_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature = current_temperature)
        assistant_response = f"Has dicho: '{prompt}'. (Temperatura usada: **{current_temperature}**). Este es un mensaje de prueba del asistente."
# 3. Coloca el slider en la segunda columna


with col_slider:
    st.subheader("Configuración de IA")

    # El slider para la temperatura
    temperature = st.slider(
        "Temperatura de la IA",
        min_value=0.0,
        max_value=1.0,
        value=0.7, # Valor por defecto
        step=0.2, # Paso de incremento/decremento
        key="temperature_slider" # Clave única para el slider
    )

    st.write(f"Temperatura seleccionada: **{temperature}**")

    # Guarda el valor del slider en st.session_state para que la lógica del chat pueda acceder a él
    st.session_state.temperature_slider_value = temperature

    st.markdown("---")
    st.write("Aquí puedes añadir otros ajustes o información relevante.")
    st.button("this is a clean button", key="clean_chat_botton",on_click = clean_history())

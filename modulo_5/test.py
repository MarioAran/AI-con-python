from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages.human import HumanMessage
import os

api_key = os.environ.get("GOOGLE_API_KEY")
print(api_key)
if api_key is None:
    raise ValueError("No se encontró la variable de entorno GOOGLE_API_KEY")


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

pregunta = input("¿Pregunta?: ")
mensaje = HumanMessage(content=pregunta)

respuesta = llm.invoke([mensaje])
print("Respuesta:", respuesta.content)

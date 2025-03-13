import streamlit as st
from src.agent import app  # Importar el flujo de trabajo de LangGraph
import pyperclip  # Para copiar texto al portapapeles

# Configuración de la página
st.set_page_config(
    page_title="Generador de Correos Electrónicos",
    page_icon="📧",
    layout="centered",
)

# Título y descripción
st.title("📧 Generador de Correos Electrónicos")
st.markdown("""
    **Genera correos electrónicos personalizados para ventas.**  
    Ingresa el nombre de la empresa y obtén un correo listo para usar.
""")

# Función para ejecutar el flujo de trabajo
def run_langgraph_workflow(company):
    """Ejecuta el flujo de trabajo en LangGraph y retorna el resultado."""
    entradas = {"company": company, "num_steps": 0}
    
    resultado = None
    for salida in app.stream(entradas):
        for clave, valor in salida.items():
            if clave == "state_printer":
                resultado = valor["final_email"]
    
    return resultado

# Entrada de datos
company = st.text_input("Nombre de la empresa", placeholder="Ej: Mercado Libre")

# Botón para generar el correo
if st.button("Generar Correo Electrónico"):
    if not company:
        st.error("⚠️ Por favor, ingresa el nombre de la empresa.")
    else:
        with st.spinner("Generando correo..."):
            salida = run_langgraph_workflow(company)["final_email"]
        
        if salida:
            st.success("✅ Correo generado con éxito!")
            st.subheader("✉️ Correo Generado")
            st.text_area("Vista Previa", salida, height=300, key="email_output")
            
            # Botón para copiar al portapapeles
            if st.button("📋 Copiar al portapapeles"):
                pyperclip.copy(salida)
                st.success("Texto copiado al portapapeles!")
        else:
            st.error("❌ No se pudo generar el correo. Verifica los datos ingresados.")
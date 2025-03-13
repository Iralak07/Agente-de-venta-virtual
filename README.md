# Agente de Automatización con LangGraph

Este agente inteligente está construido con **LangGraph**, una poderosa herramienta para crear flujos de trabajo basados en grafos. Combina técnicas de **búsqueda en la web**, **procesamiento de lenguaje natural (NLP)** y **generación de texto** para ofrecer una solución integral en la automatización de correos empresariales.

## Características Principales

### 🔎 Búsqueda Automática de Información
El agente recopila información relevante sobre la empresa en tiempo real utilizando herramientas de búsqueda en la web.

### 📧 Generación de Correos Personalizados
Utiliza la información recopilada para redactar correos electrónicos adaptados a las necesidades específicas de cada empresa.

### 🔍 Análisis y Optimización
Antes de finalizar, el agente revisa el borrador del correo y ofrece mejoras para asegurar que sea convincente y relevante.

### 💻 Interfaz Amigable
Una interfaz sencilla y funcional creada con **Streamlit** permite a los usuarios interactuar fácilmente con el agente.

### ⏳ Automatización Completa
Desde la búsqueda de información hasta la generación del correo, todo el proceso está automatizado, ahorrando tiempo y esfuerzo a los equipos de ventas.

## Tecnologías Utilizadas

- **LangGraph**: Para definir y gestionar el flujo de trabajo del agente.
- **Streamlit**: Para crear una interfaz web interactiva.
- **Tavily API**: Para realizar búsquedas en la web y obtener información relevante.
- **NLP (Procesamiento de Lenguaje Natural)**: Para analizar y generar contenido de manera inteligente.

## ⚙️ Cómo Funciona

1. **Entrada del Usuario**:
   - El usuario ingresa el nombre de la empresa en la interfaz de **Streamlit**.
2. **Búsqueda de Información**:
   - El agente realiza una búsqueda automática en Internet para recopilar datos clave sobre la empresa.
3. **Generación del Borrador**:
   - Utiliza la información recopilada para redactar un correo electrónico persuasivo y adaptado.
4. **Análisis y Mejora**:
   - Un módulo especializado revisa el borrador y sugiere mejoras si es necesario.
5. **Salida Final**:
   - Se presenta el correo optimizado en la interfaz, listo para ser copiado o enviado.

## 👨‍💻 Instalación y Uso

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/Iralak07/Agente-de-venta-virtual.git
   cd app
   ```

2. Instalar dependencias:
   ```bash
   pip install langchain langgraph langchain_groq langchain_community streamlit
   ```

3. Configurar las claves API en las variables de entorno:
   ```python
   import os
   os.environ["GROQ_API_KEY"] = "TU_CLAVE_AQUI"
   os.environ["TAVILY_API_KEY"] = "TU_CLAVE_AQUI"
   ```

4. Ejecutar la aplicación:
   ```bash
   streamlit run app.py
   ```
---

Este proyecto está diseñado para optimizar la generación de correos y mejorar la eficiencia en la captación de clientes a través de la inteligencia artificial. 🌟


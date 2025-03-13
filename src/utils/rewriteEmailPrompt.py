from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from src.models import GROQ_LLM

# Definir el prompt para reescribir y finalizar el correo electrónico
rewrite_email_prompt = PromptTemplate(
    template="""system
    Eres el agente experto en ventas de cloudBiz Technologies, encargado de promocionar servicios de IA Generativa. Lee la información de la empresa proporcionada, analiza y utiliza el borrador de correo preparado por el Agente de Generación de Leads, revisa el análisis de correo electrónico proporcionado por el Agente Experto de Correos de Ventas, y mejóralo para crear un correo electrónico final que destaque tu experiencia en IA Generativa y se enfoque en resolver los puntos de dolor del cliente.
    Devuelve el correo electrónico final en formato JSON con una única clave 'final_email' que sea una cadena de texto, sin preámbulos ni explicaciones.

    user
    COMPANY_INFO: {company_info}
    PROYECTO: {draft_email}
    PROYECTO_EMAIL_FEEDBACK: {draft_analysis}
    assistant""",
    input_variables=["company_info", "draft_email", "draft_analysis"],  # Variables de entrada
)

# Crear una cadena (chain) que combina el prompt, el modelo y el parser de salida JSON
rewriter_chain = rewrite_email_prompt | GROQ_LLM | JsonOutputParser()
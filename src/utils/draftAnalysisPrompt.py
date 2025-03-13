from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from src.models import GROQ_LLM

# Definir el prompt para analizar el borrador del correo electrónico
draft_analysis_prompt = PromptTemplate(
    template="""system
    Eres el agente experto en Correos de Ventas. Lee el PROYECTO_EMAIL y la COMPANY_INFO.
    Verifica si el PROYECTO_EMAIL aborda los puntos clave que se deben destacar para la empresa en relación con cloudBiz Technologies y si es lo suficientemente impresionante para enviarlo al cliente.

    Proporciona retroalimentación sobre cómo se puede mejorar el correo electrónico y qué cosas específicas se pueden agregar o cambiar para que el correo sea más efectivo en abordar los problemas del cliente.
    Devuelve "NO_FEEDBACK" si estás satisfecho con la calidad del correo.

    Devuelve el análisis en formato JSON con una única clave "draft_analysis" y sin preámbulos ni explicaciones.

    user
    COMPANY_INFO: {company_info}
    PROYECTO: {draft_email}
    assistant""",
    input_variables=["company_info", "draft_email"],  # Variables de entrada: información de la empresa y borrador del correo
)

# Crear una cadena (chain) que combina el prompt, el modelo y el parser de salida JSON
draft_analysis_chain = draft_analysis_prompt | GROQ_LLM | JsonOutputParser()
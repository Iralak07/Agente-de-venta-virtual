from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from src.models import GROQ_LLM

# Definir el prompt para redactar un correo electrónico
write_email_prompt = PromptTemplate(
    template="""system
    Eres el Agente de Generación de Leads para la empresa cloudBiz, encargado de promocionar servicios de IA Generativa. Lee la información de la empresa y utilízala para crear un borrador de correo electrónico que comience con una introducción formal de cloudBiz, y explica cómo la IA Generativa puede mejorar la eficiencia de las operaciones de la empresa dada, dependiendo de sus productos y servicios.
    Puedes utilizar una o más de las siguientes soluciones de cloudBiz, según el dominio de la empresa, para promocionar el trabajo actual de cloudBiz que sea más adecuado para la empresa en cuestión.
    Soluciones de cloudBiz para usar en el correo:
    1. eCAI (IA Conversacional Empresarial)
    2. Intellexi (Analizador de documentos inteligente para convertir datos no estructurados en datos estructurados)
    3. Aspira (Agente de Entrevistas Inteligente impulsado por IA)
    Además, agrega casos de uso específicos del dominio que se ajusten a las necesidades del cliente.
    Devuelve el borrador del correo electrónico en formato JSON con una única clave 'draft_email' que sea una cadena de texto, sin preámbulos ni explicaciones.

    user
    INFORMACIÓN_DE_LA_EMPRESA: {company_info} \n\n
    assistant""",
    input_variables=["company_info"],  # La plantilla espera una variable llamada 'company_info'
)

# Crear una cadena (chain) que combina el prompt, el modelo y el parser de salida JSON
writer_chain = write_email_prompt | GROQ_LLM | JsonOutputParser()
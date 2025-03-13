from langchain.prompts import PromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.output_parsers import JsonOutputParser
from src.models import GROQ_LLM

# Definir la herramienta de búsqueda
web_search_tool = TavilySearchResults(k=1)

# Prompt para generar palabras clave de búsqueda
search_keyword_prompt = PromptTemplate(
    template="""system
    Eres un experto en determinar las mejores palabras clave en castellano para buscar en la web y obtener la mejor información para el cliente, dado el Nombre de la Empresa. Determina las mejores palabras clave que encontrarán la mejor información para obtener todos los detalles sobre la empresa, incluyendo los productos y servicios clave de la empresa, noticias recientes del mercado sobre la empresa, el trabajo activo del equipo de liderazgo de la empresa en las últimas tecnologías, y cualquier noticia relacionada con el uso de IA Generativa en la empresa.
    Devuelve un JSON con una única clave 'keywords' con no más de 5 palabras clave y sin preámbulo ni explicación.

    user
    NOMBRE_DE_LA_EMPRESA: {company} \n
    assistant""",
    input_variables=["company"],
)

search_keyword_chain = search_keyword_prompt | GROQ_LLM | JsonOutputParser()
from langchain_core.documents import Document  # Para crear documentos con el contenido de las búsquedas
from src.utils.searchKeywordPrompt import search_keyword_chain, web_search_tool
from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

from src.utils.writeEmailPrompt import writer_chain
from src.utils.draftAnalysisPrompt import draft_analysis_chain
from src.utils.rewriteEmailPrompt import rewriter_chain

# Definir una clase GraphState que representa el estado del flujo de trabajo
class GraphState(TypedDict):
    company: str
    draft_email: str
    final_email: str
    company_info: List[str]
    info_needed: bool
    num_steps: int
    draft_analysis: str


# Definir la función principal para buscar información sobre la empresa
def company_info_search(state):
    # Mensaje de inicio para indicar que la búsqueda ha comenzado
    print("---BÚSQUEDA DE INFORMACIÓN DE INVESTIGACIÓN DE EMPRESAS---")

    # Extraer el nombre de la empresa del estado actual
    company = state['company']

    # Incrementar el contador de pasos en 1
    num_steps = state['num_steps'] + 1

    # Generar palabras clave de búsqueda utilizando la cadena search_keyword_chain
    # Se pasa el nombre de la empresa y se extrae la lista de palabras clave del JSON resultante
    keywords = search_keyword_chain.invoke({"company": company})['keywords']
    # Inicializar una lista vacía para almacenar los resultados de las búsquedas
    full_searches = []

    # Iterar sobre cada palabra clave generada
    for keyword in keywords:
        # Imprimir la palabra clave actual (para fines de seguimiento o depuración)
        print(keyword)

        # Realizar una búsqueda en la web utilizando la herramienta web_search_tool
        # Se pasa la palabra clave como consulta (query)
        temp_docs = web_search_tool.invoke({"query": keyword})

        # Extraer el contenido de los resultados de la búsqueda y unirlos en una sola cadena
        web_results = "\n".join([d["content"] for d in temp_docs])

        # Crear un objeto Document con el contenido de los resultados y añadirlo a la lista full_searches
        full_searches.append(Document(page_content=web_results))

    # Devolver un diccionario con los resultados de las búsquedas y el contador de pasos actualizado
    return {"company_info": full_searches, "num_steps": num_steps}


def draft_email_writer(state):
    # Mensaje de inicio para indicar que el borrador del correo ha comenzado
    print("---CREANDO BORRADOR DE CORREO ELECTRÓNICO---")
    company_info = state['company_info']

    # Generar el borrador del correo utilizando la cadena writer_chain
    draf_email = writer_chain.invoke({"company_info": company_info})

    # Incrementar el contador de pasos en 1
    num_steps = state['num_steps'] + 1
    
    # Devolver un diccionario con el borrador del correo y el contador de pasos actualizado
    return {"draft_email": draf_email, "num_steps": num_steps}

def analyze_draft_email(state):
    # Mensaje de inicio para indicar que el análisis del borrador del correo ha comenzado
    print("---ANALIZANDO BORRADOR DE CORREO ELECTRÓNICO---")
    company_info = state['company_info']
    draft_email = state['draft_email']

    # Generar el análisis del borrador del correo utilizando la cadena draft_analysis_chain
    analysis = draft_analysis_chain.invoke({"draft_email": draft_email, "company_info": company_info})

    # Incrementar el contador de pasos en 1
    num_steps = state['num_steps'] + 1

    # Devolver un diccionario con el análisis del borrador del correo y el contador de pasos actualizado
    return {"draft_analysis": analysis, "num_steps": num_steps}


def route_to_rewrite(state):
    print("---DECIDIR SI REESCRIBIR CORREO ELECTRÓNICO---")
    draft_analysis = state['draft_analysis']
    num_steps = state['num_steps']
    # Decidir si se debe reescribir el correo
    if draft_analysis['draft_analysis'] == "NO FEEDBACK":
        return "no_rewrite"
    else:
        return "rewrite"

def rewrite_email(state):
    print("---REESCRIBIENDO EL CORREO ELECTRÓNICO---")
    draft_email = state['draft_email']
    draft_analysis = state['draft_analysis']
    company_info = state['company_info']

    # Reescribir el correo utilizando la cadena rewriter_chain
    final_email = rewriter_chain.invoke({"draft_email": draft_email, "draft_analysis": draft_analysis, "company_info": company_info})

    # Incrementar el contador de pasos en 1
    num_steps = state['num_steps'] + 1

    # Devolver un diccionario con el correo final y el contador de pasos actualizado
    return {"final_email": final_email, "num_steps": num_steps}

def no_rewrite(state):
    print("---NO ES NECESARIO REESCRIBIR---")
    draft_email = state['draft_email']

    # Incrementar el contador de pasos en 1
    num_steps = state['num_steps'] + 1

    # Devolver un diccionario con el borrador del correo y el contador de pasos actualizado
    return {"final_email": draft_email, "num_steps": num_steps}

def state_printer(state):
    print("---RESULTADO FINAL---")
    final_email = state['final_email']
    num_steps = state['num_steps']

    # Devolver un diccionario con el correo final y el contador de pasos actualizado
    return {"final_email": final_email, "num_steps": num_steps}


# Crear un flujo de trabajo utilizando StateGraph
flujo_de_trabajo = StateGraph(GraphState)

# Definir los nodos y su orden de ejecución
# Cada nodo representa una tarea específica en el flujo de trabajo
flujo_de_trabajo.add_node("company_info_search", company_info_search)  # Nodo para buscar información de la empresa
flujo_de_trabajo.add_node("draft_email_writer", draft_email_writer)  # Nodo para redactar el borrador del correo
flujo_de_trabajo.add_node("analyze_draft_email", analyze_draft_email)  # Nodo para analizar el borrador del correo
flujo_de_trabajo.add_node("rewrite_email", rewrite_email)  # Nodo para reescribir el correo si es necesario
flujo_de_trabajo.add_node("no_rewrite", no_rewrite)  # Nodo para saltar la reescritura si no es necesario
flujo_de_trabajo.add_node("state_printer", state_printer)  # Nodo para imprimir el estado actual del flujo de trabajo

# Establecer el punto de entrada del flujo de trabajo
# El flujo comienza con la búsqueda de información de la empresa
flujo_de_trabajo.set_entry_point("company_info_search")

# Conectar los nodos con bordes para definir la secuencia de ejecución
flujo_de_trabajo.add_edge("company_info_search", "draft_email_writer")  # Después de buscar información, redactar el borrador
flujo_de_trabajo.add_edge("draft_email_writer", "analyze_draft_email")  # Después de redactar, analizar el borrador

# Añadir un flujo condicional después de analizar el borrador
# La función "route_to_rewrite" decide si se debe reescribir el correo o no
flujo_de_trabajo.add_conditional_edges(
    "analyze_draft_email",  # Nodo desde el cual se toma la decisión
    route_to_rewrite,  # Función que decide la ruta a seguir
    {
        "rewrite": "rewrite_email",  # Si se necesita reescribir, ir al nodo "rewrite_email"
        "no_rewrite": "no_rewrite",  # Si no se necesita reescribir, ir al nodo "no_rewrite"
    },
)

# Conectar los nodos finales al nodo "state_printer"
flujo_de_trabajo.add_edge("no_rewrite", "state_printer")  # Si no se reescribe, imprimir el estado
flujo_de_trabajo.add_edge("rewrite_email", "state_printer")  # Si se reescribe, imprimir el estado

# Conectar el nodo "state_printer" al final del flujo de trabajo
flujo_de_trabajo.add_edge("state_printer", END)

# Compilar el flujo de trabajo para poder ejecutarlo
app = flujo_de_trabajo.compile()

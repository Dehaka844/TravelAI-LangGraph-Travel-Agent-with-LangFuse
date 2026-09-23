from typing import Literal

from pydantic import BaseModel, Field

from src.graph.state import AgentState
from src.llm.models import llm


class IntencionOutput(BaseModel):
    intencion: Literal["vuelos", "hoteles", "general"] = Field(
        description="Intención detectada en el mensaje del usuario."
    )

class CalidadOutput(BaseModel):
    score_calidad: float = Field(
        ge=0.0,
        le=1.0,
        description="Puntuación de calidad de la respuesta entre 0 y 1."
    )

    requiere_escalado: bool = Field(
        description="Indica si la consulta debe ser escalada a un agente humano."
    )


llm_clasificador = llm.with_structured_output(IntencionOutput)

llm_evaluador = llm.with_structured_output(CalidadOutput)


def clasificar_intencion(state: AgentState):
    mensaje = state["mensaje_usuario"]

    prompt = f"""
Clasifica la intención de la siguiente consulta de un cliente
de una agencia de viajes.

Debes elegir únicamente una de estas categorías:

- vuelos: consultas relacionadas con vuelos, rutas, aeropuertos,
  horarios, fechas de vuelo o reservas de vuelos.
- hoteles: consultas relacionadas con hoteles, alojamiento,
  habitaciones, servicios del hotel o reservas de hoteles.
- general: consultas relacionadas con información turística,
  destinos o cualquier consulta que no corresponda a vuelos u hoteles.

Consulta del usuario:
{mensaje}
"""

    resultado = llm_clasificador.invoke(prompt)

    return {
        "intencion": resultado.intencion
    }


def experto_vuelos(state: AgentState):
    mensaje = state["mensaje_usuario"]

    prompt = f"""
Eres el especialista en vuelos de TravelAI, una agencia de viajes.

Tu función es ayudar al cliente con consultas relacionadas con vuelos.

Analiza la consulta y proporciona una respuesta útil y clara.
Puedes orientar al usuario sobre rutas, fechas, aeropuertos,
horarios, equipaje y aspectos relacionados con vuelos.

IMPORTANTE:
No tienes acceso a sistemas reales de reservas ni a datos de
disponibilidad en tiempo real. Nunca inventes vuelos, precios,
horarios o disponibilidad.

Si el usuario solicita información que requiere datos en tiempo real,
indica claramente que sería necesario consultar el sistema de
reservas correspondiente.

Consulta del usuario:
{mensaje}
"""

    respuesta = llm.invoke(prompt)

    return {
        "respuesta_especialista": respuesta.content
    }


def experto_hoteles(state: AgentState):
    mensaje = state["mensaje_usuario"]

    prompt = f"""
Eres el especialista en hoteles de TravelAI, una agencia de viajes.

Tu función es ayudar al cliente con consultas relacionadas con
hoteles y alojamientos.

Analiza la consulta y proporciona una respuesta útil y clara.
Puedes orientar al usuario sobre tipos de alojamiento, servicios,
ubicación, habitaciones y aspectos relacionados con hoteles.

IMPORTANTE:
No tienes acceso a sistemas reales de reservas ni a datos de
disponibilidad en tiempo real. Nunca inventes hoteles, precios,
habitaciones o disponibilidad.

Si el usuario solicita información que requiere datos en tiempo real,
indica claramente que sería necesario consultar el sistema de
reservas correspondiente.

Consulta del usuario:
{mensaje}
"""

    respuesta = llm.invoke(prompt)

    return {
        "respuesta_especialista": respuesta.content
    }


def experto_general(state: AgentState):
    mensaje = state["mensaje_usuario"]

    prompt = f"""
Eres el especialista en información general de viajes de TravelAI,
una agencia de viajes.

Tu función es responder preguntas generales relacionadas con viajes,
destinos turísticos, recomendaciones, planificación y cultura.

Proporciona respuestas claras, útiles y personalizadas para el
usuario.

No inventes datos. Si una información puede depender de circunstancias
actuales o datos en tiempo real, indícalo claramente.

Consulta del usuario:
{mensaje}
"""

    respuesta = llm.invoke(prompt)

    return {
        "respuesta_especialista": respuesta.content
    }

def evaluar_calidad(state: AgentState):
    mensaje = state["mensaje_usuario"]
    respuesta = state["respuesta_especialista"]

    prompt = f"""
Eres un evaluador de calidad de respuestas de una agencia de viajes.

Debes evaluar la respuesta de un especialista teniendo en cuenta:

1. Relevancia:
   ¿La respuesta responde directamente a la consulta del usuario?

2. Utilidad:
   ¿La información proporcionada resulta útil para el usuario?

3. Claridad:
   ¿La respuesta está bien explicada y es fácil de comprender?

4. Fiabilidad:
   ¿Evita inventar información que no puede conocer?

5. Adecuación:
   ¿La respuesta es apropiada para la consulta realizada?

Asigna una puntuación entre 0 y 1:

- 0.0 = respuesta completamente inadecuada.
- 0.5 = respuesta parcialmente adecuada.
- 1.0 = respuesta excelente.

También determina si sería necesario escalar la consulta
a un agente humano.

La consulta original del usuario es:

{mensaje}

La respuesta generada por el especialista es:

{respuesta}
"""

    resultado = llm_evaluador.invoke(prompt)

    return {
        "score_calidad": resultado.score_calidad,
        "requiere_escalado": resultado.requiere_escalado,
    }

def generar_respuesta_final(state: AgentState):
    mensaje = state["mensaje_usuario"]
    respuesta_especialista = state["respuesta_especialista"]

    prompt = f"""
Eres el asistente final de TravelAI, una agencia de viajes.

Debes preparar la respuesta final que recibirá el usuario.

Consulta original:
{mensaje}

Respuesta proporcionada por el especialista:
{respuesta_especialista}

Requisitos:

- Mantén la información útil proporcionada por el especialista.
- Responde directamente a la consulta del usuario.
- Haz que la respuesta sea clara, natural y fácil de entender.
- No inventes información.
- No menciones procesos internos, nodos, evaluaciones,
  puntuaciones ni sistemas de IA.
- Si el especialista indica que no dispone de información
  en tiempo real, conserva esa aclaración.
"""

    respuesta = llm.invoke(prompt)

    return {
        "respuesta_final": respuesta.content
    }

def escalar_a_humano(state: AgentState):
    return {
        "respuesta_final": (
            "Tu consulta necesita una revisión más detallada por parte "
            "de uno de nuestros agentes. Hemos derivado la consulta "
            "para que un especialista pueda ayudarte de forma adecuada."
        )
    }
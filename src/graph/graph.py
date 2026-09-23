from langgraph.graph import StateGraph, END

from src.graph.state import AgentState
from src.graph.nodes import (
    clasificar_intencion,
    experto_vuelos,
    experto_hoteles,
    experto_general,
    evaluar_calidad,
    generar_respuesta_final,
    escalar_a_humano,
)
from src.graph.routers import (
    router_intencion,
    router_calidad,
)


def crear_grafo():
    workflow = StateGraph(AgentState)

    # ==========================================
    # NODOS
    # ==========================================

    workflow.add_node(
        "clasificar_intencion",
        clasificar_intencion
    )

    workflow.add_node(
        "experto_vuelos",
        experto_vuelos
    )

    workflow.add_node(
        "experto_hoteles",
        experto_hoteles
    )

    workflow.add_node(
        "experto_general",
        experto_general
    )

    workflow.add_node(
        "evaluar_calidad",
        evaluar_calidad
    )

    workflow.add_node(
        "generar_respuesta_final",
        generar_respuesta_final
    )

    workflow.add_node(
        "escalar_a_humano",
        escalar_a_humano
    )

    # ==========================================
    # PUNTO DE ENTRADA
    # ==========================================

    workflow.set_entry_point("clasificar_intencion")

    # ==========================================
    # ROUTER DE INTENCIÓN
    # ==========================================

    workflow.add_conditional_edges(
        "clasificar_intencion",
        router_intencion,
        {
            "vuelos": "experto_vuelos",
            "hoteles": "experto_hoteles",
            "general": "experto_general",
        }
    )

    # ==========================================
    # EXPERTOS → EVALUACIÓN
    # ==========================================

    workflow.add_edge(
        "experto_vuelos",
        "evaluar_calidad"
    )

    workflow.add_edge(
        "experto_hoteles",
        "evaluar_calidad"
    )

    workflow.add_edge(
        "experto_general",
        "evaluar_calidad"
    )

    # ==========================================
    # ROUTER DE CALIDAD
    # ==========================================

    workflow.add_conditional_edges(
        "evaluar_calidad",
        router_calidad,
        {
            "respuesta": "generar_respuesta_final",
            "escalar": "escalar_a_humano",
        }
    )

    # ==========================================
    # FINAL DEL GRAFO
    # ==========================================

    workflow.add_edge(
        "generar_respuesta_final",
        END
    )

    workflow.add_edge(
        "escalar_a_humano",
        END
    )

    return workflow.compile()


app = crear_grafo()
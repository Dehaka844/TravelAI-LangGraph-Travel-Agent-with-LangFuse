from src.graph.state import AgentState


def router_intencion(state: AgentState) -> str:
    """
    Decide a qué experto enviar la consulta
    según la intención detectada.
    """

    return state["intencion"]


def router_calidad(state: AgentState) -> str:
    """
    Decide si mostrar la respuesta o escalarla
    a un agente humano según la calidad.
    """

    if state["score_calidad"] < 0.6:
        return "escalar"

    return "respuesta"
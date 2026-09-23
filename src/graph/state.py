from typing import TypedDict


class AgentState(TypedDict):
    mensaje_usuario: str
    intencion: str
    respuesta_especialista: str
    score_calidad: float
    requiere_escalado: bool
    respuesta_final: str
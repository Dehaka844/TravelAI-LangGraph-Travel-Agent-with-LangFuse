from src.graph.nodes import evaluar_calidad


state = {
    "mensaje_usuario": "Quiero un vuelo de Madrid a París para el 15 de marzo",
    "intencion": "vuelos",
    "respuesta_especialista": """
Sí, hay vuelos baratos mañana. El vuelo sale a las 15:00,
cuesta 50 euros y tiene disponibilidad.
""",
    "score_calidad": 0.0,
    "requiere_escalado": False,
    "respuesta_final": "",
}


resultado = evaluar_calidad(state)

print("=" * 60)
print("EVALUACIÓN")
print("=" * 60)
print(f"Score de calidad: {resultado['score_calidad']}")
print(f"Requiere escalado: {resultado['requiere_escalado']}")
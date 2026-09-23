from src.graph.nodes import clasificar_intencion


test_cases = [
    "Quiero un vuelo de Madrid a París para el 15 de marzo",
    "Busco un hotel con piscina en Barcelona para 2 noches",
    "¿Cuál es la mejor época para visitar Japón?",
]


for mensaje in test_cases:
    state = {
        "mensaje_usuario": mensaje,
        "intencion": "",
        "respuesta_especialista": "",
        "score_calidad": 0.0,
        "requiere_escalado": False,
        "respuesta_final": "",
    }

    resultado = clasificar_intencion(state)

    print("=" * 60)
    print(f"Consulta: {mensaje}")
    print(f"Intención: {resultado['intencion']}")
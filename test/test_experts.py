from src.graph.nodes import (
    experto_vuelos,
    experto_hoteles,
    experto_general,
)


def crear_state(mensaje):
    return {
        "mensaje_usuario": mensaje,
        "intencion": "",
        "respuesta_especialista": "",
        "score_calidad": 0.0,
        "requiere_escalado": False,
        "respuesta_final": "",
    }


test_cases = [
    (
        "Quiero un vuelo de Madrid a París para el 15 de marzo",
        experto_vuelos,
    ),
    (
        "Busco un hotel con piscina en Barcelona para 2 noches",
        experto_hoteles,
    ),
    (
        "¿Cuál es la mejor época para visitar Japón?",
        experto_general,
    ),
]


for mensaje, experto in test_cases:
    resultado = experto(crear_state(mensaje))

    print("=" * 60)
    print(f"Consulta: {mensaje}")
    print()
    print("Respuesta:")
    print(resultado["respuesta_especialista"])
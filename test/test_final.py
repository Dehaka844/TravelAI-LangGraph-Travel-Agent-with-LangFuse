from src.graph.nodes import (
    generar_respuesta_final,
    escalar_a_humano,
)


state = {
    "mensaje_usuario": "Quiero un vuelo de Madrid a París para el 15 de marzo",
    "intencion": "vuelos",
    "respuesta_especialista": (
        "Para encontrar un vuelo de Madrid a París el 15 de marzo, "
        "es necesario consultar un sistema de reservas para comprobar "
        "la disponibilidad y los precios actuales. "
        "El aeropuerto principal de Madrid es Madrid-Barajas (MAD), "
        "mientras que en París existen varios aeropuertos."
    ),
    "score_calidad": 0.8,
    "requiere_escalado": False,
    "respuesta_final": "",
}


print("=" * 60)
print("RESPUESTA FINAL")
print("=" * 60)

resultado = generar_respuesta_final(state)

print(resultado["respuesta_final"])


print()
print("=" * 60)
print("ESCALADO")
print("=" * 60)

resultado_escalado = escalar_a_humano(state)

print(resultado_escalado["respuesta_final"])
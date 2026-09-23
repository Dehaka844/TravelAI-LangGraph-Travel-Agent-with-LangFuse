from src.graph.graph import app
from src.config.langfuse import langfuse, langfuse_handler


consultas = [
    "Quiero un vuelo de Madrid a París para el 15 de marzo",
    "Busco un hotel con piscina en Barcelona para 2 noches",
    "¿Cuál es la mejor época para visitar Japón?",
]


for consulta in consultas:

    print()
    print("=" * 70)
    print(f"CONSULTA: {consulta}")
    print("=" * 70)

    resultado = app.invoke(
        {
            "mensaje_usuario": consulta
        },
        config={
            "callbacks": [langfuse_handler],
            "run_name": "TravelAI",
            "metadata": {
                "application": "TravelAI",
                "framework": "LangGraph",
            },
        }
    )

    print(f"Intención: {resultado['intencion']}")
    print(f"Score calidad: {resultado['score_calidad']}")
    print(f"Requiere escalado: {resultado['requiere_escalado']}")

    print()
    print("RESPUESTA FINAL:")
    print(resultado["respuesta_final"])

    # Obtener el trace generado por LangFuse
    trace_id = langfuse_handler.last_trace_id

    if trace_id:
        langfuse.create_score(
            name="score_calidad",
            value=float(resultado["score_calidad"]),
            trace_id=trace_id,
            data_type="NUMERIC",
            comment="Puntuación generada por el evaluador de calidad de TravelAI."
        )


langfuse.flush()
from src.llm.models import llm
from src.config.langfuse import langfuse, langfuse_handler


response = llm.invoke(
    "Responde únicamente con: LangFuse funciona correctamente.",
    config={
        "callbacks": [langfuse_handler]
    }
)

print("=" * 60)
print("RESPUESTA")
print("=" * 60)
print(response.content)


langfuse.flush()